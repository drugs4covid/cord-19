#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday June 1 12:52:05 2021

@author: cbadenes
"""
import json
import hashlib
import annotation as an

def parse(paragraph):
    try:
      if ('text_t' in paragraph):
          txt = paragraph['text_t']
          annotation = an.Annotation(txt)
          paragraph['mesh_codes']=[]
          paragraph['chemicals']=[]
          paragraph['chemical_terms']=[]
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
          paragraph['disease_terms']=[]
          paragraph['disease_types']=[]
          paragraph['covid']=[]
          paragraph['covid_terms']=[]
          paragraph['genetics']=[]
          paragraph['genetic_terms']=[]
          paragraph['genetic_types']=[]
          if (annotation.has_chemicals()):
              for chemical in annotation.get_chemicals():
                  if ('found_term' in chemical):
                      paragraph['chemicals'].append(chemical['found_term'])
                  if ('text_term' in chemical):
                      paragraph['chemical_terms'].append(chemical['text_term'])
                  if ('ATC' in chemical):
                     paragraph['atc_codes'].append(str(chemical['ATC']))
                  if ('ATC_level' in chemical):
                     paragraph['atc_levels'].append(str(chemical['ATC_level']))
                  if ('cid' in chemical):
                     paragraph['cid_codes'].append(str(chemical['cid']))
          if (annotation.has_diseases()):
              for disease in annotation.get_diseases():
                  if ('found_term' in disease):
                     paragraph['diseases'].append(disease['found_term'])
                  if ('text_term' in disease):
                     paragraph['disease_terms'].append(disease['text_term'])
                  if ('semantic_type' in disease):
                     paragraph['disease_types'].append(disease['semantic_type'])
                  if ('cui' in disease):
                     paragraph['cui_codes'].extend(str(disease['cui']))
                  if ('mesh_id' in disease):
                     paragraph['mesh_codes'].append(str(disease['mesh_id']))
                  if ('cross_references' in disease):
                      for reference in disease['cross_references']:
                          if (reference.startswith('ICD10CM')):
                                paragraph['icd10_codes'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('ICD9CM')):
                                paragraph['icd9_codes'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('SNOMEDCT')):
                                paragraph['snomed_codes'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('DOID')):
                                paragraph['doid_codes'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('NCI')):
                                paragraph['nci_codes'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('GARD')):
                                paragraph['gard_codes'].append(str(reference.split(":")[1]))
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
                     paragraph['genetic_terms'].append(genetic['text_term'])
                  if ('uniprot_id' in genetic):
                     paragraph['uniprot_codes'].extend(str(genetic['uniprot_id']))
                  if ('type' in genetic):
                     paragraph['genetic_types'].extend(genetic['type'])
                  if ('ncbi_gene_id' in genetic):
                     paragraph['ncbi_codes'].append(str(genetic['ncbi_gene_id']))
                  if ('ncbi_taxon_id' in genetic):
                     paragraph['ncbi_taxonomy'].append(str(genetic['ncbi_taxon_id']))

    except AttributeError as e:
        print("Missing attribute:",e)

    return paragraph
