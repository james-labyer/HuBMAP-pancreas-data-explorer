# HuBMAP Pancreas Data Explorer

This site visualizes pancreas data collected as part of the HuBMAP project, which aims to collect cell-level data for every organ in the human body.

## Prerequisites
Docker/ Docker Compose

## Getting Started with development
1. Clone this repo

   ```
   git clone https://github.com/james-labyer/HuBMAP-pancreas-data-explorer.git
   ```

2. Some of the files in this project are too large to check into GitHub. The GitHub repo includes representative examples that use smaller files. If you want to view the larger files, download them and move them into:

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

5. If you added larger files, generate the pages that rely on them

   ```
   exec -ti {container_name} bash
   ./prep/make-slicers.sh
   ```

   The files should end up in `app/pages/P114Aopticalclearing`.

## Running tests locally
Run pytest within a development container:
```
docker exec {container_name} pytest --cov-report term-missing --cov
```

## Running on production
1. Log into the server and clone this repo

   ```
   git clone https://github.com/james-labyer/HuBMAP-pancreas-data-explorer.git
   ```

2. If there are new large files that cannot be checked into GitHub, download them and move them into:

   ```
   app/assets/optical-clearing-czi
   ```

3. Build the image

   ```
   docker compose -f docker-compose.yaml build
   ```

4. Run the image

   ```
   docker compose -f docker-compose.yaml up
   ```
