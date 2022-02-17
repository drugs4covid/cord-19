import pysolr

# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('https://librairy.linkeddata.es/solr/cord19-paragraphs', always_commit=True, timeout=50)

# Note that auto_commit defaults to False for performance. You can set
# `auto_commit=True` to have commands always update the index immediately, make
# an update call with `commit=True`, or use Solr's `autoCommit` / `commitWithin`
# to have your data be committed following a particular policy.
times = 0
#for doc in solr.search('*:*',rows=10,start=5,sort='id ASC',cursorMark='*'):

finished = False
page = 10
size = 5
total = -1
max_size = 0
while (total < max_size):
    page += 1
    results = solr.search('*:*',rows=size,start=page,sort='id ASC')
    max_size = results.hits
    num_found = len(results)
    next_cursor = results.nextCursorMark
    print("Page:",page,"Num_Found:", num_found,"Total:",total,"Hits:",max_size)
    if (len(results) < size):
        print("total index read")
        break
    for doc in results:
        print(doc['id'])
        total += 1


#for doc in solr.search('*:*',rows=1,start=0,sort='id ASC'):
#    print(doc['id'])
#    times += 1
#    if (times > 2):
#        break
