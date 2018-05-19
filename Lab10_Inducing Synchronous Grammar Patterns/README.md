# Inducing Synchronous Grammar Patterns

### Purposes : 

- for Machine (Assisted) Translation and Bilingual Lexicography

- Translation tool： a database of bilingual text segments that could be reused in new translation projects.

- 找英文中心語所對應的中文、詞性 產生英文->中文文法規則
    - V about n|V n
    - care about the future | 關心未來

- 列出指定英文文法常見中文文法的轉換

------------------------

單字學習：bilingual 表示雙語 monolingual 單語  multilingual 多語

#### Monolingual Dictionary

- Consider ”finish” in a monolingual dictionary (Collins)

    1. [V -ing] (finish doing something) As soon as he’d **finished eating**, he excused himself.

    2. [V n] (finish something that you are making) The consultants had been working to **finish a report** this week.

#### Bilingual Dictionary

- Consider ”finish” in a bilingual dictionary (Collins)

    1. **V v-ing | v V** (FINISH v-ing | v+完) As soon as he’d finished eating, he excused himself. 他一吃完就告退。

    2. **V n | V n** (FINISH n | 完成 n) The consultants had been working to finish a report this week. 這些顧問本週一直在努力 完成一份報告。 

### Input : 

- UM-Corpus.en.200k.tagged : english corpus with pos

- UM-Corpus.ch.200k.tagged : chinese corpus

**以上為英中對照具語料**

- UM-Corpus.en.200k : english corpus only sentence

- align.final.200k : the bilingual index pairs

```
UM-Corpus.en.200k.tagged : 
[('all the commune members', ',', 'young and old', ',', 'went', 'out', 'to', 'hervest', 'the crops', '.'), 
('all the commune member', ',', 'young and old', ',', 'go', 'out', 'to', 'hervest', 'the crop', '.'),
('PDT DT JJ NNS', ',', 'JJ CC JJ', ',', 'VBD', 'RP', 'TO', 'VB', 'DT NNS', '.'),
('I-NP I-NP I-NP H-NP', 'O', 'I-NP I-NP H-NP', 'O', 'H-VP', 'H-PRT', 'H-TO', 'H-VP', 'I-NP H-NP', 'O')]

all[0] the[1] commune[2] members[3] ,[4]
young[5] and[6] old[7] ,[8]
went[9] out[10] to[11]
hervest[12]
the[13] crops[14]
.[15]

UM-Corpus.ch.200k.tagged : 
[0]全體_N [1]老少_N [2]社員_N [3]都_ADV [4]收割_V [5]莊稼_N [6]去_V [7]了_ASP [8]。_。

align.final.200k : 英-中

0-0 1-0 2-1 2-2 3-0 4-1 5-1 6-1 7-1 8-1 9-6 10-6 11-6 12-5 13-7 14-4 14-5 15-8

0-0 1-0 2-1 2-2 3-0 4-1 
0all-0全體 
1the-0全體
2commune-1老少
2commune-2社員 
3members-0全體
4,-1老少

5-1 6-1 7-1 8-1 
5young-1老少
6and-1老少
7old-1老少 
8,-1老少

9-6 10-6 11-6
9went-6去
10out-6去
11to-6去

12-5
12harvest-莊稼

13-7 14-4 14-5 
13the-7了
14crops-4收割  
14crops-5莊稼

15-8
15.-8。

```

- grampat: UM-Corpus.en.200k.tagged 產生 grammar pattern

- prons,HiFreWords : 用於選好的例句

### Process:

- 找出 英文文法 到各中文文法的次數，並用標準差去篩出常用的

eg. V N -> V p N

- 最後在運用 prons,HiFreWords 找出三個好的 english pat

## Output:

```

V n (121119)
-> V n (26889)
     authorized me 授權_V 我_N 
     keeping abreast 與時俱進_V 國際_N 
     leave any fingerprints 留下_V 指紋_N 
-> V (13617)
     adore everything 崇拜_V 
     be an aggregate 服務_V 
     constitute a crime 構成_V 
-> V v (10849)
     controlling aspects 上癮_V 上癮_V 
     explain everything 說明_V 詳細_V 
     give directions 指路_V 指路_V 
-> V n n (10192)
     buy insurance 買_V 保險_N 保險_N 
     decrease body fat 減少_V 脂肪_N 脂肪_N 
     don aboriginal dress 穿上_V 土著_N 居民_N 
-> V V n (8953)
     has abundant experience 擁有_V 豐富_V 經驗_N 
     having a love 有_V 有_V 愛_N 
     helped anchor Asia 幫助_V 掌握_V 亞洲_N 
-> V V V (3600)
     is a master 是_V 是_V 貼切_V 
     is gaining extensive attention 受到_V 廣泛_V 重視_V 
     make a house call 浴_V 出診_V 出診_V 
-> n V (3188)
     has clinical importance 糖尿病_N 重要_V 
     have access 他們_N 訪問_V 
     have control 你_N 控制_V 
-> n V n (2719)
     be an administrator 管理員_N 冒充_V 管理員_N 
     became a citizen 奧巴馬_N 加入_V 印尼_N 
     have both 你們_N 需要_V 你們_N 
-> V V n n (2628)
     do detailed bookkeeping 進行_V 詳細_V 簿記_N 工作_N 
     does have air conditioning 是_V 有_V 空調_N 空調_N 
     like learning foreign languages 想_V 學_V 外語_N 外語_N 
-> V n V (2533)
     include abdominal discomfort 包括_V 腹部_N 不適_V 
     involves a code change 涉及到_V 程式碼_N 更改_V 
     make a difference 有所_V 作為_N 有所_V 
-> n (2485)
     be coal 永遠_ADV 煤炭_N 
     can detect evidence 可以_ADV 跡象_N 
     held me 不只_ADV 我_N 
-> V n n n (2409)
     buy large agricultural machinery 購買_V 大型_N 農業_N 機械_N 
     hang epitaphs 懸掛_V 墓誌銘_N 槓架_N 結構_N 
     keeping kids 使_V 孩子_N 們_N 學校_N 
->  (2260)
     applying levels 將_ADV 
     can keep house 會_ADV 
     have an account 得_ADV 
-> V V V n (2041)
     are a common cause 是_V 是_V 常見_V 原因_N 
     has a marked influence 有_V 有_V 顯著_V 影響_N 
     have a distinct advantage 有_V 有_V 明顯_V 優勢_N 
-> n V V (1153)
     getting a date 瑪麗_N 約會_V 約會_V 
     initiate criminal action 刑事_N 訴訟_V 提起_V 
     make a call 你_N 大_V 需要_V 
-> V n V n (1089)
     avoid color changing 防止_V 顏色_N 發生_V 變化_N 
     gives a different answer 給出_V 主教_N 不同於_V 答案_N 
     has been a center 成為_V 奧克蘭_N 成為_V 中心_N 
-> n n (1082)
     felt hat 常_ADV 禮帽_N 圓頂_N 
     have fun 不必_ADV 娛樂_N 款_N 
     is advantage 尚_ADV 隱士_N 好處_N 
-> n n V (988)
     Blood gases analysis 血氣_N 血氣_N 分析_V 
     assign events 歷史_N 事件_N 發生_V 
     burn down houses 州官_N 州官_N 放火_V 
-> p V n (956)
     came form France 從_P 寄來_V 法國_N 
     has lost confidence 被_P 失去_V 信心_N 
     laid back its ears 向_P 收_V 兩耳_N 
-> n V n n (881)
     are called electronic effect 電子_N 總稱為_V 電子_N 效應_N 
     boost domestic demand 措施_N 促進_V 內需_N 內需_N 
     detailing actual expenditure 預算_N 實際_V 情況_N 支出_N 
-> V V V V (864)
     helps keep down floods 有助於_V 有助於_V 制止_V 制止_V 
     keep a man awake 使_V 不成_V 寐_V 寐_V 
     make an important decision 作出_V 重要_V 重要_V 決定_V 
-> p V (829)
     be choose 被_P 選拔出_V 
     be hand 被_P 勾結_V 
     cover increase 用_P 提高_V 
-> V p n (783)
     committed a breach 犯_V 在_P 罪_N 
     is drinking himself 喝_V 把_P 自己_N 
     is hand 是_V 用_P 手工_N 

```









