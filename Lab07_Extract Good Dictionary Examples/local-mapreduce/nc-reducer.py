import sys
from collections import Counter, defaultdict
ngm_count = defaultdict(lambda:defaultdict(lambda:0))
for line in sys.stdin:
    ngm, count = line.split('\t'); n = ngm.count(' ')+1 
    ngm_count[n][ngm] += int(count)

for n in range(2, 6):
    for ngm in ngm_count[n]:
        if ngm_count[n][ngm] >= 1:
            print( '%s\t%s' % (ngm, ngm_count[n][ngm]) )