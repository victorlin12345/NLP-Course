
# coding: utf-8

# ## Channel Probability

# In[2]:


count = {}
correct = {}
for line in open('count_1edit.txt', 'r'):
    w = line.split('\t')[0].split('|')[0]
    c = line.split('\t')[0].split('|')[1]
    p = int(line.split('\t')[1].rstrip('\n'))
    count[(w,c)] = p
    if c not in correct:
        correct[c] = p
    else:
        correct[c] = correct[c] + p


# In[3]:


N_all = len(count.keys())


# In[4]:


N_0 =  (26*26*26*26 + 2*26*26*26 + 26*26) - N_all


# In[5]:


def r_word_amount(r):
    total = 0
    for v in list(count.values()):
        if v == r:
            total = total + 1
    return total


# In[6]:


N_r = [ N_0 if r == 0 else r_word_amount(r) for r in range(12) ]



# In[7]:


def Pedit(w, c):
    if (w,c) not in count:
        if c not in correct:
            return 10**(-30) # 為避免分母為0，遇到這種就直接回傳一個很小的數字
        return 1/(correct[c]+N_r[1])
    else:
        if count[(w, c)] > 10:
            return count[(w, c)]/correct[c]
        else:
            return (count[(w, c)]+1)/(correct[c] + N_r[count[(w, c)]])


# - 未看過且未有correct的，無法使用laplace，因此給一個極小數即可

# In[8]:


# Pedit("-","*")


# - 未看過但correct有出現得（laplace 0->1）

# In[9]:


# Pedit("-","i")


# - 有出現在裡面的

# In[10]:


# Pedit("c","i") #count < 10


# In[11]:


# Pedit("e","i")


# ## Word Probabilty

# In[12]:


from collections import Counter, defaultdict
import re

'''Word Probability'''
def words(text): return re.findall(r'\w+', text.lower())
count_word = Counter(words(open('big.txt').read()))

Nw = sum(count_word.values())

Pdist = {word: float(count)/Nw for word, count in count_word.items()}

def Pw(word): 
    return Pdist[word] if word in Pdist else 10/10**len(word)/Nw


# In[13]:


'''Next States'''
letters    = 'abcdefghijklmnopqrstuvwxyz'
# state 是一個tuple
def next_states(state):
    # appearant
    L, R, edit, pw, pedit = state
    R0, R1 = R[0], R[1:]
    if edit == 2: return [(L+R0, R1, edit, pw, pedit*0.8)]
    # ('a', 'ppearant', 0, 0.0, (w,c))
    noedit = [(L+R0, R1, edit, pw, pedit*0.8)]
    # ('', 'ppearant', 1, 0.0, (R0,'')) 
    delete = [(L, R1, (edit + 1), Pw((L + R1)), pedit*Pedit(L[-1:]+R0, L[-1:]))]
    #('a', 'ppearant', 1, 0.0, (L + R0, L + c))
    replace = [(L + c, R1, (edit + 1), Pw((L + c + R1)), pedit*Pedit(R0,c)) for c in letters]
    #('aa', 'ppearant', 1, 0.0, (L + R0 ,L + R0 + c))          
    insert  = [(L + R0 + c, R1, (edit + 1), Pw((L + R0 + c + R1)), pedit*Pedit(R0,R0 + c)) for c in letters]
    
    transpose = [(L+R1[0], R0+R1[1:], (edit+1), Pw(L+R1[0]+R0+R1[1:]), pedit*Pedit(R0+R1[0], R1[0]+R0))] if len(R1) > 0 else []    
    
    return noedit + delete + replace + insert + transpose 


# In[14]:


# state = ('', 'appearant', 0, Pw('appearant'),1)
# next_states(next_states(state)[0])[:10]


# In[15]:


def combine_L_R(states):
    word_tuple = {}
    for L, R, edits, p, pw in states:
        word = L + R
        state = (L, R, edits, p, pw)
        if word not in word_tuple:
            word_tuple[word] = state
        elif edits < word_tuple[word][2]: #edit 次數較小的
            word_tuple[word] = state
    return list(word_tuple.values()) 


# In[16]:


import math
'''Combining channel probability with word probability to score states'''
def P(pw, pedit):
    if pw != 0 and pedit != 0:
        return math.log10(pw) + math.log10(pedit)
    elif pw != 0 and pedit == 0:
        return math.log10(pw)
    elif pw == 0 and pedit != 0:
        return math.log10(pedit)
    else:
        return 0


# In[17]:


from operator import itemgetter

def sort_state(states):
    tmp = {}
    sorted_by_prob = []
    for s in states:
        tmp[s] = P(s[3],s[4])
    sorted_by_prob_map = sorted(tmp.items(),key=itemgetter(1),reverse = True)
    for i in sorted_by_prob_map:
        sorted_by_prob.append(i[0])
    return sorted(sorted_by_prob,key=itemgetter(2))


# In[18]:


def filter_state(states):
    st = states
    for index, state in enumerate(states):
        if (state[2] != 0) and (P(state[3],state[4]) <= 0):
            print(state)
            del st[index] 
    return st


# In[19]:


MAXBEAM = 500
from pprint import pprint
def correction(word):
    states = [('', word, 0, Pw(word), 1)]
    for i in range(len(word)):
        #print(i, states[:3])
        states = [ state for states in map(next_states, states) for state in states ]
        states = combine_L_R(states) 
        states = sort_state(states)[:MAXBEAM]
        # filter_state(states)

    states = sorted(states, key=lambda x: P(x[3],x[4]), reverse=True)
    return states[:3]
    