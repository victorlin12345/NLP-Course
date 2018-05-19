Good Dictionary Examples
利用好的 grammar pattern 在大量文本中找出好的例句 
### command

source ,4 mapper ,8 reducer ,map program ,reduce program , output folder name
```
cat bnc.sents.txt | ./lmr 4m 8 'python3 GDEX-map.py' 'python3 GDEX-reduce.py' bnc.gdex

 * Output directory: bnc.gdex
 * Elasped time: 0:00:15 ( 直接跑上面的會給 Elasped time )
```

### Map

#### Input:

1. bnc.coll.small.txt ( collocations list )

    | first  	| last 	| distence 	| count (won't use) 	|
    |--------	|------	|----------	|-------------------	|
    | aacute 	| il   	| 1        	| 54                	|
    | aacute 	| cs   	| 1        	| 73                	|
    | aacute 	| luk  	| -1       	| 74                	|
    | :     	| :  	| :       	| :                 	|
2. bnc.sents.txt ( example sentence )

    e.g. <br/> 
    I watched Sir John take the path to Glastonbury and knew there was little in tracking him any further .

    Geraldine hoovered the living room and watered her plants .

    Environmentalists argue that in the West a similar crisis would result in parliamentary hearings and campaigns by pressure groups .
    ...

#### Process:

1. extract candidate examples by the collcation list.

### Output:

1. first_last_distance  sentence (format)

### Reduce

#### Process:

1.  Compute the score for example (word_loc - not_high_freq - prons)
    1. word_loc: the collocation position (in english, the more last word is more important)
    2. not_high_freq:  count of word not in HiFreWords.txt (good example should have lots of high frequency words)
    3. prons: count of prons (good example shouldn't have he, she, it, etc)

2. each collocation choose the highest score of example.

#### Output:

```
ability_cope_2	The nature of classroom interaction is one factor which may affect children 's ability to cope with explanations in the classroom .
ability_mixed_-1	Again , this is certainly a is often about in terms of mixed ability teaching .
able_provide_2	Party politics are a feature of life in local authorities and as an officer it is essential that you are able to provide and impartial advice .
able_read_2	Only in the last hundred years have most people in the developed world been able to read and write .
able_understand_2	It is n't coping with a person who is twice your age and beset by problems you have no hope of being able to understand .
academic_community_1	Earlier in this book , we saw that there is no single group which forms the academic community .
accept_fact_2	Do you accept that fact that it 's only a quarter of people ?
acceptable_perfectly_-1	The PG404 out at 4ppm ( pages per minute ) , and the output quality is perfectly acceptable .
access_equal_-1	In other words , a declaration of common ownership of the land of the gens does not imply free and equal access to all within the gens .
accessible_easily_-1	After researching the project for a year , Paul Vincent decided to look for premises with a shop that would make the centre easily accessible .
accommodation_temporary_-1	The Audit Commission has said that if all authorities did as well as the average , significant reductions could be made in the number of families living temporary accommodation .
accurate_picture_1	This information is essential not for good careers education but also to assist schools in providing an accurate picture of the local economic and business situation for their students .
```