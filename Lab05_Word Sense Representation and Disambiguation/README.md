Word Senser Representation And Disambiguation ( Logistic Regression )
藉由字的解釋和例句作為feature做分類器取機率配合language model(字可能的類)判斷字意
前提要有單字的解釋和例句

## What is Word Sense Disambiguation ?

- a content word W in context of a sentence CONT.
- W all potential senses from a sense inventory ( e.g. the WordNet )
- we are supposed to identify the intended sense of W in CONT from a senses(W).
- if we could perform WSD reliably on a large scale, the results definitely will help improve many important NLP tasks including : 
    - Machine translation
    - Question Answering
    - Determine the level of difficulty of words in a reader for learning a second language.

## There are four approaches to solving the WSD problem : 

- Supervised approach: 
This approach requires a training corpus (e.g., Semcor, http: //www.cse.unt.edu/~rada/downloads.html#semcor) of words tagged in context with intended senses. The training corpus can then be used to train a classifier that can tag words in a given new context.

- Dictionary-based approach (Lesk Algorithm): 
Choose sense with a definition that contains the most word overlap with the given context.

- Semi-Supervised approach:
Start with a very small hand-labeled seed-set(sentences/collocations associated with each word sense). Then rely on the "one sense per collocation" constraint to tag some sentences. Subsequently, identify more collocations in order to extend the sized of tagged part of the training data, until no more sentences can be tagged.

- Unsupervised approach: 
combined the information in Roget’s International Thesaurus with cooccurrence data from large corpora in order to learn disambiguation rules for Roget’s classes, which could then be applied to words.

## Supervised approach ( Logistic Regression )

### Input:

1. wn.in.evp.cat.txt
```
data format : word [tab] category [tab] senseDef_example [tab] sense_candidates

e.g.
abandon-v-1	get_rid_of.v.01	abandon||forsake, leave behind||We abandoned the old car in the empty parking lot	{'abandon-v-1': 'get_rid_of.v.01', 'abandon-v-2': 'abandon.v.02', 'abandon-v-3': 'leave.v.01', 'abandon-v-4': 'abandon.v.04', 'abandon-v-5': 'leave.v.02'}

```

### process:

1. Using Logistic Regression Model to predict word ( feature come from : sense & example )
    - train: 9/10 of wn.in.evp.cat.txt 
    - test: 1/10 of wn.in.evp.cat.txt 

p.s.
#### feature generate
- **TF-IDF** 
- 詞頻(term frequency，tf): 指某個字詞在該檔案中出現的次數/該檔案所有的字數量
- 逆向檔案頻率(inverse document frequency，idf): 某字在所有檔案出現次數/所有當檔案 稱為df，idf 則是 df取倒數後對其做log10
- tf-idf: tf * idf
- 例子：
>假如一篇檔案的總詞語數是100個，而詞語「母牛」出現了3次，那麼「母牛」一詞在該檔案中的詞頻就是3/100=0.03。而計算檔案頻率（IDF）的方法是以檔案集的檔案總數，除以出現「母牛」一詞的檔案數。所以，如果「母牛」一詞在1,000份檔案出現過，而檔案總數是10,000,000份的話，其逆向檔案頻率就是lg（10,000,000 / 1,000）=4。最後的tf-idf的分數為0.03 * 4=0.12。
- 在此作業中 tf ：我們將文件數看成 wncat ， 因此 tf 就是在字詞在各類 wncat 出現的次數/各類 wncat所有的字詞數量
- 在此作業中 df ：我們將文件數看成 wncat ， 因此 df 就是在字詞出現在幾個 wncat 中/ wncat類別總數
- 在此作業中 idf：df 倒數取log10

### output:

- non filting by candidates : 
```
accuracy : 0.6310344827586207
```
- filting by candidates :
```
accuracy : 0.7991379310344827
```




