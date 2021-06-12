from elasticsearch import Elasticsearch, Connection
import os
import sys
import json
import glob
import requests
import elasticsearch.connection as conn

def search(query):

    # Check if ElasticSearch is working
    if not isRunning():
        return "ElasticSearch is not working"

    # Attach Elasticsearch
    es = Elasticsearch(HOST="http://localhost", PORT=9200)
    es = Elasticsearch()

    # Create new index
    es.indices.delete(index="wikipedia")
    if not (es.indices.exists(index="wikipedia")):
        es.indices.create(index="wikipedia")
    
    # Fill in the index
    id_counter = 1
    path = os.getcwd()    
    directory = path + "/data"

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "rb") as file:
                body = file.read()
                es.index(index = "wikipedia", id = id_counter, body = body)
                id_counter = id_counter + 1
                
    # Create the query
    body = {
        "from":0,
        "size":10,
        "query": {
            "match": {
                "paragraphs.text" : query
            }
        }
    }
    
    result = es.search(index = "wikipedia", body = body)
    text = ""
    
    rank = 1
    for hit in result['hits']['hits']:
        text = text + str(rank) + ". " + str(hit["_source"]["title"]) + " Score of: " + str(hit["_score"]) + "\n"
        rank = rank + 1
        
    if text == "":
        return "No results"
    return text
        
def isRunning():
    try:
        res = requests.get("http://localhost:9200/_cluster/health")
        if res.status_code == 200:
            if res.json()['number_of_nodes'] > 0:
                return True
        return False
    except Exception as e:
        print(e)
        return False