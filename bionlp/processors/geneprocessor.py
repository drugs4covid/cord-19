from .bioprocessor import BioProcessor
import pysolr
from bionlp.processors.utils import unique_terms
import re
import os


class GeneProcessor(BioProcessor):

    def __init__(self, model_name):
        super().__init__(model_name)
        self.solr_url = os.getenv('SOLR_URL','http://librairy.linkeddata.es/solr/')
        try:
            self.solr_engine = pysolr.Solr(self.solr_url + 'genetic', timeout=50)
        except ConnectionError:
            print('Connection with Solr Genetic database could not be established')

    def normalize_genetic_entities(self, genetic_ents):
        normalized_gen = []
        genetics = unique_terms(genetic_ents)
        for gen in genetics:
            try:
                label = str(gen)
                solr_query_strict = 'term:\"' + label + '\"^100 or synonyms:\"' + label + '\"^10'
                solr_query_lax = 'term:' + label + '^100 or synonyms:' + label + '^10'
                solr_query_strict_syn = 'term:\"' + label + '\"^10 or synonyms:\"' + label + '\"^100'
                solr_query_lax_syn = 'term:' + label + '^10 or synonyms:' + label + '^100'
                results_lax = self.solr_engine.search(solr_query_lax, **{'fl': '*,score'})
                results_strict = self.solr_engine.search(solr_query_strict, **{'fl': '*,score'})
                results_lax_synonyms = self.solr_engine.search(solr_query_lax_syn, **{'fl': '*,score'})
                results_strict_synonyms = self.solr_engine.search(solr_query_strict_syn, **{'fl': '*,score'})
            except Exception:
                label = re.sub(r'\W+', ' ', str(gen))
                try:
                    solr_query_strict = 'term:\"' + label + '\"^100 or synonyms:\"' + label + '\"^10'
                    solr_query_lax = 'term:' + label + '^100 or synonyms:' + label + '^10'
                    solr_query_strict_syn = 'term:\"' + label + '\"^10 or synonyms:\"' + label + '\"^100'
                    solr_query_lax_syn = 'term:' + label + '^10 or synonyms:' + label + '^100'
                    results_lax = self.solr_engine.search(solr_query_lax, **{'fl': '*,score'})
                    results_strict = self.solr_engine.search(solr_query_strict, **{'fl': '*,score'})
                    results_lax_synonyms = self.solr_engine.search(solr_query_lax_syn, **{'fl': '*,score'})
                    results_strict_synonyms = self.solr_engine.search(solr_query_strict_syn, **{'fl': '*,score'})
                except Exception as e:
                    print("error on genetic",e)
                    continue

            if len(results_lax) < 1 and len(results_strict) < 1:
                genetic = {'text_term': label}
                normalized_gen.append(genetic)
            else:
                # print(label)
                score_lax = 0
                score_strict = 0
                score_lax_syn = 0
                score_strict_syn = 0
                for result in results_lax:
                    # print(result['term'])
                    score_lax = result['score']
                    # print(score_lax)
                    break
                for result in results_strict:
                    # print(result['term'])
                    score_strict = result['score']
                    # print(score_strict)
                    break
                for result in results_strict_synonyms:
                    # print(result['term'])
                    score_strict_syn = result['score']
                    # print(score_strict_syn)
                    break
                for result in results_lax_synonyms:
                    # print(result['term'])
                    score_lax_syn = result['score']
                    # print(score_lax_syn)
                    break
                results_scores = {results_lax: score_lax, results_strict: score_strict,
                                  results_strict_synonyms: 0.8 * score_strict_syn,
                                  results_lax_synonyms: 0.8 * score_lax_syn}
                results = max(results_scores, key=results_scores.get)
                for result in results:
                    genetic = {}
                    genetic["text_term"] = label
                    if "term" in result:
                        genetic["found_term"] = "".join(result["term"])
                    if 'ncbi_gene_id' in result:
                        genetic['ncbi_gene_id'] = [str(e) for e in result["ncbi_gene_id"]]
                    if 'ncbi_taxon_id' in result:
                        genetic['ncbi_taxon_id'] = [str(e) for e in result["ncbi_taxon_id"]]
                    if 'type' in result:
                        genetic['type'] = result["type"]
                    if 'cross_reference' in result:
                        genetic['cross_reference'] = result["cross_reference"]
                    if 'uniprot_id' in result:
                        genetic['uniprot_id'] = result["uniprot_id"]
                    normalized_gen.append(genetic)
                    break
        return normalized_gen
