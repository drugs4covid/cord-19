#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thuesday June 1 12:45:05 2021

@author: cbadenes
"""
import time
import json
import gzip as gzip
import sys
import os
from datetime import datetime

if __name__ == '__main__':

    if (len(sys.argv) != 2):
        print("usage: python index.py <input_directory>")
        sys.exit(2)
    directory        = sys.argv[1]


    # Load articles
    print("loading files from:",directory)
    articles = [ os.path.join(directory, entry) for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
    total_articles = len(articles)
    print("[",datetime.now(),"] files available: ",total_articles)

    num_articles_per_file = 10000
    print("[",datetime.now(),"] articles per file: ",num_articles_per_file)

    num_files = total_articles // num_articles_per_file
    print("[",datetime.now(),"] num files: ",num_files)
    

    file = gzip.open('data-0.json.gz','wb')


    total = 1
    counter = 1
    for article in articles:
        if (total % num_articles_per_file == 0 ):
            file.close()
            print("[",datetime.now(),"] created file:",file.name)
            file = gzip.open('data-'+str(counter)+'.json.gz','wb')
            counter += 1
        total += 1
        try:
            with open(article, 'r') as json_file:
                data = json.load(json_file)                
                out = json.dumps(data)
                file.write(out.encode())
                file.write('\n'.encode())
        except Exception as e:
            print("Error reading article:",article, " => ",e)   
            break     

    file.close()
    print("[",datetime.now(),"] created file:",file.name)
    print("[",datetime.now(),"] Total Articles:",total)
