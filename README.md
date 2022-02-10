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
    python index.py 2022-01-31/document\_parses/pdf_json
    ```
1. Annotate paragraphs using our [bio-ner](https://github.com/drugs4covid/bio-ner) service:
    ```
    python annotate.py
    ```		  
1. Explore documents at: http://localhost:8983/solr

## Fields

* `mesh_codes_ss`:
* `chemicals_ss`:
* `chemical_terms_ss`:
* `atc_codes_ss`:
* `atc_levels_ss`:
* `cid_codes_ss`:
* `doid_codes_ss`:
* `cui_codes_ss`:
* `icd10_codes_ss`:
* `icd9_codes_ss`:
* `gard_codes_ss`:
* `snomed_codes_ss`:
* `nci_codes_ss`:
* `ncbi_codes_ss`:
* `ncbi_taxonomy_ss`:
* `uniprot_codes_ss`:
* `diseases_ss`:
* `disease_terms_ss`:
* `disease_types_ss`:
* `covid_ss`:
* `covid_terms_ss`:
* `genetics_ss`:
* `genetic_terms_ss`:
* `genetic_types_ss`:


## Papers

Papers are described by SOLR documents with the following format:

````json
{
        "id":"83efd6b442d2b469ef297857e78774f1e47cf7a2",
        "name_s":"Mental ill-health during COVID-19 confinement",
        "url_s":"https://api.semanticscholar.org/v1/paper/83efd6b442d2b469ef297857e78774f1e47cf7a2",
        "abstract_t":"Background: Confinement due to COVID-19 has increased mental ill-health. Few studies unpack the risk and protective factors associated with mental ill-health and addictions that might inform future preparedness. Methods: Cross-sectional on-line survey with 37,810 Catalan residents aged 16+ years from 21 April to 20 May 2020 ... ",
        "_version_":1724302670685011971
}
````

## Paragraphs
Paragraphs are described by SOLR documents with the following format:

````json
{
        "text_t":"Large parts of the epidemiology and pathology of SARS were related to its receptor tropism in humans (3, 11, 16) . In a scenario resembling that for avian influenza viruses, the anatomical position of the receptor in the deep respiratory tract and the downregulation of its expression were postulated to aggravate the course of disease in individuals while limiting the spread of disease on the population level (24) . While we are still uncertain of the epidemiology of hCoV-EMC-related infections, the importance of knowing its receptor in human cells is unquestionable (11) . Our data taken together suggest that hCoV-EMC does not rely on the same receptor as SARS-CoV. Urgent further research is needed in order to identify the cellular receptor for hCoV-EMC and determine its anatomical focus of replication. Our observations regarding the cell culture tropism of this novel human virus raise an intriguing perspective. We have shown here that cells from primates, pigs, as well as bats representing four families from both chiropteran suborders, Yangochiroptera and Yinpterochiroptera, retain susceptibility for the virus. This breadth of tropism is absolutely unique among CoVs (1, 11, 12) . For instance, only once have researchers succeeded in culturing any CoV in bat-derived cells, and these experiments required specifically generated bat cell cultures combined with engineered, reporter gene-expressing virus (12) . The broad replicative capability of hCoV-EMC suggests that this new virus might utilize a receptor structure that bats, primates, and pigs have in common. If that receptor were expressed in mucosal surfaces in those hosts, repeated acquisition by humans would be conceivable, putting our current idea of a \"tight\" molecular barrier against coronaviral cross-host transmission into perspective (11, 12) . Interestingly, these data provide strong support for the existence of \"generalist\" CoV, as recently projected based on cell culture studies (12) .",
        "id":"00009f1f9b446a757fe38aba3ae2e87e",
        "article_id_s":"5650690daf962117b9831c42178ffd6a6a969300",
        "size_i":1979,
        "mesh_codes_ss":["D045169"],
        "doid_codes_ss":["2945"],
        "cui_codes_ss":["C1260415",
          "C1175175",
          "C1175175"],
        "icd10_codes_ss":["J12.81"],
        "icd9_codes_ss":["079.82"],
        "gard_codes_ss":["9237"],
        "snomed_codes_ss":["398447004"],
        "nci_codes_ss":["C85064"],
        "diseases_ss":["Pneumonia due to SARS-associated coronavirus",
          "Severe Acute Respiratory Syndrome"],
        "disease_terms_ss":["SARS",
          "SARS-CoV.",
          "coronaviral"],
        "disease_types_ss":["Disease or Syndrome",
          "Respiratory tract disease|Viral disease"],
        "_version_":1724386017599815681}
````
