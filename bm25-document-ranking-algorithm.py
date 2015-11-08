# Packages
import glob
import os
from collections import Counter
import math
from nltk import PorterStemmer
import time


# Changing current directory
os.chdir("this-file-path")


# Global Variables
documents = []
SPECIAL_CHARACTERS = ['.', '?', ',', '!', "'s", "'"]
posting_list = {}
document_length = {}
vocabulary = set([])
idf = {}
K1 = 1.5
B = 0.75
score = {}


# List all files
for file in glob.glob("*.txt"):
    documents.append(file)
    posting_list[file] = {}
    score[file] = 0
documents.remove('inverted-index.txt')
posting_list.pop('inverted-index.txt')
score.pop('inverted-index.txt')
print 'List of Documents:', documents
print
print


# Remove special characters
def removeSpecialCharacters(string):
    for character in SPECIAL_CHARACTERS:
        if character in string:
            string = string.replace(character, '')
    return string


# Stem a word
def stem(word):
    return PorterStemmer().stem_word(word)


# Ask for query
query = raw_input('Enter your query: ')
query = removeSpecialCharacters(query).lower()
query = query.split()
query = map(stem, query)
print
print 'Your Query:', query
print


# Reading already existing inverted index
with open ('inverted-index.txt', "r") as f:
    test = f.read().replace('\n', ' ')
if test == "":
    test = []
else:
    test = test[:-2]
    test = test.split(';')
posting_list = {}

for x in test:
    temp = x.split(':')
    doc_name = temp[0].strip()
    doc_index = temp[1].strip()
    posting_list[doc_name] = {}
    temp2 = doc_index.split(',')
    for y in temp2:
        y = y.strip().split('=')
        y[0] = y[0].strip()
        y[1] = int(y[1])
        posting_list[doc_name][y[0]] = y[1]


docs_indexed = posting_list.keys()
print 'docs_indexed:', docs_indexed
print
print
docs_remaining = set(documents).difference(set(docs_indexed))
print 'docs_remaining:', docs_remaining
print
print
docs_delete = set(docs_indexed).difference(set(documents))
print 'docs_delete:', docs_delete
print
print
for doc in docs_delete:
    posting_list.pop(doc)
# Adding words in vocabulary and document length of the documents indexed already
for doc in posting_list:
    document_length[doc] = sum(posting_list[doc].values())
    vocabulary.update(set(posting_list[doc].keys()))


# Creating inverted index according to the query
for aDocument in docs_remaining:
    # Read the document
    with open (aDocument, "r") as f:
        test = f.read().replace('\n', ' ')
    # Remove special characters and convert into lowercase
    test = removeSpecialCharacters(test).lower()
    # Make string into list
    test = test.split()
    # Stem
    test = map(stem, test)
    test = Counter(test).most_common()
    test = dict((x, y) for x, y in test)
    document_length[aDocument] = sum(test.values())
    # Adding words into vocabulary
    vocabulary.update(set(test.keys()))
    # Creating inverted index for the document
    posting_list[aDocument] = {}
    for term in test:
        posting_list[aDocument][term] = test[term]


# Adding respective remaining words to all docs inverted index
for doc in posting_list:
    for term in vocabulary:
        if term not in posting_list[doc]:
            posting_list[doc][term] = 0
        

print 'Document Length:', document_length
print
print
print 'Posting List:'
for doc in posting_list:
    print doc, len(posting_list[doc].keys())
print
print


# numDocuments
def numDocuments(term):
    count = 0
    for doc in posting_list:
        if term in posting_list[doc]:
            if posting_list[doc][term] > 0:
                count += 1
    return count


# Calculate IDF
for term in query:
    n = numDocuments(term)
    if n == 0:
        idf[term] = 0.0
    else:
        idf[term] = math.log(len(documents) / float(n))
        #idf[term] = math.log((len(documents) - n + 0.5) / (n + 0.5))
print
print 'IDF:', idf
print
print


# Calculate Score
avgdl = sum(document_length.values()) / float(len(document_length))
for doc in documents:
    for term in query:
        if term in posting_list[doc]:
            score[doc] += (idf[term])* (((posting_list[doc][term]) * (K1 + 1)) / ((posting_list[doc][term]) + (K1 * (1 - B + (B * (document_length[doc] / avgdl))))))
        else:
            score[doc] += 0.0
print 'Score:', score
print
print
print '***** Final Rank *****'
for doc in [k for k in sorted(score, key=score.get, reverse=True)]:
    print doc
print
print


# Strat time for writing
t1 = time.time()

# Writing back the new inverted index in the file
if len(docs_remaining) != 0:
    f = open('inverted-index.txt', 'w')
    for temp in posting_list:
        string = ""
        string = string + temp + ': '
        for temp2 in posting_list[temp]:
            string = string + temp2 + ' = ' + str(posting_list[temp][temp2]) + ', '
        string = string[:-2] + ';\n'
        f.write(string)
    f.close()


# Printing time elapsed in writing
t2 = time.time()
print t2 - t1
