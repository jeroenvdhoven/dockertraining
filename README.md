# Docker training

    1. Setup
    2. Train a model
    3. Turn your model into a REST api using Flask
    4. Transfer to docker image
    5. Run docker image on remote machine
    6. Running Flask using a WSGI service

At any moment can you check out the `solutions` branch to see how you can solve the problem at hand.
`git stash` and `git stash pop` can be useful to store your work in-between switching to and from the `solutions` branch


## Setup
First, install docker: https://docs.docker.com/docker-for-mac/install/.
Second, use the provide `requirements.txt` to generate a compatible virtual environment.
```
pip install virtualenv
virtualenv ./venv/server
source venv/server/bin/activate
pip install -r requirements.txt
```

Also make sure you create your own branch based on the `master` branch before continuing with
this training.

## Train a model

The provided `main/training` folder contains all the files you need to train the full prediction
pipeline used in this training. Inspect the file so you understand what it doen. Run `trainer.py` and make sure there's a file in 
`main/server/static` called `pipeline`. 

## Turn your model into a REST api using Flask
Flask is a tool that allows you to make python backends. It can thus also be used to host machine learning models.
For a good intro how Flask works, check https://flask.palletsprojects.com/en/1.1.x/quickstart/.

The goals is to make a Flask server that hosts the model you just created. To this end, create
a file in the `main/server` folder called `server.py`. This will contain the Python code to
create the Flask server. The model has already been placed in such a way that your server code
should be able to access it.

Use the example provided in the link above as a starting template. 
When you are done, you can use the `flask run` command inside the `main/server` folder to
start the server as follows. Try this out with the example first to see if it works.
```
export FLASK_APP=server.py
flask run --host 127.0.0.1
```

If you navigate to `127.0.0.1:5000` in your browser, you should see a Hello World message. 
Once you have completed this, you can start working on making sure that Flask hosts your model.
To do this, you will need to do a few things:

- Load your model in the server.
- Be able to read in data from a request.
- Send the result back as a string.

First, you can notice from the `training.py` file that our full pipeline is stored using `joblib`
This library can also be used to load a pipeline from a file using `joblib.load`.

One way of sending data in a request is to transform it to JSON. Pandas has some convenient methods
for transforming DataFrames to and from JSON. `pd.read_json` will turn a string containing JSON into
a DataFrame if possible, while `DataFrame.to_json()` will do the opposite. You can use these methods
to send data to Flask. You can check https://flask.palletsprojects.com/en/1.1.x/quickstart/#variable-rules
to see how Flask can accept incoming variables and hand them to your functions.


    1. Flask
    2. Teach about REST
    3. Make a Flask server to host your model
    4. Run it locally to test it
4. Transfer to docker image
    1. Run:
        1. docker pull python:3.7
        2. docker pull python:3.7-slim-buster
    2. Best practices
    3. Create requirements.txt
    4. Creating a Dockerfile
        1. Starting from the right base image
        2. Install right python environment
        3. Copy the required files
        4. Launch API on starting image
        5. Think of how you can increase your build speed!
5. Run docker image locally
    1. Try it, test it!
6. Run docker image on remote machine
    1. Start AWS machine
    2. Try it, test it!
7. Now, do it properly with a WSGI machine
    1. Why use that type of machine?
    2. Which to use?
    3. Set it up in Docker
