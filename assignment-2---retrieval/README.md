# CS172 - Assignment 1 (Tokenization)

### Team member 1 - Kevin Ni

### Team member 2 - Aden Ghadimi

## How to use
We developed this in python, and you must the download packages for installing NLTK. 

Here are the instructions. 

Installing NLTK on Windows 10

Step 1: Check Python Version.

> $python --version

Step 2: Install Numpy

> $pip install numpy

Step 3: Install NLTK

> $pip install nltk

Step 4: Check if NLTK is installed 

"$python import nltk"

Afterwards, Clone Repository, and run on either command prompt or the IDE of your choosing.

Make sure to have python version 3 installed. This can be found [here](https://www.python.org/download/releases/3.0/)

Make sure to have the nltk package installed. This can be found [here](https://www.nltk.org/install.html)

Run `py VSM.py` to pull up a help GUI of possible commmands.

Required paramters are:
> query file path

> output file path

Possible flags are:
> --write

## Implementation
### Made 3 classes
Posting_Node stores positions and frequencies for a given document ID. This is used by Term_Node

Term_Node stores number of documents the term has appeared in, occurrences, and a hashmap of Posting_Node's for a given term ID.

Doc_Node stores number of distinct terms and number of total terms for a given document ID.

### Made a few global variables
term_Index is a hashmap that maps terms to term IDs

doc_Index is a hashamp that maps doc IDs to Doc_Node's

doc_Info is a hashmap that maps doc IDS to document names

term_Info is a hashmap that maps term IDs to Term_Node's

stop_words is a hashset of words

## Assignment Parts

### Vector Space Model
Binary weights

Cosine Similarity

### Write to disk
The file VSM.py uses argparse library to help with the command parsing

Should the `--write` flag be found, enable writing to disk

## Completion
We attempted the Vector Space Model with binary weights
