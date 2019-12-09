# Docker training

    1. Setup
    2. Train a model
    3. Turn your model into an API using Flask
    4. Transfer to docker image
    5. Run Flask using a WSGI server
    6. Create a docker-compose.yml configuration 
    7. Run docker image on remote machine
    
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
`main/server/static` called `pipeline`. Alternaltively, you can run the `train.sh` script from the top directory of 
this project.

## Turn your model into an API using Flask
Flask is a tool that allows you to make python backends. It can thus also be used to host machine learning models.
For a good intro how Flask works, check https://flask.palletsprojects.com/en/1.1.x/quickstart/.

The goals is to make a Flask server that hosts the model you just created. To this end, create
a file in the `main/server` folder called `server.py`. This will contain the Python code to
create the Flask server. The model has already been placed in such a way that your server code
should be able to access it.

Use the example provided in the link above as a starting template. 
When you are done, you can use the `flask run` command inside the `main/server` folder to
start the server as follows. Try this out with the example found at the flask website first to see if it works.
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

Finally, use `flask run --host 127.0.0.1` from inside the `main/server` folder to start your server.
You can use the `caller.py` file to test your API. I'd recommend making a small bash script that
starts the server for you. This will come in handy later as well.

## Transfer to docker image
Docker is a platform to make lightweight, standalone applications (containers / images). These run on the 
OS of the machine Docker runs on, but can have their own versions of programs installed.
This means that docker containers can easily be transported between servers, since the correct
version of used tools and libraries are bundled in the container. This makes it easier
to scale and port applications. 
 
As data scientists we can use containers for instance as a dedicated python container,
 a Unix container on Windows machines (though this is basically a VM, not a container),
 or for deploying machine learning models & pipelines.

For this part you might want to take a look at https://docs.docker.com/engine/reference/commandline/cli/.
Especially look at the following `docker ...` commands:
- images
- build
- run
- ps
- stop
- rm
- rmi
- save
- load

In this section we will work mainly with Dockerfiles (https://docs.docker.com/engine/reference/builder/).
Dockerfiles are effectively scripts for making new Docker containers from existing containers.
They provide reproducible ways of making Docker containers, making them very useful for
deployment purposes. We will make a Flask container to serve your model. Make sure you read the
page on Dockerfiles above before continuing.

As a base image you can use one of the `python:3.7` containers. Make sure your Dockerfile
installs the right python packages on the container, as well as copying your Flask code and model.
Finally, it should open the right ports on the container and start the Flask server. You
can build your image using the `docker build` command.

Note: Docker caches builds at each line of execution. If you build a previously build image,
it will try to use the cache as much as possible until it finds a new command or it has
to use a new version of a file you created. All stages afterwards will be rerun. This is
especially relevant when it comes to installing libraries, since this takes a while. It can
be very useful to install your libraries early on in your Dockerfile to speed up development. 

Note 2: Your container operates basically behind its own firewall. The default Flask address of 
`127.0.0.1` is not available to your machine this way. Set the host of Flask to `0.0.0.0` to
make sure you can call it from your machine. This makes it accessible to the outside, so make sure you do not
run the Flask server like this on your own machine (since 'outside' will mean the internet).

Note 3: Take a look at `.dockerignore`. The `venv` folder is listed there. Anything listed in that file will not be
send to the Docker build context. This can make your build commands run considerably faster, as well as prevent you
from creating Docker images that are too large (by accident).

Once you have that up and running, you can try it out! Run you container using `docker run`
and check if you can call your model using `caller.py`. Don't forget the `-p` flag when using `run`
Once you got your first call working, try to think of how you can make your container smaller
(run `docker images`) and faster to build. Check for instance the container sizes of
`docker pull python:3.7` and `docker pull python:3.7-slim-buster`

## Run Flask using a WSGI server
You may have noticed the warning printed by Flask:
```
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
```
Basically, the default server Flask provides is simple and works, but can't handle a production
situation well. For more details, see https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment
Webserver frameworks implementing the WSGI standard will be better options for hosting
production loads than the development server provided by Flask. Here we will use one of
those servers to host our Flask application. We will use `gunicorn`. Why? It was at the 
top of the list in the Deployment - Standalone Services section. Perfect reason, right?

Gunicorn is a python package, so you can look up the documentation (https://gunicorn.org/) as well as
look at the example in https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/
to figure out how to change your Dockerfile for the Flask server to fit a Gunicorn hosted
app. Once you have build your container, test it again using the `caller.py` script.

## Create a docker-compose.yml configuration
Now you've build up some experience with the `docker` command, you may have noticed that it becomes annoying to save
the exact command you're using to build images and start / stop containers. You may have already created a small bash
script to simplify this process. However, there is another way: `docker-compose`.

Docker-compose allows you to specify how multiple images together form one application. For instance, you can define
a webserver image and a database image in one configuration so these can easily interface with each other. Furthermore,
it greatly simplifies your building and deployment cycle. We only have 1 image in our application, but it can still help
simplify our workflow. Take a look at the following commands in the documentation (https://docs.docker.com/compose/):

- up: build (if needed) and start a service using a `docker-compose.yml` file
- down: shut down and remove a service using a `docker-compose.yml` file 

Try to create your own `docker-compose.yml` file for your gunicorn server. Make sure you:
 
- open the right ports
- set the right build context
- reference the right dockerfile
- Include the `image` option to name your image

It is worth noting that `docker-compose up` and `docker-compose down` only work from the same directory where 
`docker-compose.yml` is located.

## Run docker image on remote machine
Now, to actually put the container in production! Start a t2-medium server on AWS (use the amazon linux image) and make
sure you have SSH access (set the security group). Save your docker container using
`docker save` and copy it to your machine. `scp` should do the trick here.

SSH into your created machine, install docker using `sudo yum install -y docker`, and start the
service using `sudo service docker start`. Load your image using `docker load`, and finally
start your image using `docker run`. Don't forget to set the `-p` option and to make sure
the firewall allows you to access the machine at port `5000`. Then test it with the `caller.py`
script (make sure you set the correct URL).

At this moment I'm still working on a way to deploy using `docker-compose.yml`