Automatic recognition of common  ( N, V, ADJ )
從大量文本中為名詞、動詞、形容詞自動找出常用的文法及例句

### Training

#### Input:

1. UM-Corpus.en.200k.tagged.txt ( 未處理過的sentence with POS )

#### Process:

1. 將 lab8 的 grampat.py 改寫成吐出 n, adj 的 pattern 的     grampat_v_n_adj.py 

2. 利用 grampat_v_n_adj.py 對 Input 產生 pattern grammar。
    指令：
    ```
    cat UM-Corpus.en.200k.tagged.txt | python3 grampat_v_n_adj.py >> o.txt
    ```
    結果：
    ```
    all that remains for me to do is to say good-bye .[ sentence ]
    REMAIN	V for n	remains for me
    BE	V to v	do is to say
    SAY	V n	say good-bye
    [ grammar pattern (verb, pattern, example) ]
    ```
3. 選出各 base word ( N, V, ADJ ) 常見的 grammar 並 選出好的例句
    1. 將各個 baseword 所有的 grammar 統計 各 grammar 的 exaple 數，並運用標準差1 可以挑出對於 baseword 重要的 grammar  
    2. 因為有些較短的 grammar 必定較多句，**故在篩選時，乘上 gramma 長度(eg. V wh to v 長度4)可幫助顯現長gramma**
    2. 並對於好的 grammar 中所有 example 用 computeScore 找出最佳例句

#### Output:

```

ABILITY
N to v (468) its bulk and ability to fly

CLASSIFY
V by n (3) classified by BS 2916
V into n (8) are classified into groups
V as n (12) are classified as action
V n (20) can manually classify these content items


USEFUL
ADJ in n (18) very useful in business
ADJ to v (30) useful to have
ADJ as n (8) useful as a debugging aid
ADJ for n (20) especially useful for batch operations
ADJ to n (14) useful to management

DISCUSS
V in n (57) will discuss in detail
V n (270) concerned may have and discuss them
V adv (31) will discuss later
V wh to v (15) discuss how to eliminate

```