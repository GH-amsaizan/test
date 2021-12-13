# Slim build of python
FROM python:3.8-slim

WORKDIR /app

# Copy repository root to the app directory
COPY . /app

# Install requirements 
RUN apt-get update && apt-get install -y build-essential
RUN pip install -e . && pip install pytest

CMD [ "bash" ]