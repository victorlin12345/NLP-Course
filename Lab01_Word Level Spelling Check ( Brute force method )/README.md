## Word Level Spelling Check ( Brute force method )

### Input:

- big.txt

### Process:

- get corpus unigram and bigram count (known)

- make a function for word possible edit set. Below are the situation that may do wrong in writing word. (eg. book) 
    1. delete : ook
    2. transpose : obok
    3. replace: [a~z]ook
    4. insert: [a~z]book

- get all possible result which in known and the highest Prob will be the answer

### Output:

```
correction('prepareq my')
('prepared', 'by')

correction('see yo')
('seem', 'to')

```







