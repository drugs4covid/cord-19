#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wednesday February 9 09:45:05 2021

@author: cbadenes
"""
import annotator as annotators
import pysolr
import time
import sys
import requests
import multiprocessing as mp
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

    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())

    t = time.time()
    documents = []
    counter = 0
    for doc in solr.search('*:*',sort='id ASC',cursorMark='*'):
        counter += 1
        documents.append(doc)
        if (len(documents) == 100):
            print("[",datetime.now(),"]",counter,"paragraphs: annotating 100")
            paragraphs = pool.map(annotators.parse,documents)
            solr.add(paragraphs)
            documents = []

    print('Time to annotate paragraphs: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Annotations:",counter)
