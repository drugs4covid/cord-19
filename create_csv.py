#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thuesday June 1 12:45:05 2021

@author: cbadenes
"""
import time
import json
import sys
import os
import csv
from datetime import datetime

if __name__ == '__main__':

    if (len(sys.argv) != 2):
        print("usage: python index.py <input_directory>")
        sys.exit(2)
    directory        = sys.argv[1]


    # Load articles
    print("loading files from:",directory)
    files = [ os.path.join(directory, entry) for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))]
    total_files = len(files)
    print("[",datetime.now(),"] files available: ",total_files)

    csv_file = open('data.csv','w',encoding='UTF8', newline='')
    writer = csv.writer(csv_file)
    header = ['id', 'title', 'abstract']
    # write the header
    writer.writerow(header)

    min_papers = 0
    max_papers = total_files
    min_abstract_size = 10

    num_papers = 0
    for file in files[min_papers:max_papers]:
        try:
            with open(file) as json_file:
                data = json.load(json_file)
                id = data['paper_id']
                metadata = data['metadata']
                title = metadata['title']
                abstract_text = ""
                if (len(data['abstract'])>0):                    
                    for abstract in data['abstract']:
                        abstract_text += abstract['text'] + " "
                if (len(abstract_text) > min_abstract_size):
                    num_papers += 1
                    row = [id, title, abstract_text]
                    writer.writerow(row)
        except Exception as e:
            print("Error reading file:",file, " => ",e)

    csv_file.close()
    print("[",datetime.now(),"] Total Articles:",num_papers)
