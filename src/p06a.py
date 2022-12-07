# python src/p06a.py data/p06.txt

import sys
N = 4

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