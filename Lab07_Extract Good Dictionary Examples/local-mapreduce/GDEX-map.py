import re, sys

def tokens(str1): return re.findall('[a-z]+', str1.lower().strip())

def ngrams(sent, n):
    return [ ' '.join(x) for x in zip(*[sent[i:] for i in range(n) if i <= len(sent) ] ) ]

def good_coll_examples():
    good_colls = set()
    for line in open('bnc.coll.small.txt','r'):
        element = line.split('\t')
        good_colls.add((element[0],element[1],int(element[2])))
    return good_colls

good_coll_examples = good_coll_examples()

def is_good_coll(base_word, coll, dist):
    if (base_word, coll, dist) in good_coll_examples:
        return True    

for line in sys.stdin:
    sent = tokens(line)
    for n in range(2, 6):
        for ngram in ngrams(sent, n):
            ngram = ngram.split(' ')
            first = ngram[0]
            last = ngram[-1]
            if is_good_coll(first, last,(n-1)):
                print('%s_%s_%s\t%s' % (first, last,str((n-1)),line.strip()))
            if is_good_coll(last, first,(1-n)):
                print('%s_%s_%s\t%s' % (last, first,str((1-n)),line.strip()))
