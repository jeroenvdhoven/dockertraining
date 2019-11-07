# Docker training

    1. Setup
    2. Train a model
    3. Turn your model into a REST api using Flask
    4. Transfer to docker image
    5. Run docker image on remote machine
    6. Running Flask using a WSGI service

1. Setup
First, install docker: https://docs.docker.com/docker-for-mac/install/
Second, use the provide `requirements.txt` to generate a compatible virtual environment.
```
pip install virtualenv
virtualenv ./venv/server
source venv/server/bin/activate
pip install -r requirements.txt
```

2. Train a model
The provided `main/training` folder contains all the files you need to train the full prediction
pipeline used in this training. Inspect the file so you understand what it doen. Run `trainer.py` and make sure there's a file in 
`main/server/static` called `pipeline`. 

3. Turn your model into a REST api using Flask
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
