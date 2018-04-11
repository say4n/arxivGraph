#!/usr/bin/env python3

from collections import Counter
from itertools import combinations
import json


ARXIV_DATA = "data/arxivData.json"
TOP_N = 10
COLAB_THRESHOLD = 5


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

    authors, colabs = get_authors(data)
    print(f"{len(authors)} unique authors & {len(colabs)} unique colabs in the dataset.")

    print(f"\nTop {TOP_N} most common authors are:")
    for key, val in authors.most_common(TOP_N):
        print(f"{key}\t:\t{val} papers")

    pairs = list()

    for (author, peers) in colabs.items():
        pairs_t = (tuple(sorted([author, peer])) for peer in peers)
        pairs.extend(pairs_t)

    pairs = Counter(pairs)

    print(f"\nTop {TOP_N} most common author pairs are:")
    for key, val in pairs.most_common(TOP_N):
        print(f"{key}\t:\t{val//2} colabs")

    
    pairs_sieved = dict()
    for key, val in pairs.items():
        if val >= COLAB_THRESHOLD:
            pairs_sieved[key] = val

    print(f"\n{len(pairs_sieved)} pairs have >= {COLAB_THRESHOLD} contribs.")

