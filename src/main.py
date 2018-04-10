#!/usr/bin/env python3

from collections import Counter
from itertools import combinations
import json


ARXIV_DATA = "data/arxivData.json"


with open(ARXIV_DATA, "rt") as f:
    data = json.load(f)
 

def get_authors(papers):
    """Get all authors from metadata"""
    authors, pairs = list(), dict()

    for paper in papers:
        paper_authors = paper["author"]
        paper_authors = set(map(lambda author: author['name'], paper_authors))

        if len(paper_authors) > 1:
            for peers in combinations(paper_authors, len(paper_authors)-1):
                author = list(paper_authors - set(peers))[0]
                
                try: 
                    pairs[author].extend(peers)
                except KeyError:
                    pairs[author] = list()
                    pairs[author].extend(peers)

        authors.extend(paper_authors)
        
    return Counter(authors), pairs


if __name__ == "__main__":
    print(f"Loaded {len(data)} papers.")

    authors, pairs = get_authors(data)
    print(f"{len(authors)} unique authors & {len(pairs)} unique pairs in the dataset.")

    top_n = 5
    print(f"Top {top_n} most common authors are:")

    for key, val in authors.most_common(top_n):
        print(f"{key}\t:\t{val}")

