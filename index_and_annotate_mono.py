#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thuesday June 1 12:45:05 2021

@author: cbadenes
"""
import worker as workers
import pysolr
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

    solr_papers = pysolr.Solr(server+'/cord19-papers', always_commit=True, timeout=120)
    solr_paragraphs = pysolr.Solr(server+'/cord19-paragraphs', always_commit=True, timeout=120)

    window = 100
    num_papers = 0
    papers = []
    num_paragraphs = 0
    paragraphs = []
    for file in files:
        try:
            result = workers.parse_and_annotate(file)
            if ('paper' in result):
                papers.append(result['paper'])
                num_papers += 1
                if (len(papers) >= window):
                    print("[",datetime.now(),"] indexing papers: ", num_papers, "/", len(papers))
                    solr_papers.add(papers)
                    papers = []
            if ('paragraphs' in result):
                paragraphs.extend(result['paragraphs'])
                num_paragraphs += len(result['paragraphs'])
                if (len(paragraphs) >= window):
                    print("[",datetime.now(),"] indexing paragraphs: ", num_paragraphs,"/",len(paragraphs))
                    solr_paragraphs.add(paragraphs)
                    paragraphs = []
        except Exception as e:
            print("Error reading file:",file, " => ",e)

    print("[",datetime.now(),"] indexing last papers: ", num_papers, "/", len(papers))
    solr_papers.add(papers)
    print("[",datetime.now(),"] indexing last paragraphs: ", num_paragraphs,"/",len(paragraphs))
    solr_paragraphs.add(paragraphs)
    print('Time to parse articles: {} mins'.format(round((time.time() - t) / 60, 2)))
    print("Total Articles:",num_papers)
    print("Total Paragraphs:",num_paragraphs)
