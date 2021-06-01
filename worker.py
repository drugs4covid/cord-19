#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday June 1 12:52:05 2021

@author: cbadenes
"""
import json
import hashlib
#import scispacy
#import spacy
#import stanza
#import sys

#stanza.download('en', package='mimic', processors={'ner': 'bc5cdr'})
#stanza_nlp = stanza.Pipeline('en', package='mimic', processors={'ner': 'bc5cdr'})

#spacy_nlp  = spacy.load("en_core_sci_scibert")


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
              paragraph['text_t']=body['text']
              paragraph['id']=hashlib.md5(body['text'].encode('utf-8')).hexdigest()
              paragraph['section_s']=body['section']
              paragraph['article_id_s']=data['paper_id']
              paragraph['size_i']=len(body['text'])
              
              #scispacy
              #sci_doc = spacy_nlp(body['text'])
              #paragraph['scispacy_entities']=sci_doc.ents
              
              #stanza
              #stanza_doc = stanza_nlp(body['text'])
              #paragraph['stanza_entities']=[entity.text for entity in stanza_doc.entities]
              
              paragraphs.append(paragraph)
        
          result['paragraphs']=paragraphs           
          
    except AttributeError as e:
        print("Missing attribute:",e)
        
    return result





