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


if __name__ == '__main__':

    text = "We found that OC43 was the species that was most commonly detected, which is in line with earlier studies [1-3, 5, 10, 13, 26, 27] . The odds ratio for positive samples in our study was significantly lower for females than males. This gender difference is interesting in relation to COVID-19, as male patients have a higher risk of severe disease and death than females [28, 29] . We noted CoV infections across all age strata, although the highest prevalence was observed among children. At species level, the fraction of positive samples was relatively even across age strata for 229E and OC43. In contrast, HKU1 and NL63 showed a declining prevalence with increasing age. Collectively, our results indicate that symptomatic CoV reinfections among adults and elderly are not uncommon even though we did not formally exclude the possibility that they had primary CoV infections through serological testing."
    annotation = Annotation(text)
    print("Chemicals:",annotation.get_chemicals())
    print("Diseases:",annotation.get_diseases())
    print("Covid:",annotation.get_covid())
    print("Genetics:",annotation.get_genetics())
