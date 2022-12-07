# python src/p06b.py data/p06.txt

import sys
N = 14

def find_marker(signal):
    for idx in range(len(signal)):
        if idx < N:
            continue
        if len(set(signal[idx-N:idx])) < N:
            continue
        return idx

with open(sys.argv[1]) as fd:
    signal = fd.read()
    print(find_marker(signal))