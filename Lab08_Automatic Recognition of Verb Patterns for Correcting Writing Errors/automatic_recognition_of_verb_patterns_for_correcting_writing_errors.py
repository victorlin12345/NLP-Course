
# coding: utf-8

'''
Explainable Artificial Intelligence:
- Method:  Correct the pattern using Noisy Channel Model
- Step:
    - Parse sentence
    - Identify in/correct patterns (i.e., V about n): 
        - Compute Noisy Channel Model
        - V n → V about n [ P(W|c) ]
    - Compute Lexical Language Model
        - discuss: V n, V wh-to-inf, V n w [ P(pat_c|pat_c_s) ]
    - Combined both prob sorting the best candiadate
        - Noisy Channel Model * Lexical Language Model
'''

import subprocess
import operator
from collections import defaultdict


def cmd_line(line):
    try:
        output = subprocess.check_output(line, shell=True)
        print(line,'completed')
    except subprocess.CalledProcessError:
        print('Exception handled')


# 產生了 wong.txt
cmd_line('cat ef_train.src.tagged.txt | python3 grampat.py >> wrong.txt ')
# 產生了 correct.txt
cmd_line('cat ef_train.tgt.tagged.txt | python3 grampat.py >> correct.txt ')

# finding seg start position in sentence
def pattern_pos(sent1, sent2):
    lst = sent1.split()
    sublst = sent2.split()
    if len(lst) < len(sublst):
        lst, sublst = sublst, lst
    count = 0
    n = len(sublst)
    for i in range(len(lst)):
        for j in range(n):
            if lst[i] == sublst[j]:
                count += 1
            if count == n:
                return i - n + 1
    return -10

def generate_filter_data(file):
    
    sen_dict = defaultdict(lambda: [])

    for line in file:
        id, verb, pat, seg, sen = line.strip('\n').split('\t')
        position = pattern_pos(sen, seg)
        sen_dict[id].append((verb,position,pat))
    
    return sen_dict

wrong_dict = generate_filter_data(open('wrong.txt','r'))
correct_dict = generate_filter_data(open('correct.txt','r'))


# ### Noisy Channel

# from correct.txt each verb's pattern
candidate = defaultdict(lambda: defaultdict(int))
# (verb, wrong_pattern, correct_pattern )
corrected = defaultdict(lambda: defaultdict(int))

# start finding corrected pattern
for id, correct in correct_dict.items():
    wrong = wrong_dict[id]
    for c in correct:
        c_verb, c_position, c_pat = c
        candidate[c_verb][c_pat] += 1
        for w in wrong:
            w_verb, w_position, w_pat = w
            '''
            correcting conditions:
             1. same verb
             2. seg start position is allowed in 3 distance
             3. different gramma
             4. avoid matching wrong 
            '''  
            if (c_verb == w_verb) and (abs(c_position - w_position) <=3) and (c_pat != w_pat) and c not in wrong:
                #corrected[(c_verb, w_pat)][c_pat] += 1
                corrected[ w_pat][c_pat] += 1

# for smoothing: get the pattern amount of sum. e.g. sum of count 1 is 30
def corrected_amount_counter(_dict ,amount):
    total = 0
    for c_pats in list(_dict.values()):
        for v in list(c_pats.values()):
            if v == amount:
                total = total + 1
    return total

N_amount = [ 100000 if amount == 0 else corrected_amount_counter(corrected ,amount) for amount in range(12) ]

def smooth(count, r=10):
    if count <= r:
        return (count+1)*N_amount[count+1]/N_amount[count]
    else:
        return count

def Pedit(verb, pat):
    answers = {}
    if pat in corrected:
        for candidate_pat, count in corrected[pat].items():
            noisy_channel_prob = smooth(count)/sum(candidate[verb].values())
            if candidate_pat in candidate[verb]:
                language_prob = candidate[verb][candidate_pat]/sum(candidate[verb].values())
            else:
                language_prob = 1/sum(candidate[verb].values())
            candidate_prob = language_prob * noisy_channel_prob    
            answers[candidate_pat] = candidate_prob     
        best_candidate, prob = max(answers.items(), key=operator.itemgetter(1))
        return best_candidate, prob
    else:
        return (verb, pat)


def format_word(word):
    return word.strip('(').strip(')')

def correction():
    hit = 0
    index = 0
    for line in open('ef_test.ref.txt','r'):
        index += 1
        verb_test, patterns = line.strip('\n').split('\t')[1:]
        verb_test = format_word(verb_test)
        patterns = format_word(patterns)
        pat_w, pat_c = patterns.split('->')
        pat_c = pat_c.lstrip(' ')
        pat_w = pat_w.rstrip(' ')
        pat_best, prob  = Pedit(verb_test, pat_w)
        
        if pat_best == pat_c:
            hit += 1
            print('%d Correct' % index)
        else:
            print('%d Wrong' % index)
        
        prediction = '%s, (%s -> %s)' % (verb_test, pat_w, pat_best)
        print('Answer: %s' % pat_c)
        print('Pred : %s' % prediction)
        print('Prob : %.4f\n' % prob)

    total = index
    print('hit = %d, total = %d, accuracy = %f' % (hit, total, hit / total))

correction()




