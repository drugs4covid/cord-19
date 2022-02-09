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



if __name__ == '__main__':

    # Create a client instance. The timeout and authentication options are not required.
    server = 'http://localhost:8983/solr'
    if (len(sys.argv) == 2):
        server = sys.argv[1]
        print("remote solr: ",server)

    #solr = pysolr.Solr(server+'/cord19-papers', always_commit=True, timeout=50)
    url = server+'/cord19-paragraphs'
    solr = pysolr.Solr(url, always_commit=True, timeout=50)

    # Load articles
    print("reading paragraphs from:",url)

    t = time.time()
    count   = 0
    rows    = 1
    max     = 10
    #for doc in solr.search('*:*',fl='id',sort='id ASC',cursorMark='*'):
    for doc in solr.search('*:*',sort='id ASC',cursorMark='*'):
        count += 1
        if 'text_t' in doc:
            if 'annotated' in doc:
                continue
            print("annotating",doc['id'],"...")
        if (count >= max):
            break

    print('Time to parse articles: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Annotations:",count)
