import os

import joblib
import pandas as pd
from fastapi import FastAPI
from typing import Dict, Iterable, List
from pydantic import create_model, BaseModel

from main import output_folders, model_file

# Start an application
app = FastAPI()

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


class Column(BaseModel):
    pass


class Item(BaseModel):
    name: List[str]
    description: str = None


class DataFrame(BaseModel):
    data: Dict[str, Iterable]

    def to_df(self):
        return pd.DataFrame(self.data)


# Make an endpoint that accepts one variable `data` as input
@app.post('/predict/')
async def predict(data: DataFrame) -> str:
    return str(pipeline.transform(data.to_df()))


@app.post('/test/')
async def predict(data: DataFrame) -> str:
    return str(pipeline.transform(data.to_df()))
