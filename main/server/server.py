from flask import Flask
import joblib
import os
import pandas as pd

from main import output_folder, model_file

# Start an application
app = Flask(__name__)

# Read the pipeline
target_file = os.path.join(output_folder, model_file)
if not os.path.isfile(target_file):
    target_file = os.path.join("main", "server", "static", model_file)

pipeline = joblib.load(target_file)


@app.route('/<string:data>')
def predict(data: str):
    converted_data = pd.read_json(data)
    return str(pipeline.transform(converted_data))


if __name__ == "__main__":
    app.run()
