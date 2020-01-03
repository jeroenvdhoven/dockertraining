import os

import joblib
import pandas as pd
from flask import Flask

from main import output_folder
from typing import List
import json


def create_model_paths(files: List[str]):
    output_folder_files = map(
        lambda f: os.path.join(output_folder, f),
        files
    )
    return [
        file if os.path.isfile(file) else os.path.join("static", file)
        for file in output_folder_files
    ]


# Start an application
app = Flask(__name__)

# Get the paths of the models to be used
original_files = os.listdir(output_folder)
target_files = create_model_paths(original_files)

# Read the pipelines
pipelines = {
    original_file: joblib.load(target_file)
    for target_file, original_file in zip(target_files, original_files)
}


@app.route('/<string:model>/<string:data>')
def predict(model: str, data: str):
    converted_data = pd.read_json(data)
    return json.dumps({
        "model": model,
        "predictions": pipelines[model].transform(converted_data).tolist()
    })


# Run the app only if this file is run.
if __name__ == "__main__":
    app.run()
