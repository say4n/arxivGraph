#!/usr/bin/env python3

import urllib.request
import feedparser
import time
import json


def main():
    f = open("arxivData.json", "a")

    base_url = 'http://export.arxiv.org/api/query?'
    # search for CV,CL,AI,LG,NE,ML field papers
    search_query = 'cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML'

    start = 0
    max_results = 1000
    count = 0
    fail_count = 0

    result_list = []

    try:
        while start < 50000:
            query = 'search_query=%s&start=%i&max_results=%i' % (
                search_query, start, max_results)
            start = start + 1000

            feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
            feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

            response = urllib.request.urlopen(base_url+query).read()
            feed = feedparser.parse(response)

            for entry in feed.entries:
                # Arxiv id
                temp_sic = {}
                c1_data = str(entry.id.split('/abs/')[-1])

                # date
                c2_data = str(entry.published)
                year = int(str(c2_data[:4]))
                month = int(str(c2_data[5:7]))
                day = int(str(c2_data[8:10]))

                # Title
                c3_data = str(entry.title)

                # author
                c4_data = entry.authors

                # Pdf link
                c5_data = entry.links
                c6_data = entry.tags
                c7_data = str(entry.summary)

                temp_dic = {
                    "id": c1_data,
                    "year": year,
                    "month": month,
                    "day": day,
                    "title": c3_data,
                    "author": c4_data,
                    "link": c5_data,
                    "tag": c6_data,
                    "summary": c7_data
                }

                count += 1

                print(f"\r{count}", end="")

                data = json.dumps(temp_dic, indent=4)
                result_list.append(temp_dic)

            # time.sleep(5)
    except:
        json.dump(result_list, f, sort_keys=True, indent=4)
        f.close()

    #json.dumps(result_list, f, indent=4)
    json.dump(result_list, f, sort_keys=True, indent=4)
    f.close()

    print(f'Final count: {count}')
    print('Connection is closed!')

    return None


if __name__ == "__main__":
    main()
