## Sentence Level Spelling Check with Web Corpus ( NetSpeak API )

[NetSpeak](http://www.netspeak.org)

### Purpose : 1. Detection error 2. Correction error

### Type of Spelling ERRORS in context

- Non-word errors(from Birkbeck Spelling)

    - I felt very **strang**. -> I felt very **strange**.

- Real-word errors

    - at **bake** time. -> at **break** time.
    
### Detectng Spelling error in context

- Non-word errors

    - 1 gram counts ( if there is the word not in corpus: big.txt )

- Real-word errors

    - Use NetSpeak API ( the lower trigram count, the higher error probility )

    - eg. when the brake was finished: 
        
        - min(c(when the brake),c(the brake was),c(brake was finished))

### Correcting Spelling error in context

1. After detect where is the error, we can use lab3 to generate serveral candidates

2. Using NetSpeak API to choose the best correction.

    - replace the wrong word and pick the highest count

    - c( when the break was finished ) = c( when the break )*c( the break was )*c( break was finished )

### Input : 

- lab4.test.1.txt (format: wrong \t correct)

### Process :

1. find error trigram

2. correct error trigram

### Output : 
```
['felt very strang', 'field very strang', 'fell very strang', 'felt very strang', 'felt every strang', 'felt vary strang', 'felt very strange', 'felt very strong', 'felt very staring']
0 ---------------------------------------
Error: strang
Candidates: ['strange', 'strong', 'staring']
Correction: strange
i felt very strang  -> i felt very strange 
hits : 1


['and brake time', 'at brake time', 'it brake time', 'at break time', 'at broken time', 'at broke time', 'at brake time', 'at brake times', 'at brake them']
1 ---------------------------------------
Error: brake
Candidates: ['break', 'broken', 'broke']
Correction: break
at brake time  -> at break time 
hits : 2


['when the brack', 'went the brack', 'whom the brack', 'when the brack', 'when they brack', 'when then brack', 'when the black', 'when the back', 'when the branch']
2 ---------------------------------------
Error: brack
Candidates: ['black', 'back', 'branch']
Correction: black
when the brack was finished  -> when the black was finished 
hits : 2


['in the weanter', 'and the weanter', 'on the weanter', 'in the weanter', 'in they weanter', 'in then weanter', 'in the winter', 'in the water', 'in the weather']
3 ---------------------------------------
Error: weanter
Candidates: ['winter', 'water', 'weather']
Correction: water
in the weanter when it was snowing  -> in the water when it was snowing 
hits : 2

...

```





