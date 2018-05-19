#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

API_URL = "http://api.netspeak.org/netspeak3/search?query=%s"


class NetSpeak:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'}
        self.page = None

    def __getPageContent(self, url):
        return requests.get(url, headers=self.headers).text
        # return self.opener.open(url).read()

    def __rolling(self, url, maxfreq=None):
        if maxfreq:
            webdata = self.__getPageContent(url + "&maxfreq=%s" % maxfreq)
        else:
            webdata = self.__getPageContent(url)
        if webdata:
            # webdata = webdata.decode('utf-8')
            results = [data.split('\t') for data in webdata.splitlines()]
            results = [(data[2], float(data[1])) for data in results]
            lastFreq = int(results[-1][1])
            if lastFreq != maxfreq:
                return results + self.__rolling(url, lastFreq)
            else:
                return []
        else:
            return []

    def search(self, query):
        queries = query.split()
        new_query = []
        for token in queries:
            if token.count('|') > 0:
                new_query.append('[+{0}+]'.format('+'.join(token.split('|'))))
            elif token == '*':
                new_query.append('?')
            else:
                new_query.append(token)
        new_query = '+'.join(new_query)
        url = API_URL % (new_query.replace(' ', '+'))
        return self.__rolling(url)


if __name__ == "__main__":
    SE = NetSpeak()
    # Search_Result = SE.search("approach that *")
    # print Search_Result
    # at * time
    test = 'when the brake is finished'.split()
    print(test)
    # test = '? is finished'
    # test = 'brake is finished'

    for i in range(len(test) - 2):
        print(i)
        res = SE.search(' '.join(test[i:i + 3]))
        if res:
            print('\n'.join('\t'.join([str(y) for y in x]) for x in res))
        else:
            print('not found')
