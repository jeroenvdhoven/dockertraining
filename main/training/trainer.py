import os

import pandas as pd
from joblib import dump
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, FunctionTransformer

from main import output_folder, model_file
from main.training.model_functions import call_model, reverse_labels

if __name__ == "__main__":
    # Read data
    data = pd.read_csv(os.path.join("main", "training", "iris.csv"))
    data = data[data["Species"].isin(["setosa", "virginica"])]

    # Split into x and y
    x = data.drop("Species", axis=1)
    y = data[["Species"]]

    # Make preprocessing pipelines
    x_pipeline = Pipeline([
        ("scaling", StandardScaler()),
    ])
    x_fit = x_pipeline.fit_transform(x)

    y_pipeline = Pipeline([
        ("labeler", OrdinalEncoder()),
    ])
    y_fit = y_pipeline.fit_transform(y)

    # Fit the pipeline
    model = LogisticRegression(solver="lbfgs")
    model.fit(x_fit, y_fit)

    # Create a fully integrated pipeline
    prediction_pipeline = Pipeline([
        ("preprocessing", x_pipeline),
        ("pipeline", FunctionTransformer(func=call_model, kw_args={"model": model})),
        ("retransform labels", FunctionTransformer(
            # Turn the 0-1 labels back into setosa / virginica labels
            func=reverse_labels,
            validate=False,
            kw_args={"pipe": y_pipeline}),
         )
    ])

    # Try the full pipeline
    preds = prediction_pipeline.transform(x)
    print(confusion_matrix(y, preds))

    # Save models
    os.makedirs(output_folder, exist_ok=True)
    dump(prediction_pipeline, os.path.join(output_folder, model_file))
