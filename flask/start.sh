#!/bin/bash

# Default host will work well for testing without Docker.
# However, use 0.0.0.0 with Docker. 127.0.0.1 is not open to the world,
# which means you will not be able to access it on the Docker image from outside.
default_host="127.0.0.1"
host=${host:-$default_host}

echo $host

export FLASK_APP=server.py
cd main/flask-server && flask run -h $host