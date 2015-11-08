# bm25-document-ranking-algorithm
BM25 Document Ranking Algorithm

In information retrieval, Okapi BM25 (BM stands for Best Matching) is a ranking function used by search engines to rank matching documents according to their relevance to a given search query. It is based on the probabilistic retrieval framework developed in the 1970s and 1980s by Stephen E. Robertson, Karen Spärck Jones, and others.

The name of the actual ranking function is BM25. To know more about BM25, visit 'https://en.wikipedia.org/wiki/Okapi_BM25'.

This program implements BM25 algorithm in python. The corpus used is a collection of Marvels & DC Comics superhero's wikipedia pages in text files.

Inverted index is calculated for the first time only. After than it is only written if there is any changes in the document set.
