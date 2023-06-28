# TueSearch

This project contains the source code of the final project from the course modern search engines at the University of
Tübingen.

## Table of Contents

- [TueSearch](#tuesearch)
    - [Table of Contents](#table-of-contents)
- [Project Structure](#project-structure)
- [Crawler](#crawler)
    - [Crawler set up](#crawler-set-up)
    - [Crawler usage](#crawler-usage)
    - [Crawler cheatsheet](#crawler-cheatsheet)
        - [Show directories' content](#show-directories-content)
        - [Show logs](#show-logs)
- [Backend](#backend)
    - [Backend set up](#backend-set-up)
    - [Backend usage](#backend-usage)
    - [Backend cheatsheet](#backend-cheatsheet)
        - [Test the API](#test-the-api)
- [Frontend](#frontend)
- [Docker](#docker)
    - [Docker set up](#docker-set-up)
    - [Docker usage](#docker-usage)
    - [Docker cheatsheet](#docker-cheatsheet)
        - [Show containers](#show-containers)
        - [Show logs](#show-logs-1)
        - [Enter containers](#enter-containers)
        - [Restart the services](#restart-the-services)
- [Clean up everything](#clean-up-everything)
- [Team Members](#team-members)

# Project Structure

The project has the following structure:

- `.github`: This directory contains the GitHub workflow files for the project.
- `backend`: This directory contains the Flask application for the search engine.
    - `app.py`: This script contains the Flask API for the search engine.
    - `build_inverted_index.py`: The script for building the inverted index from the crawled documents.
    - `build_ranker.py`: The script for building the ranker from the inverted index and query.
    - `rank.py`: This module contains the ranker class, which uses the built ranker to rank the documents based on the
      query.
    - `streamers.py`: This module contains the streamers class, which is used to stream the documents from the database
      to the ranker.
- `crawler`: This directory contains the main source code of the web crawler.
    - `data`: This directory contains the data files for the project.
        - `serp.json`: This file contains the search engine results page (SERP) for the query "Tübingen".
        - `documents.json`: This file contains some initial crawled documents so local development gets a bit easier.
    - `models`: SQL models for the database.
        - `base.py`: This file contains the base model for the database.
        - `document.py`: This file contains the model for the documents table.
        - `job.py`: This file contains the model for the jobs table.
    - `relevance_classification`: Classify URL's, document's and job's relevance.
        - `document_relevance.py`: Determines if a document should be indexed.
        - `job_relevance.py`: Determines if a job should be executed.
        - `url_relevance.py`: Determines if a URL should be crawled and when it should be crawled.
    - `tests`: This directory contains the test files for the project. (Note: The test directory could be improved
      further to include more comprehensive testing scenarios and coverage.)
    - `utils`:
        - `io`: This module contains the functions for reading and writing data to files.
        - `log`: This module contains the functions for logging the crawling process.
        - `text`: Contains the function to preprocess text before feed it to ranker and classifier.
    - `crawl.py`: Determine a crawler. A crawler is a single process that crawls a single URL.
    - `fetch_serp.py`: The script for fetching the search engine results page (SERP) and saving it as a JSON file.
    - `initialize_database.py`: The script for initializing the database and creating the necessary tables and add
      initial data.
    - `main.py`: Start the crawler.
    - `priority_queue.py`: Contains the priority queue class, which is used to determine which server and which link is
      preferred.
- `docker`: This directory contains the docker files for the project.
    - `my.cnf`: This file contains the configuration for the MySQL database.
    - `mysql.cnf`: This file contains the configuration for the MySQL database.
    - `python.Dockerfile`: This file contains the Dockerfile for the Python crawler & backend.
- `.pre-commit-config.yaml`: This file contains the configuration for the pre-commit hooks.
- `.pylintrc`: This file contains the configuration for the pylint linter.
- `CODEOWNERS`. This file contains the GitHub code owners for the project.
- `docker-compose.yml`: Configuration for docker-compose for local development and deployment.
- `example.env`: This file contains the example environment variables for the project.
- `example.mysql.env`: This file is specifically for the MySQL's instance in the docker-compose file.
- `package.json`: This file contains the required dependencies for the project's frontend.
- `python.Dockerfile`: This file contains the Dockerfile for the Python crawler & backend.
- `requirements.dev.txt`: This file contains the required dependencies for the project's crawler & backend at local.
- `requirements.prod.txt`: This file contains the required dependencies for the project's crawler & backend at
  production. Should contain fewer dependencies.

# Crawler

## Crawler set up

The following set up was tested under Ubuntu 22.04. LTS and Windows WSL2 (although the WSL seems to
have some performance issues).

1. Create output directories and initialize environment variables

```bash
bash scripts/init.sh
```

2. Start MySQL database

```bash
docker-compose up -d --build mysql
```

3. Start the migration scripts to create the database tables.

```bash
python3 -m scripts.migration
```

## Crawler usage

To use the web crawler, follow the workflow below:

1. (Optional) If you want new SERP, delete the `crawler/data/serp.json` file, fetch a new search engine results page (
   SERP) using the `crawler/fetch_serp.py` script.

```bash
python3 -m crawler.fetch_serp
```

2. Run the `crawler/initialize_database.py` script. This script sets up the database
   and creates the necessary tables for storing crawled documents and job management.

```bash
python3 -m crawler.initialize_database
```

3. Once you have the initialized database, you can start the crawling process using the `crawler/main.py` script.

```bash
python3 -m crawler.main -n 10 # Crawl 10 items
```

or simply

```bash
python3 -m crawler.main # Craw in loop
```

## Crawler cheatsheet

### Show directories' content

```bash
ls -lha /opt/tuesearch/data/
```

```bash
ls -lha /opt/tuesearch/log/
```

# Backend

## Backend set up

Same as described in the section [Crawler](#crawler).

## Backend usage

1. After crawling, you can build the inverted index using the `backend/build_inverted_index.py` script. This script
   analyzes
   the crawled documents and constructs an inverted index to enable efficient searching.

```bash
python3 -m backend.build_inverted_index
```

This step should be repeated regularly to keep the index fresh.

2. Build the ranker using the `backend/build_ranker.py` script.
   This script builds the models needed to rank websites. After training, the model
   will be stored in paths defined in the `.env` file.

```bash
python3 -m backend.build_ranker
```

This step should be repeated regularly to keep the ranker fresh.

3. You can run the Flask application to search for documents using the `backend/app.py` script.

```bash
python3 -m backend.app
```

## Backend cheatsheet

### Test the API

```bash
curl http://localhost:5000/search?q=tübingen
```

# Frontend

1. Install dependencies

```bash
npm install
```

2. Start the frontend

```bash
npm run dev
```

3. Open the browser at `http://localhost:4000/`

# Docker

## Docker set up

Same as described in the section [Crawler](#crawler). Try this command if you have permission issues:

```bash
bash scripts/init.sh
```

## Docker usage

1. Start the services

```bash
docker-compose up -d --build
```

and wait at first time about 60 seconds for the crawler to fill the database.

2. If everything successes then

```bash
docker container ps
```

should show only 2 containers running, `mysql` and `backend_server`.

3. Test the API with

```bash
curl http://localhost:5001/search?q=tübingen
```

Note that port of the container's backend is not the same as
the port of the host's backend.

## Docker cheatsheet

### Show containers

```bash
docker container ps
```

### Run only one service

```bash
docker-compose up initialize_database
```

```bash
docker-compose up crawl
```

```bash
docker-compose up build_inverted_index
```

```bash
docker-compose up build_ranker
```

### Show logs

```bash
docker container logs mysql
```

```bash
docker container logs initialize_database
```

```bash
docker container logs crawl
```

```bash
docker container logs build_inverted_index
```

```bash
docker container logs build_ranker
```

```bash
docker container logs backend_server
```

### Enter containers

```bash
docker exec -it mysql bash
```

```bash
docker exec -it initialize_database bash
```

```bash
docker exec -it crawl bash
```

```bash
docker exec -it build_inverted_index bash
```

```bash
docker exec -it build_ranker bash
```

```bash
docker exec -it backend_server bash
```

### Restart the services

```bash
docker-compose down
docker-compose up -d --build
```

# Clean up everything

In case of unexplainable errors, try to clean up everything and start from scratch.

```bash
docker-compose down
docker system prune -a
docker volume prune --force
sudo rm -rf /opt/tuesearch
```

# Team Members

- [Daniel Reimer](https://github.com/Seskahin)
- [Long Nguyen](https://github.com/longpollehn)
- [Lukas Listl](https://github.com/LukasListl)
- [Philipp Alber](https://github.com/coolusaHD)
