# HuBMAP Pancreas Data Explorer

This site visualizes pancreas data collected as part of the HuBMAP project, which aims to collect cell-level data for every organ in the human body.

## Prerequisites
Docker/ Docker Compose

## Getting Started with development
1. Clone this repo
```
git clone https://github.com/james-labyer/HuBMAP-pancreas-data-explorer.git
```
2. Build the image
```
cd app
docker compose -f docker-compose-dev.yaml build
```
3. Run the image
```
docker compose -f docker-compose-dev.yaml up
```
Running the image starts the app at localhost:8050. Hot reloading within the Docker container does not work currently, but since the dev image uses a mount, you can see the changes by starting and stopping the container without rebuilding it.

## Running tests locally
Run pytest within a development container:
```
docker exec {container_name} pytest --cov=app tests
```

## Preparing the production image
1. Log into the server and clone this repo
```
git clone https://github.com/james-labyer/HuBMAP-pancreas-data-explorer.git
```
2. Build the image
```
docker compose -f docker-compose.yaml build
```
3. Run the image
```
docker compose -f docker-compose.yaml up
```
