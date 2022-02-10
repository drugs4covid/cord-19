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
          fields = ['mesh_codes','chemicals','chemical_terms','atc_codes','atc_levels','cid_codes','doid_codes','cui_codes','icd10_codes','icd9_codes','gard_codes','snomed_codes','nci_codes','ncbi_codes','ncbi_taxonomy','uniprot_codes','diseases','disease_terms','disease_types','covid','covid_terms','genetics','genetic_terms','genetic_types']
          # Initialize fields
          for field in fields:
              # Remove exiting ones to avoid type format error
              paragraph.pop(field, None)
              paragraph[field+"_t"]=[]

          if (annotation.has_chemicals()):
              for chemical in annotation.get_chemicals():
                  if ('found_term' in chemical):
                      paragraph['chemicals'].append(chemical['found_term'])
                  if ('text_term' in chemical):
                      paragraph['chemical_terms'].append(chemical['text_term'])
                  if ('ATC' in chemical):
                     paragraph['atc_codes_t'].append(str(chemical['ATC']))
                  if ('ATC_level' in chemical):
                     paragraph['atc_levels_t'].append(str(chemical['ATC_level']))
                  if ('cid' in chemical):
                     paragraph['cid_codes_t'].append(str(chemical['cid']))
          if (annotation.has_diseases()):
              for disease in annotation.get_diseases():
                  if ('found_term' in disease):
                     paragraph['diseases'].append(disease['found_term'])
                  if ('text_term' in disease):
                     paragraph['disease_terms'].append(disease['text_term'])
                  if ('semantic_type' in disease):
                     paragraph['disease_types'].append(disease['semantic_type'])
                  if ('cui' in disease):
                     paragraph['cui_codes_t'].extend(disease['cui'])
                  if ('mesh_id' in disease):
                     paragraph['mesh_codes_t'].append(str(disease['mesh_id']))
                  if ('cross_references' in disease):
                      for reference in disease['cross_references']:
                          if (reference.startswith('ICD10CM')):
                                paragraph['icd10_codes_t'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('ICD9CM')):
                                paragraph['icd9_codes_t'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('SNOMEDCT')):
                                paragraph['snomed_codes_t'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('DOID')):
                                paragraph['doid_codes_t'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('NCI')):
                                paragraph['nci_codes_t'].append(str(reference.split(":")[1]))
                          elif (reference.startswith('GARD')):
                                paragraph['gard_codes_t'].append(str(reference.split(":")[1]))
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
                     paragraph['uniprot_codes_t'].extend(genetic['uniprot_id'])
                  if ('type' in genetic):
                     paragraph['genetic_types_t'].extend(genetic['type'])
                  if ('ncbi_gene_id' in genetic):
                     paragraph['ncbi_codes_t'].append(str(genetic['ncbi_gene_id']))
                  if ('ncbi_taxon_id' in genetic):
                     paragraph['ncbi_taxonomy_t'].append(str(genetic['ncbi_taxon_id']))

    except AttributeError as e:
        print("Missing attribute:",e)

    return paragraph


if __name__ == '__main__':

    paragraph = {'text_t':"Despite over 300 active and recruiting clinical trials and a number of trials already completed, there is still no robust evidence that any of the investigated therapeutics are effective as treatments for COVID-19 disease (Channappanavar et al., 2017) . Equally, there is no evidence to support prophylactic treatment either (Sanders et al., 2020) . However, there are only 29 trials in adult patients with placebo-controlled arm (Channappanavar et al., 2017) . Various types of pharmacological treatments are currently under investigation including anti-viral, anti-malarial and anti-inflammatory agents. These therapies generally target the following processes: (1) the entry of the virus into host cells, (2) multiplication of the viral genetic material, and (3) immune response/inflammation. Most of these agents have been previously used as treatments for SARS-CoV and MERS-CoV, however the overall conclusions of the meta-analyses published in 2006 and 2018, respectively, did not support the use of any particular regimen. In relation to the meta-analysis of SARS-CoV treatments, the authors systematically reviewed 54 treatment studies, 15 in vitro studies and three ARDS studies (Stockman et al., 2006) . Although the combination of ribavirin and interferon-based (IFN) treatments appears the most effective for MERS (Morra et al., 2018) , this needs to be confirmed in randomized placebo-controlled trial settings. In terms of vaccines, there are at least 115 vaccine candidates in development with a number of these already initiated in human trials, however we expect vaccines to be available to people under emergency use only in early 2021 (Callaway, 2020; Thanh Le et al., 2020) ."}
    annotation = parse(paragraph)
    print(annotation)
