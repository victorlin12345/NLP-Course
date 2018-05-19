
# coding: utf-8

# ## skip bigram are filled into the dict


raw_data = [line.strip().split('\t') for line in open('citeseerx.ngms','r')]



from collections import defaultdict, Counter

skipBigramDistance = defaultdict(lambda:defaultdict(Counter))


def read_ngrams(raw_data):
    for sentence, freq in raw_data:
        ngram = sentence.split(' ')
        count = int(freq)
        skipBigramDistance[ngram[0]][ngram[-1]] += Counter({len(ngram)-1: count})
        skipBigramDistance[ngram[-1]][ngram[0]] += Counter({1-len(ngram): count}) 




read_ngrams(raw_data)



# ## filter by λ1 and λ3 filtering parameter for collocates and positions
# - λ1: strength of wi, ki = (freqi − freq)/σ > λ1
# - λ3: in pi peak frequency of j such that pij > avg(pi) + λ3*Vi^(1/2)
# <br>[Vi : 在 pi 中 所有數的標準差]
# <br>Smadja (1993) suggested using the setting of (λ1, λ2, λ3) = (1, 10, 1) for better results.
# <br>
# 變異數 Vi sigma^2 開更號 = 標準差
# ![Alt text](SD.jpg)

import akl as a


import numpy as np
skip_bigram_abc = defaultdict(lambda: 0)

max_distance = 5

for word, vals in skipBigramDistance.items():
    count = []
    if word in a.akl:
        for coll, val in vals.items():
            c = val.values()
            c_bar = sum(c) / (2*max_distance)
            skip_bigram_abc[(word, coll, 'freq')] = sum(c)
            skip_bigram_abc[(word, coll, 'spread')] = ((sum([x**2 for x in c]) - 2*c_bar*sum(c) + 2*max_distance*c_bar**2) / (2 * max_distance))**(0.5)
            count.append(sum(c))
        skip_bigram_abc[(word, 'avg_freq')] = np.mean(count)
        skip_bigram_abc[(word, 'dev')] = np.std(count)


# - output 格式不拘，主要會看搭配詞 (包含距離、count) 及對應的 ngram
# - 以 role-n 這個 head word 舉例，擷取出的搭配詞有18個
# - 依 count 高低排序印出的結果如下圖～


import math
k0 = 1
U0 = 10
k1 = 1

def skip_bigram_filter(skip_bigram_info, skip_bigram_abc):
    cc = defaultdict(lambda: [])
    for word, vals in skip_bigram_info.items():
        f = skip_bigram_abc[(word, 'avg_freq')]
        for coll, val in vals.items():
            if skip_bigram_abc[(word, 'dev')]-0 < 1E-6:
                strength = 0
            else:
                strength = (skip_bigram_abc[(word, coll, 'freq')] - f) / skip_bigram_abc[(word, 'dev')]
            if strength < k0:
                continue
            spread = skip_bigram_abc[(word, coll, 'spread')]
            if spread < U0:
                continue
            c_bar = sum(val.values()) / (2*max_distance)
            peak = c_bar + k1 * math.sqrt(spread)
            for dist, count in val.items():
                if count >= peak:
                    cc[word].append((coll, dist, strength, spread, peak, count))
    return cc

cc = skip_bigram_filter(skipBigramDistance, skip_bigram_abc)


import pandas
def word_coll(word):
    sort_by_f = sorted(cc[word], key=lambda tup: tup[5], reverse = True)
    collocations_df = pandas.DataFrame(sort_by_f,
                                   columns = ['collocate', 'distance', 'strength', 'spread', 'peak', 'p'])
    return collocations_df


pprint(word_coll('role-n'))





