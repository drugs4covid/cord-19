#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday June 1 12:52:05 2021

@author: cbadenes
"""
import json
import hashlib
import annotation

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

                  annotation = Annotation(txt)
                  paragraph['mesh_codes']=[]
                  paragraph['chemicals']=[]
                  paragraph['chemicals_terms']=[]
                  paragraph['atc_codes']=[]
                  paragraph['atc_levels']=[]
                  paragraph['cid_codes']=[]
                  paragraph['doid_codes']=[]
                  paragraph['cui_codes']=[]
                  paragraph['icd10_codes']=[]
                  paragraph['icd9_codes']=[]
                  paragraph['gard_codes']=[]
                  paragraph['snomed_codes']=[]
                  paragraph['nci_codes']=[]
                  paragraph['ncbi_codes']=[]
                  paragraph['ncbi_taxonomy']=[]
                  paragraph['uniprot_codes']=[]
                  paragraph['diseases']=[]
                  paragraph['diseases_terms']=[]
                  paragraph['diseases_types']=[]
                  paragraph['covid']=[]
                  paragraph['covid_terms']=[]
                  paragraph['genetics']=[]
                  paragraph['genetics_terms']=[]
                  paragraph['genetics_types']=[]
                  if (annotation.has_chemicals()):
                      for chemical in annotation.get_chemicals():
                          if ('found_term' in chemical):
                              paragraph['chemicals'].append(chemical['found_term'])
                          if ('text_term' in chemical):
                              paragraph['chemicals_terms'].append(chemical['text_term'])
                          if ('ATC' in chemical):
                             paragraph['atc_codes'].append(chemical['ATC'])
                          if ('ATC_level' in chemical):
                             paragraph['atc_levels'].append(chemical['ATC_level'])
                          if ('cid' in chemical):
                             paragraph['cid_codes'].append(chemical['cid'])
                  if (annotation.has_diseases()):
                      for disease in annotation.get_diseases():
                          if ('found_term' in disease):
                             paragraph['diseases'].append(disease['found_term'])
                          if ('text_term' in disease):
                             paragraph['diseases_terms'].append(disease['text_term'])
                          if ('semantic_type' in disease):
                             paragraph['diseases_types'].append(disease['semantic_type'])
                          if ('cui' in disease):
                             paragraph['cui_codes'].extend(disease['cui'])
                          if ('mesh_id' in disease):
                             paragraph['mesh_codes'].append(disease['mesh_id'])
                          if ('cross_references' in disease):
                              for reference in disease['cross_references']:
                                  if (reference.startswith('ICD10CM')):
                                        paragraph['icd10_codes'].append(reference.split(":")[1])
                                  elif (reference.startswith('ICD9CM')):
                                        paragraph['icd9_codes'].append(reference.split(":")[1])
                                  elif (reference.startswith('SNOMEDCT')):
                                        paragraph['snomed_codes'].append(reference.split(":")[1])
                                  elif (reference.startswith('DOID')):
                                        paragraph['doid_codes'].append(reference.split(":")[1])
                                  elif (reference.startswith('NCI')):
                                        paragraph['nci_codes'].append(reference.split(":")[1])
                                  elif (reference.startswith('GARD')):
                                        paragraph['gard_codes'].append(reference.split(":")[1])
                  if (annotation.has_covid()):
                      for covid in annotation.get_covid():
                          if ('found_term' in covid):
                             paragraph['covid'].append(covid['found_term'])
                          if ('text_term' in covid):
                             paragraph['covid_terms'].append(covid['text_term'])
                  if (annotation.has_genetics()):
                      for genetic in annotation.get_genetics():
                          if ('found_term' in genetic):
                             paragraph['genetics'].append(genetic['found_term'])
                          if ('text_term' in genetic):
                             paragraph['genetics_terms'].append(genetic['text_term'])
                          if ('uniprot_id' in genetic):
                             paragraph['uniprot_codes'].extend(genetic['uniprot_id'])
                          if ('type' in genetic):
                             paragraph['genetics_types'].extend(genetic['type'])
                          if ('ncbi_gene_id' in genetic):
                             paragraph['ncbi_codes'].append(genetic['ncbi_gene_id'])
                          if ('ncbi_taxon_id' in genetic):
                             paragraph['ncbi_taxonomy'].append(genetic['ncbi_taxon_id'])

                  print(paragraph)
                  paragraphs.append(paragraph)

          result['paragraphs']=paragraphs

    except AttributeError as e:
        print("Missing attribute:",e)

    return result
