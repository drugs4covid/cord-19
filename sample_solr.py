import pysolr

# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('https://librairy.linkeddata.es/solr/cord19-paragraphs', always_commit=True, timeout=50)

# Note that auto_commit defaults to False for performance. You can set
# `auto_commit=True` to have commands always update the index immediately, make
# an update call with `commit=True`, or use Solr's `autoCommit` / `commitWithin`
# to have your data be committed following a particular policy.

# Do a health check.
solr.ping()

# How you'd index data.
solr.add([
    {
        "text_t":"In this paper, we have established a PMO-functionalized G-FET nanosensor for the rapid direct detection of SARS-CoV-2 RNA in clinical throat swab samples with an attempt to realize a PCR-free identification of COVID-19. During the pandemic, this method is expected to be an effective diagnostic tool of COVID-19 with following attractive merits: (i) Detection limit is as low as 0.37 fM, which is below the other reported biosensing platform (Table S4 ). (ii) Allowing a well-defined distinction between SARS-CoV-2 RdRp and SARS-CoV RdRp. (iii) Excellent antiinterference capability and precision in undiluted biological samples (throat swab/serum) detection. (iv) Outstanding reliability and accuracy for testing of RNA extracts from real clinical specimens and a high agreement with the results of RT-PCR. (v) Rapid specific response to COVID-19 patient samples can be achieved within 2 min by real-time measurement. (ⅵ) A crucial advance in this work is PCR-free direct detection without pre-amplification, which consumedly reduces the molecular diagnostic turn-around time. In summary, the yielded platform provides a rapid (~2 min), sensitive, and reliable detection strategy for SARS-CoV-2. It is hoped that this sensing platform can be used as a rapid screening tool in the emergency department. When close contacts are under medical observation, the method can be used to quickly identify infected individuals and give immediate feedback to doctors. It is believed that this is a powerful means of combating current COVID-19 as well as any future outbreaks. ",
        "id":"00-sample",
        "section_s":"Conclusions",
        "article_id_s":"a72590332f936f24b1b55f1603444af79464a424",
        "size_i":1566,
        "mesh_codes_ss":["D000086382","D045169"],
        "doid_codes_ss":["80600","2945"],
        "cui_codes_ss":["C5203670","C1175175"],
        "icd10_codes_ss":["U07.1","J12.81"],
        "icd9_codes_ss":["79.82"],
        "gard_codes_ss":["9237"],
        "snomed_codes_ss":["840539006","398447004"],
        "nci_codes_ss":["C85064"],
        "diseases_ss":["Severe acute respiratory syndrome coronavirus 2",
          "COVID-19",
          "Severe Acute Respiratory Syndrome"],
        "disease_terms_ss":["SARS-CoV-2",
          "COVID-19",
          "SARS-CoV"],
        "disease_types_ss":["Respiratory tract disease|Viral disease",
          "Respiratory tract disease|Viral disease"],
    }
])

# You can index a parent/child document relationship by
# associating a list of child documents with the special key '_doc'. This
# is helpful for queries that join together conditions on children and parent
# documents.

# Later, searching is easy. In the simple case, just a plain Lucene-style
# query is fine.
results = solr.search('id:00-sample')

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print(result)
