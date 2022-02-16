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
from random import random

if __name__ == '__main__':

    # Create a client instance. The timeout and authentication options are not required.
    server = 'http://localhost:8983/solr'
    if (len(sys.argv) == 2):
        server = sys.argv[1]
        print("remote solr: ",server)

    # Load articles
    #solr = pysolr.Solr(server+'/cord19-papers', always_commit=True, timeout=50)
    url = server+'/cord19-paragraphs'
    solr = pysolr.Solr(url, always_commit=True, timeout=120)
    print("reading paragraphs from:",url)

    #num_parallel = mp.cpu_count()
    num_parallel = 4
    print("Number of processors: ", num_parallel)
    pool = mp.Pool(num_parallel)

    t = time.time()
    finished = False
    page = 0
    size = 2
    total = -1
    max_size = -1
    while (not finished) and (total <= max_size):
        try:
            results = solr.search('*:*',rows=size,start=page,sort='id ASC')
            if (max_size < 0):
                max_size = results.hits
            num_found = len(results)
            next_cursor = results.nextCursorMark
            print("[",datetime.now(),"]","Page:",page,"Num_Found:", num_found,"Total:",total,"Hits:",max_size)
            finished = len(results) < size
            page += 1
            documents = []
            for doc in results:
                total += 1
                documents.append(doc)
            #print("[",datetime.now(),"]",total,"paragraphs: annotating the latest",size)
            paragraphs = pool.map(annotators.parse,documents)
            solr.add(paragraphs)
        except Exception as e:
            print("Error reading from solr:",e)
            delay_in_secs = random()*100
            print("waiting for ", delay_in_secs, " secs ..")
            time.sleep(delay_in_secs)
    print('Time to annotate paragraphs: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Annotations:",counter)
