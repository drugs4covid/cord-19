# CORD-19 Analysis

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v3+-blue.svg)
![Python](https://img.shields.io/badge/python-v3+-blue.svg)
[![GitHub Issues](https://img.shields.io/github/issues/librairy/cord-19.svg)](https://github.com/librairy/cord-19/issues)
[![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Basic Overview
pre-processing of articles published in CORD-19 for indexing in a SOLR repository


## Quick Start

1. Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)
1. Clone this repo
	```
	git clone https://github.com/librairy/cord-19.git
	```
1. Move into the root folder
	```
	cd cord-19/
	```
1. Run the SOLR repository (the first time it may take a few minutes to download the Docker images)
    ````
    docker-compose up -d
    ````  
1. Create a virtual environment
    ```
    python -m venv custom-env
    ```
1. Activate the environment
    ```
    source custom-env/bin/activate
    ```
1. Install dependencies
    ```
    pip install -r requirements.txt
    ```
1. Download the latest [CORD-19](https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases.html) corpus : 
    ````
    wget -bcq 'https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/historical_releases/cord-19_2021-05-24.tar.gz'
    ````
1. Extract the tar.gz file:
    ````
    tar -zxvf cord-19_2021-05-24.tar.gz
    ````
1. Parse articles:
    ```
    python index.py ipg210105.xml
    ```  
1. Explore documents at: http://localhost:8983/solr

## Documents

Indexed documents have the following format:

	
## Statistics


| Strategy |  Sample | Precision |   Recall | F-Measure |
|----------|---------|-----------|----------|-----------|
|   Top1   |  1000   | 0.46      | 0.27     |   0.31    |
|   Top2   |  1000   | 0.33      | 0.62     |   0.39    |
|   Top3   |  1000   | 0.25      | 0.85     |   0.34    |
 