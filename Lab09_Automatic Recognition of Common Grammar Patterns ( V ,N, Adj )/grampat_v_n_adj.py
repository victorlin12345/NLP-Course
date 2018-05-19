import sys
from collections import defaultdict
from pprint import pprint
# from pgrules import isverbpat
pgPreps = 'in_favor_of|_|about|after|against|among|as|at|between|behind|by|for|from|in|into|of|on|upon|over|through|to|toward|towarV in favour of	ruled in favour ofV in favour of	ruled in favour ofds|with'.split(
    '|')
otherPreps = 'out|down'.split('|')
verbpat = ('V; V n; V ord; V oneself; V adj; V -ing; V to v; V v; V that; V wh; V wh to v; V quote; ' +
           'V so; V not; V as if; V as though; V someway; V together; V as adj; V as to wh; V by amount; ' +
           'V amount; V by -ing; V in favour of n; V in favour of ing; V n in favour of n; V n in favour of ing; V n n; V n adj; V n -ing; V n to v; V n v n; V n that; ' +
           'V n wh; V n wh to v; V n quote; V n v-ed; V n someway; V n with together; ' +
           'V n as adj; V n into -ing; V adv; V and v').split('; ')
verbpat += ['V %s n' % prep for prep in pgPreps] + ['V n %s n' % prep for prep in verbpat]
verbpat += [pat.replace('V ', 'V-ed ') for pat in verbpat]
reservedWords = 'how wh; who wh; what wh; when wh; someway someway; together together; that that'.split('; ')
pronOBJ = ['me', 'us', 'you', 'him', 'them']

pgNoun = ('N for n to v; N from n that; N from n to v; N from n for n; N in favor of; N in favour of; ' +
          'N of amount; N of n as n; N of n to n; N of n with n; N on n for n; N on n to v' +
          'N that; N to v; N to n that; N to n to v; N with n for n; N with n that; N with n to v').split('; ')
pgNoun += pgNoun + ['N %s -ing' % prep for prep in pgPreps]
pgNoun += pgNoun + ['ADJ %s n' % prep for prep in pgPreps if prep != 'of'] + ['N %s -ing' % prep for prep in pgPreps]

pgAdj = ('ADJ adj; ADJ and adj; ADJ as to wh; ' +
         'ADJ enough; ADJ enough for n; ADJ enough for n to v; ADJ enough n; ' +
         'ADJ enough n for n; ADJ enough n for n to v; ADJ enough n that; ADJ enough to v; ' +
         'ADJ for n to v; ADJ from n to n; ADJ in color; ADJ -ing; ' +
         'ADJ in n as n; ADJ in n from n; ADJ in n to n; ADJ in n with n; ADJ in n as n; ADJ n for n' +
         'ADJ n to v; ADJ on n for n; ADJ on n to v; ADJ that; ADJ to v; ADJ to n for n; ADJ n for -ing' +
         'ADJ wh; ADJ on n for n; ADJ on n to v; ADJ that; ADJ to v; ADJ to n for n; ADJ n for -ing').split('; ')
pgAdj += ['ADJ %s n' % prep for prep in pgPreps]
# pgPatterns = pgVerb + pgAdj + pgNoun
verbpat = verbpat + pgAdj + pgNoun
defaultMap = {'NP': 'n', 'VP': 'v', 'JP': 'adj', 'ADJP': 'adj', 'ADVP': 'adv', 'SBAR': 'that', }

headPat = ['V', 'N', 'J']


def isverbpat(pat):
    return pat in verbpat


maxDegree = 9


def sentence_to_ngram(words, lemmas, tags, chunks):
    return [(k, k + degree) for k in range(1, len(words)) for degree in range(2, min(maxDegree, len(words) - k + 1))]
    #                 if chunks[k][-1] in ['H-VP', 'H-NP', 'H-ADJP']
    #                 and chunks[k+degree-1][-1] in ['H-VP', 'H-NP', 'H-ADJP', 'H-ADVP'] ]


mapHead = dict([('H-NP', 'N'), ('H-VP', 'V'), ('H-ADJP', 'ADJ'), ('H-ADVP', 'ADV'), ('H-VB', 'V'), ])
# mapRest = dict( [('H-NP', 'n'), ('H-VP', 'v'), ('H-TO', 'to'), ('H-ADJ', 'adj'), ('H-ADV', 'adv')] )
mapRest = dict(list(defaultMap.items()) + [('VBG', 'ing'), ('VBD', 'v-ed'), ('VBN', 'v-ed'), ('VB', 'v'), ('JJ', 'ADJ'), ('NN', 'n'), ('NNS', 'n'), ('RB', 'adv'),
                                           ])

mapRW = dict([pair.split() for pair in reservedWords])


def hasTwoObjs(tag, chunk):
    if chunk[-1] != 'H-NP':
        return False
    return (len(tag) > 1 and tag[0] in pronOBJ) or (len(tag) > 1 and 'DT' in tag[1:])


def chunk_to_element(words, lemmas, tags, chunks, i, isHead):
    # print ('***', i, words[i], lemmas[i], tags[i], chunks[i], isHead, tags[i][-1] == 'RP' and tags[i-1][-1][:2] == 'VB')
    if isHead:
        return mapHead[chunks[i][-1]] if chunks[i][-1] in mapHead else '*'
    if lemmas[i][0] == 'favour' and words[i - 1][-1] == 'in' and words[i + 1][0] == 'of':
        return 'favour'
    if tags[i][-1] == 'RP' and tags[i - 1][-1][:2] == 'VB':
        return '_'
    if tags[i][0][0] == 'W' and lemmas[i][-1] in mapRW:
        return mapRW[lemmas[i][-1]]
    if hasTwoObjs(tags[i], chunks[i]):
        return 'n n'
    if tags[i][-1] in mapRest:
        return mapRest[tags[i][-1]]
    if tags[i][-1][:2] in mapRest:
        return mapRest[tags[i][-1][:2]]
    if chunks[i][-1] in mapHead:
        return mapHead[chunks[i][-1]].lower()
    if lemmas[i][-1] in pgPreps:
        return lemmas[i][-1]
    return lemmas[i][-1]


def simplifyPat(pat):
    if pat == 'V ,':
        return 'V'
    else:
        return pat.replace(' _', '').replace('_', ' ').replace('  ', ' ')


def ngram_to_pat(words, lemmas, tags, chunks, start, end):
    pat, doneHead = [], False
    for i in range(start, end):
        isHead = tags[i][-1][0] in headPat and not doneHead
        pat.append(chunk_to_element(words, lemmas, tags, chunks, i, isHead))
        if isHead:
            doneHead = True
    pat = simplifyPat(' '.join(pat))
    # print ('===', start, end, pat, words[start:end])
    return pat if isverbpat(pat) else ''


def ngram_to_head(words, lemmas, tags, chunks, start, end):
    for i in range(start, end):
        if tags[i][-1][0] in 'V' and tags[i + 1][-1] == 'RP':
            return lemmas[i][-1].upper() + ('_' + lemmas[i + 1][-1].upper())
        if tags[i][-1][0] in headPat:
            return lemmas[i][-1].upper()


if __name__ == '__main__':
    for line in sys.stdin:
        # if "'out', 'in', 'favour', 'of'," not in line and "'down', 'in', 'favour', 'of'," not in line: continue
        parse = eval(line.strip())
        parse = [[y.split() for y in x] for x in parse]
        # pprint(parse)
        print ('\n' + ' '.join([' '.join(x) for x in parse[0]]))
        for start, end in sentence_to_ngram(*parse):
            pat = ngram_to_pat(*parse, start, end)
            if pat:
                print ('%s\t%s\t%s' % (ngram_to_head(*parse, start, end), pat, ' '.join([' '.join(x) for x in parse[0][start:end]])))
        # break
    # $ cat pgv.ex.tagged.txt | python grampat.py
    '''
mapMWE = defaultdict(str)
for x, y, z in [ 'in favour of;IN;H-PP'.split(';') for pair in reservedWords ]: mapRW[x] = ([y], [z])
def findSublist(words, pats):
    Ns = set([ x.count('_')+1 for x in pats.split(';')])
    pats = [ [ y.split() for y in x.split('_') ] for x in pats.split(';')]
    return [ (k, k+n, ' '.join( [ ' '.join(x) for x in pat ] ))
                for k in range(len(words)) for pat in pats for n in Ns if words[k:k+n] == pat ]
def merge_MWE(words, lemmas, tags, chunks, i, j, pat):
    return (words[:i]+[[pat]]+words[j:], lemmas[:i]+[[pat]]+lemmas[j:],
                tags[:i]+[mapRW[pat][0]]+tags[j:], chunks[:i]+[mapRW[pat][1]]+chunks[j:])
def merge_MWEs(words, lemmas, tags, chunks, matches):
    for i, j, pat in matches:
        words, lemmas, tags, chunks = merge_MWE(words, lemmas, tags, chunks, i, j, pat )
    return [words, lemmas, tags, chunks]
        #parse = merge_MWEs(*parse, findSublist(parse[0], 'in_favour_of' ))
    '''