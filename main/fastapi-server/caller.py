import argparse

import pandas as pd
import requests
import json

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--address", type=str, default="127.0.0.1", nargs="?")
parser.add_argument("--port", type=int, default=8000, nargs="?")
parser.add_argument("--path", type=str, default="predict", nargs="?")
args = parser.parse_args()

# Create the base url where we expect the API
base_url = f"{args.address}:{args.port}"

# Read a few records from the dataset
dataset = pd.read_csv("main/training/iris.csv")
dataset.columns = [col.replace(".", "_") for col in dataset.columns]
dataset.index = dataset.index - 5

text = "{" + f'"data": {dataset.drop("Species", axis=1).iloc[:2, :].to_json()}' + "}"
# text = json.dumps({"data": {
#     "Sepal_Length": [5.1, 4.9],
#     "Sepal_Width": [3.5, 3.0],
#     "Petal_Length": [1.4, 1.4],
#     "Petal_Width": [0.2, 0.2]
# }})

# Call the API
print(f"Connecting to {base_url}...")
response = requests.post(f"http://{base_url}/{args.path}/", data=text)
print(f"Response: {response.text}")
