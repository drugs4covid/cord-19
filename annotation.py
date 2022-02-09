import requests

class Annotation():

    def __init__(self,text):
        bio_ner = "https://librairy.linkeddata.es/bio-ner/entities"
        headers = {'Content-type': 'application/json; charset=utf-8'}
        response = requests.post(bio_ner, json = { 'text':text}, headers=headers)
        self.chemicals  = []
        self.diseases   = []
        self.covid      = []
        self.genetics   = []
        if (response.status_code == 200):
            data = response.json()
            if ('entities' in data):
                entities = data['entities']
                if ('chemicals' in entities):
                    self.chemicals = entities['chemicals']
                if ('diseases' in entities):
                    self.diseases = entities['diseases']
                if ('covid' in entities):
                    self.covid = entities['covid']
                if ('genetics' in entities):
                    self.genetics = entities['genetics']



    def get_chemicals(self):
        return self.chemicals

    def has_chemicals(self):
        return len(self.chemicals) > 0

    def get_diseases(self):
        return self.diseases

    def has_diseases(self):
        return len(self.diseases) > 0

    def get_covid(self):
        return self.covid

    def has_covid(self):
        return len(self.covid) > 0

    def get_genetics(self):
        return self.genetics

    def has_genetics(self):
        return len(self.genetics) > 0
