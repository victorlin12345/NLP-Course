Auto Collocation Extraction ( based on Smadja ) 

參考網址：[https://blog.csdn.net/jinping_shi/article/details/61203395](https://blog.csdn.net/jinping_shi/article/details/61203395)

### 搭配詞（collocation）: 
是指 兩個或多個詞 語言習慣性結合在一起表示某種特殊意義的詞彙。

```
e.g.

sit in traffic，表示堵車或者在通勤上花費了非常多時間的意思

那麼sit_traffic就是一個搭配詞。

其中 sit 稱為 base word ，traffic 稱為 collocate.

所以 collocations = base word + collocate .

```
> 1. 前面的例子中介詞in去哪裡了呢？研究搭配詞時通常只研究base word和collocate兩個單詞。
> 2. 比如sit和traffic的collocation表示為(sit, traffic)，中間的單詞都省略掉。
> 3. 這樣的表示類似bigram的形式，稱為skip bigram，即跳過（skip）中間的一些詞，只取首尾兩個詞記為bigram的形式。
> 4. 普通的bigram也是skip bigram的一種。(w,w1)
> 5. 雖然skip bigram跳過了中間的詞，但不意味著這部分信息丟失了。
> 6. skip bigram有個距離屬性， **表示skip bigram中首尾兩個詞相差多少個詞。e.g.( distance 5 : base word 位置 - collocate 位置 是  5 )** 
> 7. 兩個相連的詞構成的skip bigram距離是1，**比如sit in traffic的(sit, in)的距離為1，所以沒有距離為0的bigram！**
> 8. 但是有距離是負數的bigram，比如(in, sit)的距離為-1，表示sit應該在前面。
> 9. 對於英語，這個距離一般取5和-5.

### Smadja algorithm:

- 基於ngram距離運用統計來篩選 base word 最佳的 collocate

- 想法：
    1. collocation ( base_word + coll_1 ) 出現的頻率遠高於其他 collocation ( base_word + coll_N )
    2. ( base_word + coll_1 ) 在距離上的分佈 需有 峰值
    3. 最終，選 ( base_word + coll_1 ) 距離 峰值 作為 最佳

- 判斷搭配詞是否合理的三個 Condition
    1. C1 -> strength : freq_i - avg(freq) / σ (SD) >= k0
        - 篩掉在整個語料庫中出現頻率不高的搭配詞。
    2. C2 -> spread : V(σ^2) >= U0
        - collocation 在各個距離，頻率分佈的 SD。
    3. C3 -> peak : p_j >= avg(p_j) + k1 * SD
        - 合理的搭配詞一般在某個距離上出現的次數很多。
    4. 通常，k0 = 1, k1 = 1, U0 = 10

### Input:

1. citeseerx.ngms ( 1208723 筆 collocation with pos )

e.g.<br/>
```
your-pron vote-n on-prep the-det follow-v option-n	20
```

### Process:

1. 將 citeseerx.ngms 所有的 ngram 存其 skip bigram。

2. 只取用 akl ( base word list ) 中的 skip bigram。

3. 計算 各 base word condition要用的數值。

4. 將 skip bigram 透過 condition 篩掉即為結果。

### Output:

| base word | collocate | distence | strength | spread |    peak   | count |
|:---------:|:---------:|:--------:|:--------:|:------:|:---------:|:-----:|
|     :     |     :     |     :    |     :    |    :   |     :     |   :   |
|   works   |  previous |    -1    | 9.389265 |  14.84 |  5.452272 |   13  |
|   years   |     In    |    -2    | 7.349460 |  84.60 | 13.197826 |   31  |
|   years   |    ago    |     1    | 1.734851 |  10.89 |  4.400000 |   11  |
|   years   |    last   |    -2    | 7.155853 |  73.29 | 12.460958 |   28  |
|     :     |     :     |     :    |     :    |    :   |     :     |   :   |