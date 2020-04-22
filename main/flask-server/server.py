import os

import joblib
import pandas as pd
from flask import Flask

from main import output_folders, model_file

# Start an application
app = Flask(__name__)

# Read the pipeline
model_file_detected = False
for output_folder in output_folders:
    target_file = os.path.join(output_folder, model_file)
    if os.path.isfile(target_file):
        model_file_detected = True
        break

if not model_file_detected:
    target_file = os.path.join("static", model_file)

pipeline = joblib.load(target_file)


# Make and endpoint that accepts one variable `data` as input
@app.route('/<string:data>')
def predict(data: str):
    converted_data = pd.read_json(data)
    return str(pipeline.transform(converted_data))


# Run the app only if this file is run.
if __name__ == "__main__":
    app.run()
