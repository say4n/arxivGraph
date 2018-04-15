#!/usr/bin/env python3

from collections import Counter
from config import *
from flask import Flask
from flask import request, render_template
import json
import pickle


with open(PROCESSED_DATA, "rb") as fp:
    exported_data = pickle.load(fp)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def index():
    pairs_sieved = exported_data["pairs_sieved"]
    authors_from_sieved_pairs = exported_data["authors_from_sieved_pairs"]

    author_list = list(map(str, authors_from_sieved_pairs.keys()))

    nodes = list(map(lambda author: {
                        "name": author,
                        "pubs": exported_data["authors"][author]/exported_data["most_published_author"]
                     },
                     author_list))

    edges = list(map(lambda link: {
                         "source"    : str(author_list.index(link[0])),
                         "target"    : str(author_list.index(link[1])),
                         "value"     : pairs_sieved[link]/exported_data["most_common_pair"]
                     },
                     pairs_sieved.keys()))

    nodelist = json.dumps({
        "nodes" : nodes,
        "links" : edges
    })

    constants = {
        "COLAB_THRESHOLD": exported_data["COLAB_THRESHOLD"]
    }

    return render_template('index.html',
                           nodelist=nodelist,
                           constants=constants)


if __name__ == "__main__":
    app.run(debug=True)
