FROM python:3.7-slim-buster
WORKDIR server

# Setup python env
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all server and pipeline files
COPY . .

# Set Flask configuration
ENV FLASK_APP=server.py host=0.0.0.0
EXPOSE 5000

CMD ["./flask_start.sh"]