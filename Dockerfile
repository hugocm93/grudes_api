FROM python:3.11-slim-bookworm as base
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5001

FROM base as prod
COPY . . 
ENTRYPOINT ./run.sh

FROM base as dev
ENTRYPOINT ./run.sh debug 

FROM base as test
ENTRYPOINT ./run.sh test 
