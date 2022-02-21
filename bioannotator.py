#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tuesday June 1 12:52:05 2021

@author: cbadenes
"""
import json
import hashlib
import annotation as an
import os
import inspect
from bionlp import nlp, disease_service, chemical_service, genetic_service

def group_in_dict(normalized_ent):
    normalized_ents = {}
    for k, v in [(key, d[key]) for d in normalized_ent for key in d]:
        if k not in normalized_ents:
            if isinstance(v, list):
                normalized_ents[k] = v
            else:
                normalized_ents[k] = [v]
        else:
            if v not in normalized_ents[k]:
                if isinstance(v, list):
                    normalized_ents[k] += v
                else:
                    normalized_ents[k].append(v)
    return normalized_ents

def parse(paragraph):
    try:
      if ('text_t' in paragraph):
            fields = ['mesh_codes','chemicals','chemical_terms','chebi_codes','atc_codes','atc_levels','cid_codes','doid_codes','cui_codes','icd10_codes','icd9_codes','gard_codes','snomed_codes','nci_codes','ncbi_codes','ncbi_taxonomy','uniprot_codes','diseases','disease_terms','disease_types','genetics','genetic_terms','genetic_types']
            for field in fields:
                paragraph[field+"_ss"]=[]
            doc = nlp(str(paragraph['text_t']))
            paragraph['diseases_ss'] = list({f.text for f in doc.ents if f.label_ == 'DISEASE'})
            paragraph['chemicals_ss'] = list({f.text for f in doc.ents if f.label_ == 'CHEMICAL'})
            paragraph['genetics_ss'] = list({f.text for f in doc.ents if f.label_ == 'GENETIC'})

            normalized_chem = chemical_service.normalize_chemical_entities(paragraph['chemicals_ss'])
            normalized_d = disease_service.normalize_disease_entities(paragraph['diseases_ss'])
            normalized_g = genetic_service.normalize_genetic_entities(paragraph['genetics_ss'])

            normalized_chems = group_in_dict(normalized_chem)
            normalized_dis = group_in_dict(normalized_d)
            normalized_gen = group_in_dict(normalized_g)

            if 'found_term' in normalized_chems:
                paragraph['chemical_terms_ss'].extend(normalized_chems['found_term'])
            if 'mesh_id' in normalized_chems:
                paragraph['mesh_codes_ss'].extend(normalized_chems['mesh_id'])
            if 'cid' in normalized_chems:
                paragraph['cid_codes_ss'].extend(normalized_chems['cid'])
            if 'chebi_id' in normalized_chems:
                for reference in normalized_chems['chebi_id']:
                    paragraph['chebi_codes_ss'].append(str(reference.split(":")[1]))
            if 'cross_references' in normalized_chems:
                for reference in normalized_chems['cross_references']:
                    if (reference.startswith('ICD10CM')):
                          paragraph['icd10_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('ICD9CM')):
                          paragraph['icd9_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('SNOMEDCT')):
                          paragraph['snomed_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('DOID')):
                          paragraph['doid_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('NCI')):
                          paragraph['nci_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('GARD')):
                          paragraph['gard_codes_ss'].append(str(reference.split(":")[1]))
            if 'ATC' in normalized_chems:
                paragraph['atc_codes_ss'].extend(normalized_chems['ATC'])
            if 'ATC_level' in normalized_chems:
                paragraph['atc_levels_ss'].extend(normalized_chems['ATC_level'])

            if 'found_term' in normalized_dis:
                paragraph['disease_terms_ss'].extend(normalized_dis['found_term'])
            if 'mesh_id' in normalized_dis:
                paragraph['mesh_codes_ss'].extend(normalized_dis['mesh_id'])
            if 'semantic_type' in normalized_dis:
                paragraph['disease_types_ss'].extend(normalized_dis['semantic_type'])
            if 'cui' in normalized_dis:
                paragraph['cui_codes_ss'].extend(normalized_dis['cui'])
            if 'ICD10_id' in normalized_dis:
                paragraph['icd10_codes_ss'].extend(normalized_dis['ICD10_id'])
            if 'cross_references' in normalized_dis:
                for reference in normalized_dis['cross_references']:
                    if (reference.startswith('ICD10CM')):
                          paragraph['icd10_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('ICD9CM')):
                          paragraph['icd9_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('SNOMEDCT')):
                          paragraph['snomed_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('DOID')):
                          paragraph['doid_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('NCI')):
                          paragraph['nci_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('GARD')):
                          paragraph['gard_codes_ss'].append(str(reference.split(":")[1]))

            if 'found_term' in normalized_gen:
                paragraph['genetic_terms_ss'].extend(normalized_gen['found_term'])
            if 'ncbi_gene_id' in normalized_gen:
                paragraph['ncbi_codes_ss'].extend(normalized_gen['ncbi_gene_id'])
            if 'type' in normalized_gen:
                paragraph['genetic_types_ss'].extend(normalized_gen['type'])
            if 'ncbi_taxon_id' in normalized_gen:
                paragraph['ncbi_taxonomy_ss'].extend(normalized_gen['ncbi_taxon_id'])
            if 'cross_reference' in normalized_gen:
                for reference in normalized_gen['cross_reference']:
                    if (reference.startswith('ICD10CM')):
                          paragraph['icd10_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('ICD9CM')):
                          paragraph['icd9_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('SNOMEDCT')):
                          paragraph['snomed_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('DOID')):
                          paragraph['doid_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('NCI')):
                          paragraph['nci_codes_ss'].append(str(reference.split(":")[1]))
                    elif (reference.startswith('GARD')):
                          paragraph['gard_codes_ss'].append(str(reference.split(":")[1]))
            if 'uniprot_id' in normalized_gen:
                paragraph['uniprot_codes_ss'].extend(normalized_gen['uniprot_id'])
    except Exception as e:
        print("Missing attribute:",e)

    return paragraph


if __name__ == '__main__':

    paragraph = {'text_t':"We have carried out a retrospective study on all cases of acute C. difficile infection in children admitted in the Pediatric Department of the National Institute of Infectious Diseases \"Prof. Dr. Matei Balș\" between 2013 and 2016. In all patients we have monitored age, sex, immunological status, clinical form of disease, and evolution under treatment. The diagnosis of colitis was established based on clinical criteria and confirmed through laboratory methods (detection of C. difficile A/B toxin from stool). All cases received treatment according to standard protocol except for one case where allergies to all antibiotics from the therapeutic schemes prompted us to perform fecal microbiota transplantation."}
    print("annotating paragraph...")
    annotation = parse(paragraph)
    print("done!")
    print(annotation)
