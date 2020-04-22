FROM python:3.7-slim-buster
WORKDIR server

RUN pip install --no-cache-dir --upgrade pip

# Setup python env
COPY ./fastapi/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all server and pipeline files
COPY ./main/fastapi-server/ ./main/fastapi-server/
COPY ./main/__init__.py ./main/__init__.py
COPY ./main/training/ ./main/training/
COPY ./fastapi ./fastapi

# Set Flask configuration
ENV host=0.0.0.0
EXPOSE 8000

CMD ["./fastapi/start.sh"]