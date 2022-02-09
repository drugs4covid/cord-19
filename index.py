#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thuesday June 1 12:45:05 2021

@author: cbadenes
"""
import worker as workers
import pysolr
import multiprocessing as mp
import html
import time
import sys
import os

if __name__ == '__main__':

    # Create a client instance. The timeout and authentication options are not required.
    server = 'http://localhost:8983/solr'
    solr_papers = pysolr.Solr(server+'/cord19-papers', always_commit=True, timeout=50)
    solr_paragraphs = pysolr.Solr(server+'/cord19-paragraphs', always_commit=True, timeout=50)


    if (len(sys.argv) != 2):
        print("usage: python index.py <input_directory>")
        sys.exit(2)
    directory        = sys.argv[1]


    # Load articles
    print("loading files from:",directory)
    files = [ os.path.join(directory, entry) for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
    print(len(files),"files available")

    print("Number of processors: ", mp.cpu_count())
    pool = mp.Pool(mp.cpu_count())

    max_length = len(files)
    increment = 100
    min_idx = 0
    max_idx = increment
    t = time.time()
    count_papers = 0
    count_paragraphs = 0
    while(min_idx<max_length):
        print("indexing",max_idx,"articles..")
        results = pool.map(workers.parse,files[min_idx:max_idx] )
        min_idx = max_idx
        max_idx = min_idx + increment
        papers = []
        paragraphs = []
        for result in results:
            if ('paper' in result):
                papers.append(result['paper'])
            if ('paragraphs' in result):
                paragraphs.extend(result['paragraphs'])
        count_papers += len(papers)
        print("Papers added:",count_papers)
        solr_papers.add(papers)
        count_paragraphs += len(paragraphs)
        print("Paragraphs added:",count_paragraphs)
        solr_paragraphs.add(paragraphs)

    pool.close()
    print('Time to parse articles: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Articles:",count_papers)
    print("Total Paragraphs:",count_paragraphs)
