from nltk.stem import PorterStemmer
# Make sure to run "pip install nltk"

import re
import os
import zipfile
import math

# Regular expressions to extract data from the corpus
doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)
token_regex = re.compile(r"\w+(\.?\'?\,?\w+)*")

# Initialize all the global variables
doc_ID_counter = 1
term_ID_counter = 1

# A hashmap of term -> ID
term_Index = dict()
# A hashmap of doc -> doc_node
doc_Index = dict()
# A hashmap of docID -> docname
doc_Info = dict()
# A hashmap of term -> term_node
term_Info = dict()

stop_words = set()
stemmer = PorterStemmer()

# Initialize classes
class Posting_Node:
    def __init__(self, ID):
        self.ID = ID
        self.positions = []
        
    def add_Position(self, position):
        self.positions.append(position)
        
    def get_ID(self):
        return self.ID
    
    def get_Frequency(self):
        return len(self.positions)
        
    def get_Positions(self):
        return self.positions
        
class Term_Node:
    def __init__(self, ID):
        self.ID = ID
        
        # A hashmap of docID -> Posting_Node
        self.posting_list = dict()
        
    def add_Position(self, docID, position):
        if docID not in self.posting_list:
            self.posting_list[docID] = Posting_Node(docID)
        self.posting_list[docID].add_Position(position)
    
    def get_ID(self):
        return self.ID
    
    def get_Documents(self):
        return len(self.posting_list)
    
    def get_Occurrences(self):
        occurrences = 0
        for key in self.posting_list:
            occurrences = occurrences + self.posting_list[key].get_Frequency()
        return occurrences
    
    def get_Posting_List(self):
        return self.posting_list
        
    def get_Posting_Node(self, docID):
        return self.posting_list[docID]

class Doc_Node:
    def __init__(self, ID):
        self.ID = ID
        self.distinct_terms = 0
        self.total_terms = 0
    
    def set_Distinct_Terms(self, distinct):
        self.distinct_terms = distinct
        
    def set_Total_Terms(self, total):
        self.total_terms = total
    
    def get_ID(self):
        return self.ID
        
    def get_Distinct_Terms(self):
        return self.distinct_terms
        
    def get_Total_Terms(self):
        return self.total_terms

# Initialize stop_words
stop_file = open("stopwords.txt","r")
for line in stop_file:
    line = line.strip("\n")
    stop_words.add(line)
stop_file.close()

with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
    zip_ref.extractall()
   
# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
    allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
    
print("* Parsing Started *")
for file in allfiles:
    with open(file, 'r', encoding='ISO-8859-1') as f:
        filedata = f.read()
        result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

        for document in result[0:]:
            # Retrieve contents of DOCNO tag
            docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
            # Retrieve contents of TEXT tag
            text = "".join(re.findall(text_regex, document))\
                      .replace("<TEXT>", "").replace("</TEXT>", "")\
                      .replace("\n", " ")

            # Part 1 - lower-case words, remove punctuation, remove stop-words, etc. 
            tokens = []
            
            ## Checking repeated documents
            if docno in doc_Index:
                continue
                
            ## New Document ID
            doc_Index[docno] = Doc_Node(doc_ID_counter)
            doc_Info[doc_ID_counter] = docno
            doc_ID_counter = doc_ID_counter + 1
            
            ## Lowercase the word
            text = text.lower();
            
            ## Remove underscores (\w allows underscores for some reason)
            text = text.replace("_","")

            ## Process  the text string

            for match in re.finditer(token_regex, text):
                token = (match.group())
                
                # Remove apostrophe
                token = token.split("'")[0]
                
                # Remove stop-words
                if (token in stop_words):
                    continue
                
                # Stemming
                token = stemmer.stem(token)
                
                # Add the token to our list
                tokens.append(token)
            
            # Part 2 - create tokens
            pos_counter = 1
            distinct_terms = 0

            for token in tokens:
                
            ## Matching unique term ID
                if token not in term_Index:
                    term_Index[token] = term_ID_counter
                    distinct_terms = distinct_terms + 1
                    term_ID_counter = term_ID_counter + 1
                
                # print("(", term_Index[token], ", ", token, ", ", doc_Index[docno].get_ID(), ", ", pos_counter, ") ") 
                
                ## Setting up term_Info
                if term_Index[token] not in term_Info:
                    term_Info[term_Index[token]] = Term_Node(term_Index[token])
                
                ### Add this position
                term_Info[term_Index[token]].add_Position(doc_Index[docno].get_ID(), pos_counter)
                              
                pos_counter = pos_counter + 1
            
            ## Add distinct terms and total terms to the documents
            doc_Index[docno].set_Distinct_Terms(distinct_terms)
            doc_Index[docno].set_Total_Terms(len(tokens))
   
print("* Parsing Complete *")
   
# Part Extra Credit
def write_to_disk():
    print("* Writing To Disk Started *")

    ## Building term_index.txt
    byte_counter = 0
    offset = 0

    term_Index_file = open("term_index.txt","w")
    term_Info_file = open("term_info.txt","w")

    for term_name in term_Index:
        offset = byte_counter
        
        term_Index_file.write(str(term_Index[term_name]))
        byte_counter = byte_counter + len(str(term_Index[term_name]))
        
        for posting_node_key in term_Info[term_Index[term_name]].get_Posting_List():
            posting_node = term_Info[term_Index[term_name]].get_Posting_List()[posting_node_key]
            for position in posting_node.get_Positions():
            
                term_Index_file.write("\t" + str(posting_node.get_ID()) + ":" + str(position))
                byte_counter = byte_counter + len(str(posting_node.get_ID())) + len(str(position)) + 2
                
        term_Index_file.write("\n")
        byte_counter = byte_counter + 2
        
        ## Building term_info.txt
        term_Info_file.write(str(term_Index[term_name]) + "\t" + str(offset) + "\t" + str(term_Info[term_Index[term_name]].get_Occurrences()) + "\t" + str(term_Info[term_Index[term_name]].get_Documents()) + "\n")

    term_Index_file.close()
    term_Info_file.close()

    ## Example of how to use seek
    # readding = open("term_index.txt","r")
    # readding.seek(14)
    # print(readding.readline())

    ## Building docids.txt
    docids_file = open("docids.txt","w")
    for doc_name in doc_Index:
        docids_file.write(str(doc_Index[doc_name].get_ID()) + "\t" + str(doc_name) + "\n")
    docids_file.close()

    ## Building termidis.txt
    termids_file = open("termids.txt","w")
    for term_name in term_Index:
        termids_file.write(str(term_Index[term_name]) + "\t" + str(term_name) + "\n")
    termids_file.close()
    
    print("* Writing To Disk Complete *")

# Part 3
def process_commands(**user_input):
    
    print()

    if "term" in user_input and "doc" in user_input:
        input_term = user_input["term"]
        input_doc = user_input["doc"].upper()
        
        print("Inverted list for term:", input_term)
        print("In document:", input_doc)
        print("TERM ID:", term_Index[input_term])
        print("DOC ID:", doc_Index[input_doc].get_ID())
        print("Term frequency in document:", term_Info[term_Index[input_term]].get_Posting_List()[doc_Index[input_doc].get_ID()].get_Frequency())
        
        positions_string = ""
        first = True
        for pos in term_Info[term_Index[input_term]].get_Posting_List()[doc_Index[input_doc].get_ID()].get_Positions():
            if first:
                positions_string = positions_string + str(pos)
                first = False
            else:
                positions_string = positions_string + ", " + str(pos)
                
        print("Positions:", positions_string)
        
    elif "doc" in user_input:
        input_doc = user_input["doc"].upper()
    
        print("Listing for document:", input_doc)
        print("DOC ID:", doc_Index[input_doc].get_ID())
        print("Distinct terms:", doc_Index[input_doc].get_Distinct_Terms())
        print("Total terms:", doc_Index[input_doc].get_Total_Terms())
        
    elif "term" in user_input:
        input_term = user_input["term"]
        
        print("Listing for term:", input_term)
        print("TERM ID:", term_Index[input_term])
        print("Number of documents containing term:", term_Info[term_Index[input_term]].get_Documents())
        print("Term frequency in corpus:", term_Info[term_Index[input_term]].get_Occurrences())

def set_write():
    print()
    write_to_disk()

def process_query(query_path, output_path):
    
    print()
    print("* Reading Query File *")

    queries = []
    
    # Read query file
    query_file = open(query_path[0], "r")
    for line in query_file:
        line = line.strip("\n")
        queries.append(line)
    query_file.close()
    
    print("* Finished Reading *")
    
    print()
    
    print("* Writing Query Results *")
    
    # Start building the output file
    output_file = open(output_path[0], "w")

    # Start running queries
    for query in queries:
        split_query = query.split(". ", 1)
        
        # returns a list of the top 10 results
        results = run_query(split_query[1])
       
        # Write a new line for each resuts in results
        rank = 1
        for result in results:
            output_file.write(str(split_query[0]) + " Q0 " + str(doc_Info[result[0]]) + " " + str(rank) + " " + str(result[1]) + " Exp\n")
            rank = rank + 1
    output_file.close()
    
    print("* Finished Writing *")
    
def run_query(query):
        
    results = []
    
    # loop through all the documents
    for docID in doc_Info:
        # get the score
        score = vector_space(docID, query)
        
        # if score is 0, skip
        if score == 0:
            continue
        
        # append ID and score combo
        results.append([docID, score])

    # Get the top 10
    results = sorted(results, key = lambda x: x[1], reverse = True)[:19]
    return results
  
def vector_space(docID, query):
    
    query_vector = []
    doc_vector = []
    
    # Lowercase the word
    query = query.lower();
    
    # Remove underscores (\w allows underscores for some reason)
    query = query.replace("_","")

    # Process  the text string

    repeated_words = []
    counter = 0
    # For each word in the query, see if the document has the same word
    for match in re.finditer(token_regex, query):
        word = (match.group())
        
        # Remove apostrophe
        word = word.split("'")[0]
        
        # Remove stop-words
        if (word in stop_words):
            continue
        
        # Stemming
        word = stemmer.stem(word)
        
        # If it is a repeat, skip and continue
        if (word in repeated_words):
            continue
            
        repeated_words.append(word)
        
        # Start building the vector for each query word
        query_vector.append(1)
        
        ## See if the word is in the term index
        if word not in term_Index:
            doc_vector.append(0)
            continue
        
        ## See if word is in document
        if docID not in term_Info[term_Index[word]].get_Posting_List():
            doc_vector.append(0)
            continue
        
        doc_vector.append(1)
        counter = counter + 1
        
    # Add in the words that are in the document but not the query
    distinct_words = doc_Index[doc_Info[docID]].get_Distinct_Terms()
    
    i = 0
    while(i < distinct_words - counter):
        query_vector.append(0)
        doc_vector.append(1)
        i = i + 1
    
    # print("Doc ID: ", docID, " ", doc_vector)
    # print("Query: ", query, " ", query_vector)
    # print(cos_sim(doc_vector, query_vector))
    return cos_sim(doc_vector, query_vector)

def cos_sim(doc_vector, query_vector):

    # If empty vectors
    if not doc_vector or not query_vector:
        return 0
        
    dot_product = 0
    for i in range(len(doc_vector)):
        dot_product = dot_product + doc_vector[i] * query_vector[i]
    
    doc_square = 0
    query_square = 0
    
    for num in doc_vector:
        doc_square = doc_square + num**2
    
    for num in query_vector:
        query_square = query_square + num**2
        
    # Cannot divide by 0
    if (math.sqrt(doc_square * query_square)) == 0:
        return 0
    
    return dot_product/(math.sqrt(doc_square * query_square))
    
def main():
    return
    
main()
    

