## Word Level Spelling Check ( Beam Search )

speed up the performance

### pseudocode
```
def correction(word):
    states = [ <initial state> ]
    for i in range(len(word)):
        print(i, states[:3])
        STATES = < map the next_states function to each state in STATES
         to get a list (of lists) of states >
        < Combine states with the same L and R so the #edit is minimized >
        < Sort the states in STATES in increasing values of #edit first and
         then decreasing probability of state >
        < Prune STATES, leaving at most MAXBEAM number of states >
    <Filter STATES and keep only states with #edit==0 or probability>0>
    <If there are some plausible edited results (#edit>0 and probability>0
     then remove the state with #edit==0>
    return <the first three of plausible corrections sorted by probability>
```

### Input:

- big.txt

### Process: **( beam search )**

1. each step:

    1. next-state function : get all possible set prob.

    2. minimize the state : left the set STATES ( L + R )

    3. **sort the states in STATES in increasing values of edit and decreasing probability of state. And left top 500**

2. filter STATES and keep only states with edit==0 or probability>0, if there are some plausible edited results ( edit>0 and probability>0 ) then remove the state with edit == 0

### Output:

```
pprint(correction('appearant'))
[('appearance', '', 2, 1.6171794618080352e-05),
 ('appearing', '', 2, 1.2932266646492481e-05),
 ('apparent', '', 2, 9.415869018298948e-06)]

pprint(correction('writtung'))
[('written', '', 2, 9.567378187426671e-05),
 ('writing', '', 2, 8.114552263770321e-05),
 ('writting', '', 1, 2.116569911046786e-07)]

pprint(correction('bad'))
[('and', '', 2, 0.012681757364628494),
 ('a', '', 2, 0.008860475603882461),
 ('by', '', 2, 0.003268632889514475)]

...

```