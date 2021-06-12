from elasticsearch import Elasticsearch
import os
import sys
import json

# Elastic search configuation

es = Elasticsearch(HOST="http://localhost", PORT=9200)
es = Elasticsearch()

# es.indices.delete(index="wikipedia")

if not (es.indices.exists(index="wikipedia")):
    es.indices.create(index="wikipedia")

id_counter = 1
path = os.getcwd()    
directory = path + "/data"

# for filename in os.listdir(directory):
    # if filename.endswith(".json"):
        # filepath = os.path.join(directory, filename)
        # with open(filepath, "rb") as file:
            # body = file.read()
            # es.index(index = "wikipedia", id = id_counter, body = body)
            # id_counter = id_counter + 1

body = {
    "from":0,
    "size":5,
    "query": {
        "match": {
            "paragraphs.text" : "Adolf Hitler"
        }
    }
}

result = es.search(index = "wikipedia", body = body)
for hit in result['hits']['hits']:
    print(hit["_source"]["title"], " with score of: ", hit["_score"])
    



            
        
        



    


