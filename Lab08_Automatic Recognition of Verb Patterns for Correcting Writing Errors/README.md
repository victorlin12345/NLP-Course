Automatic Recognition of Verb Patterns for correcting writing errors
判斷常見文法錯誤機率（錯-> 對) nosiy channel 配合 language model機率 (make -> V N, V for N)
兩者機率相乘 最高為更正結果
### Training

#### Input:

1. ef_train.src.tagged.txt (錯的句子)

2. ef_train.tgt.tagged.txt (修正後的句子)

#### Process:

1. 利用 grampat.py 對 Input 產生 pattern grammar。
    1. ef_train.src.tagged.txt -> wrong.txt
    2. ef_train.tgt.tagged.txt -> correct.txt

2. 統計 修改前後的 pattern 並建立 Noisy Chennel Model 及 Lexical Language Model
    1. Noisy Chennel Model: e.g. P( V N | V about N ) [ wrong, correct ]
    2. Lexical Language Model: APPLY { 'V N', 'V to N', .. }
 
### Testing

#### Input:

1. ef_test.ref.txt ( 有答案 e.g. (ANSWER)	( V about n -> V n )[ wrong -> correct ] )

#### Process:

1. wrong 的 pattern 經過 Noisy Chennel Model 得出各 candidate pattern 的 NC_Prob

2. 各 candidate pattern 經 Lexical Language Model 得到 其 LL_Prob

3. 最高的 Candidate_Prob ( NC_Prob * LL_Prob ) 為修正結果


#### Output:

```
1 Correct
Answer: V to n
Pred : APPLY, (V for n -> V to n)
Prob : 0.0228

2 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

3 Correct
Answer: V to n
Pred : EXPLAIN, (V n -> V to n)
Prob : 1.0451

4 Correct
Answer: V for n
Pred : APPLY, (V n -> V for n)
Prob : 1.5425

5 Correct
Answer: V for n
Pred : APPLY, (V to n -> V for n)
Prob : 0.4998

6 Correct
Answer: V for n
Pred : APPLY, (V n -> V for n)
Prob : 1.5425

7 Correct
Answer: V for n
Pred : APPLY, (V n -> V for n)
Prob : 1.5425

8 Correct
Answer: V for n
Pred : APPLY, (V to n -> V for n)
Prob : 0.4998

9 Correct
Answer: V for n
Pred : APPLY, (V n -> V for n)
Prob : 1.5425

10 Correct
Answer: V n
Pred : EXPLAIN, (V about n -> V n)
Prob : 0.4847

11 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

12 Correct
Answer: V to n
Pred : EXPLAIN, (V n that -> V to n)
Prob : 0.1839

13 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

14 Correct
Answer: V for n
Pred : APPLY, (V n -> V for n)
Prob : 1.5425

15 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

16 Correct
Answer: V for n
Pred : APPLY, (V to n -> V for n)
Prob : 0.4998

17 Correct
Answer: V for n
Pred : APPLY, (V to n -> V for n)
Prob : 0.4998

18 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

19 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

20 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

21 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

22 Correct
Answer: V n
Pred : DISCUSS, (V about n -> V n)
Prob : 0.9069

23 Correct
Answer: V to n
Pred : EXPLAIN, (V n -> V to n)
Prob : 1.0451

24 Correct
Answer: V for n
Pred : APPLY, (V to n -> V for n)
Prob : 0.4998

25 Correct
Answer: V n
Pred : ANSWER, (V of n -> V n)
Prob : 0.3054

26 Correct
Answer: V n
Pred : ANSWER, (V to n -> V n)
Prob : 1.7016

27 Correct
Answer: V n
Pred : ANSWER, (V about n -> V n)
Prob : 1.5009

28 Correct
Answer: V n
Pred : ANSWER, (V about n -> V n)
Prob : 1.5009

29 Correct
Answer: V n
Pred : ANSWER, (V to n -> V n)
Prob : 1.7016

hit = 29, total = 29, accuracy = 1.000000
```