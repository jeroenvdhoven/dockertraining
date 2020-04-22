FROM python:3.7-slim-buster
WORKDIR server

RUN pip install --no-cache-dir --upgrade pip

# Setup python env
COPY ./gunicorn/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all server and pipeline files
COPY ./main/flask-server/ ./main/flask-server/
COPY ./main/__init__.py ./main/__init__.py
COPY ./main/training/ ./main/training/
COPY ./gunicorn ./gunicorn


# Set gunicorn configuration
ENV FLASK_APP=server.py host=0.0.0.0
EXPOSE 5000

CMD ["./gunicorn/start.sh"]