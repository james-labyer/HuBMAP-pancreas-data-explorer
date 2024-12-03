# HuBMAP Pancreas Data Explorer

This site visualizes pancreas data collected as part of the HuBMAP project, which aims to collect cell-level data for every organ in the human body.

## Prerequisites
Docker/ Docker Compose

## Getting Started with development
1. Clone this repo

   ```
   git clone https://github.com/james-labyer/HuBMAP-pancreas-data-explorer.git
   ```

2. Some of the files in this project are too large to check into GitHub. The GitHub repo includes representative examples that use smaller files. If you want to view the larger files, download them and move them into the appropriate subfolders in:

   ```
   app/assets/optical-clearing-czi
   ```

3. Build the image

   ```
   cd app
   docker compose -f docker-compose-dev.yaml build
   ```

4. Run the image

   ```
   docker compose -f docker-compose-dev.yaml up
   ```

   Running the image starts the app at localhost:8050. Hot reloading within the Docker container does not work currently, but since the dev image uses a mount, you can see the changes by starting and stopping the container without rebuilding it.


## Running tests locally
Run pytest within a development container:
```
docker exec {container_name} pytest --cov-report term-missing --cov
```

## Setting up production for the first time
1. Log into the server and clone this repo.

   ```
   git clone https://github.com/james-labyer/HuBMAP-pancreas-data-explorer.git
   ```

2. Use `scripts/move.sh` to migrate large files into production. You will first need to edit `move.sh` to include the correct values for file source, file destination, and key.


3. Build the image

   ```
   docker compose -f docker-compose.yaml build
   ```

4. Run the image

   ```
   docker compose -f docker-compose.yaml up
   ```


## Generating PNG file to display optical clearing data
Follow the instructions in `scripts/convert-czi-to-png.ijm` to convert .czi files to a series of .png files for display on the site.