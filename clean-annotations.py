#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wednesday February 9 09:45:05 2021

@author: cbadenes
"""
import pysolr
import time
import sys
import requests
from datetime import datetime

if __name__ == '__main__':

    # Create a client instance. The timeout and authentication options are not required.
    server = 'http://localhost:8983/solr'
    if (len(sys.argv) == 2):
        server = sys.argv[1]
        print("remote solr: ",server)

    # Load articles
    #solr = pysolr.Solr(server+'/cord19-papers', always_commit=True, timeout=50)
    url = server+'/cord19-paragraphs'
    solr = pysolr.Solr(url, always_commit=True, timeout=50)
    print("reading paragraphs from:",url)

    t = time.time()
    fields = ['mesh_codes','chemicals','chemical_terms','atc_codes','atc_levels','cid_codes','doid_codes','cui_codes','icd10_codes','icd9_codes','gard_codes','snomed_codes','nci_codes','ncbi_codes','ncbi_taxonomy','uniprot_codes','diseases','disease_terms','disease_types','covid','covid_terms','genetics','genetic_terms','genetic_types']
    documents = []
    counter = 0
    for doc in solr.search('*:*',sort='id ASC',cursorMark='*'):
        counter += 1
        for field in fields:
            if field in doc:
                doc.pop(field, None)
            if field+'_t' in doc:
                doc.pop(field+"_ss", None)
        doc.pop('_version_',None)
        documents.append(doc)
        if (len(documents) == 100):
            print("[",datetime.now(),"]",counter,"paragraphs cleaned")
            solr.add(documents)
            documents = []

    print('Time to annotate paragraphs: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Annotations:",counter)
