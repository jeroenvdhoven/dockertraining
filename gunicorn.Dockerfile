FROM python:3.7-slim-buster
WORKDIR server

# Install gunicorn
RUN pip install --no-cache-dir gunicorn

# Setup python env
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all server and pipeline files
COPY . .

# Set gunicorn configuration
ENV FLASK_APP=server.py host=0.0.0.0
EXPOSE 5000

CMD [ "bash", "./gunicorn_start.sh"]