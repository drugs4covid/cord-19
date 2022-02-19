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
from datetime import datetime

if __name__ == '__main__':

    # Create a client instance. The timeout and authentication options are not required.
    server = 'http://localhost:8983/solr'


    if (len(sys.argv) != 2):
        print("usage: python index.py <input_directory>")
        sys.exit(2)
    directory        = sys.argv[1]


    # Load articles
    print("loading files from:",directory)
    files = [ os.path.join(directory, entry) for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
    total_files = len(files)
    print(total_files,"files available")

    num_parallel = 10
    print("Number of processors: ", num_parallel)
    pool = mp.Pool(num_parallel)

    increment = 100
    min_idx = 0
    max_idx = min_idx + increment
    t = time.time()
    count_papers = 0
    count_paragraphs = 0
    while(min_idx<total_files):
        try:
            solr_papers = pysolr.Solr(server+'/cord19-papers', always_commit=True, timeout=120)
            solr_paragraphs = pysolr.Solr(server+'/cord19-paragraphs', always_commit=True, timeout=120)
            print("[",datetime.now(),"]","indexing articles between:",min_idx,"-",max_idx)
            results = pool.map(workers.parse_and_annotate,files[min_idx:max_idx] )
            papers = []
            paragraphs = []
            for result in results:
                if ('paper' in result):
                    papers.append(result['paper'])
                    num_papers = len(papers)
                    if (num_papers >= 100):
                        print("saving", num_papers, "papers..")
                        solr_papers.add(papers)
                        papers = []
                if ('paragraphs' in result):
                    paragraphs.extend(result['paragraphs'])
                    num_paragraphs = len(paragraphs)
                    if (num_paragraphs >= 100):
                        print("saving", num_paragraphs, "paragraphs..")
                        solr_paragraphs.add(paragraphs)
                        paragraphs = []
            if (len(papers) > 0):
                print("saving the rest of",len(papers),"papers..")
                solr_papers.add(papers)
            if (len(paragraphs) > 0):
                print("saving the rest of",len(paragraphs),"paragraphs..")
                solr_paragraphs.add(paragraphs)
            min_idx = max_idx
            max_idx = min_idx + increment
            solr_papers.get_session().close()
            solr_paragraphs.get_session().close()
        except Exception as e:
            print("Error reading from solr:",e)


    pool.close()
    print('Time to parse articles: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Articles:",count_papers)
    print("Total Paragraphs:",count_paragraphs)
