# WEEK 3 TASK PART 1: RELEVANCE RANKING

import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# DATA
wikipedia = ""
file_name = "enwiki-20181001-corpus.1000-articles.txt"
try:
    file = open(file_name, "r", encoding='utf-8')
    wikipedia = file.read()
    file.close()
except OSError:
    print("Error reading the file", file_name)

# Split into lists of strings (each article is a string)
documents = wikipedia.split('</article>')

# Create a dictionary (article name: article contents) if needed
dict = {}
for d in documents:
    alku = d.find("<article name=")
    loppu = d.find('">')
    name = d[16:loppu]
    text = d[loppu + 2:]
    dict[name] = text

def read_article(title):
    if title in dict.keys():
        print("\n*****************************************")
        print("\n" + title)
        print(dict.get(title))
        print("*****************************************\n")
    else:
        print("No such article found.")

# CREATING THE MATRIX

gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
g_matrix = gv.fit_transform(documents).T.tocsr()


def search_documents(query_string):
    # Vectorize query string
    query_vec = gv.transform([query_string]).tocsc()

    # Cosine similarity
    hits = np.dot(query_vec, g_matrix)

    # Rank hits
    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]),
                                       reverse=True)

    # Output result
    print("Your query '{:s}' matches the following documents:".format(query_string))
    count = 0
    for i, (score, doc_idx) in enumerate(ranked_scores_and_doc_ids):
        print("Matching article #{:d} (score: {:.4f}): {:s}".format(i, score, documents[doc_idx][15:200]) + "...")
        print()
        count += 1
        if count > 4:
            return print("Showing the first five of", len(ranked_scores_and_doc_ids), "articles.\n")

# MAKING QUERIES
print("Welcome to the search engine!")
print("Data: 1000 Wikipedia articles")
print("Number of terms in vocabulary:", len(gv.get_feature_names()))
print()
# Ask the user to type a query
query = str(input("Enter a query: "))
while query != "":
    try:
        search_documents(query)
        query = str(input("Enter a new query (enter blank if you want to quit): "))
    except KeyError:
        query = str(input("Your search failed. Try again: "))
    except IndexError:
        query = str(input("Word(s) not found. Try again: "))

else:
    print("Goodbye!")