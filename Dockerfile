FROM python:3.11-slim-bookworm as base
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5001

FROM base as prod
COPY . . 
ENTRYPOINT flask run --host 0.0.0.0 --port 5001

FROM base as dev
ENTRYPOINT flask run --host 0.0.0.0 --port 5001 --reload 
