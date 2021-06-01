# CORD-19 Analysis

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/docker-v3+-blue.svg)
![Python](https://img.shields.io/badge/python-v3+-blue.svg)
[![GitHub Issues](https://img.shields.io/github/issues/librairy/cord-19.svg)](https://github.com/librairy/cord-19/issues)
[![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Basic Overview
pre-processing of articles published in the [CORD-19](https://github.com/allenai/cord19) corpora to be indexed in a SOLR repository


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
1. Parse articles from a directory:
    ```
    python index.py 2021-05-24/document\_parses/pdf_json
    ```  
1. Explore documents at: http://localhost:8983/solr

## Papers

Papers are described by SOLR documents with the following format:

````json
{
	"id": "f905f78b32f63c6d14a79984dfb33f1b358b8ab4",
	"name_s": "Multimerization of HIV-1 integrase hinges on conserved SH3-docking platforms",
	"url_s": "https://api.semanticscholar.org/v1/paper/f905f78b32f63c6d14a79984dfb33f1b358b8ab4",
	"abstract_t": "New anti-AIDS treatments must be continually developed in order to overcome resistance mutations including those emerging in the newest therapeutic target, the viral integrase (IN). Multimerization of IN is functionally imperative and provides a forthcoming therapeutic target. Allosteric inhibitors of IN bind to non-catalytic sites and prevent correct multimerization not only restricting viral integration but also the assembly and maturation of viral particles. Here, we report an allosteric inhibitor peptide targeting an unexploited SH3-docking platform of retroviral IN. The crystal structure of the peptide in complex with the HIV-1 IN core domain reveals a steric interference that would inhibit conserved docking of SH3-containing domain with the core domain vital for IN multimerization, providing a template for the development of novel anti-IN allosteric inhibitors. ",
	"_version_": 1701368637485481984
}
````
	
## Paragraphs	
Paragraphs are described by documents with the following format:

````json
{
	"id": "796a12340c8483934a02f0b00d8cb4d6",
	"article_id_s": "f905f78b32f63c6d14a79984dfb33f1b358b8ab4",
	"size_i": 1282,
	"text_t": "In the absence of a curative treatment, the highly active antiretroviral therapy (HAART) keeps the HIV-1 virus of AIDS patients under control. HAART combines drugs targeting different stages of viral replication including the integration step catalyzed by the integrase protein (IN) (1) . Integration of viral DNA into host genome involves two steps catalyzed by IN: (i) cleavage of a dinucleotide from each 3'-end of the viral DNA (3'processing), and (ii) insertion of this processed viral DNA into the host DNA (strand-transfer) (2) . Clinical IN strand transfer inhibitors (INSTIs) target the catalytic site of the enzyme to specifically inhibit the DNA joining reaction, however, as with all anti-AIDS treatments, the continued success of these drugs is persistently disrupted by resistance mutations (1, 2) . Although 3'-processing can be carried out by monomeric IN (3) , the assembly of IN functional multimers is imperative for the strand-transfer activity (4) (5) (6) (7) (8) , and for virus particle maturation and production (reviewed in (9, 10) ). In the continued quest to identify and develop new drugs, allosteric inhibitors that bind sites outside the catalytic core and disrupt IN multimerization are emerging with potent therapeutic potential (11) (12) (13) (14) .",
	"_version_": 1701368637733994496
}
````