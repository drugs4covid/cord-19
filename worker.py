#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday June 1 12:52:05 2021

@author: cbadenes
"""
import json
import hashlib
import annotator as annotators

def parse(article):
    result = {}
    try:
      with open(article) as json_file:
          data = json.load(json_file)
          # load paper
          paper = {}
          paper['id'] = data['paper_id']
          metadata = data['metadata']
          paper['name_s'] = metadata['title']
          paper['url_s'] = "https://api.semanticscholar.org/v1/paper/" + data['paper_id']
          if (len(data['abstract'])>0):
              abstract_text = ""
              for abstract in data['abstract']:
                  abstract_text += abstract['text'] + " "
              paper['abstract_t'] = abstract_text
          result['paper'] = paper

          paragraphs = []
          # load paragraphs
          for body in data['body_text']:
              paragraph = {}
              txt = body['text']
              if (len(txt) > 0):
                  paragraph['text_t']=txt
                  paragraph['id']=hashlib.md5(body['text'].encode('utf-8')).hexdigest()
                  paragraph['section_s']=body['section']
                  paragraph['article_id_s']=data['paper_id']
                  paragraph['size_i']=len(body['text'])
                  paragraphs.append(paragraph)

          result['paragraphs']=paragraphs

    except Exception as e:
        print("Error parsing paragraph:",e)

    return result

def parse_and_annotate(article):
    result = {}
    try:
      with open(article) as json_file:
          data = json.load(json_file)
          # load paper
          paper = {}
          paper['id'] = data['paper_id']
          metadata = data['metadata']
          paper['name_s'] = metadata['title']
          paper['url_s'] = "https://api.semanticscholar.org/v1/paper/" + data['paper_id']
          if (len(data['abstract'])>0):
              abstract_text = ""
              for abstract in data['abstract']:
                  abstract_text += abstract['text'] + " "
              paper['abstract_t'] = abstract_text
          result['paper'] = paper

          paragraphs = []
          # load paragraphs
          for body in data['body_text']:
              paragraph = {}
              txt = body['text']
              if (len(txt) > 0):
                  paragraph['text_t']=txt
                  paragraph['id']=hashlib.md5(body['text'].encode('utf-8')).hexdigest()
                  paragraph['section_s']=body['section']
                  paragraph['article_id_s']=data['paper_id']
                  paragraph['size_i']=len(body['text'])
                  paragraphs.append(annotators.parse(paragraph))

          result['paragraphs']=paragraphs

    except Exception as e:
        print("Error parsing paragraph:",e)

    return result
