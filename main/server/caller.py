import argparse

import pandas as pd
import requests

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--address", type=str, default="127.0.0.1", nargs="?")
parser.add_argument("--port", type=int, default=5000, nargs="?")
parser.add_argument("--model", type=str, default="pipeline", nargs="?")
args = parser.parse_args()

# Create the base url where we expect the API
base_url = f"{args.address}:{args.port}"

# Read a few records from the dataset
dataset = pd.read_csv("main/training/iris.csv")
text = dataset.drop("Species", axis=1).iloc[:2].to_json()

# Call the API
print(f"Connecting to {base_url}...")
url = f"http://{base_url}/{args.model}/{text}"
response = requests.get(url)
print(f"Response: {response.text}")
