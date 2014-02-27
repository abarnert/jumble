#!/usr/bin/env python

import collections
import os.path
import sys
import jumble

path = os.path.join(os.path.dirname(__file__), 'words')
with open(path) as f:
    words = {line.strip() for line in f}

letters = collections.Counter()
for word in words:
    letters |= collections.Counter(word)
letters = ''.join(letters.elements())
#letters = '-ACBEDGFIHKJMLONQPSRUTWVYXZaaaaaacccccbbbbeeeeeeedddddggggffffiiiiiihhhhkkkkjjmmmmllllloooooonnnnnnqqppppssssssssrrrruuuuutttttwwwvvvyyyyxxzzz'

print("{} words, requiring '{}'".format(len(words), letters))

anagrams = set(jumble.jumble(words, letters))
if anagrams != words:
    print('error, only {} anagrams found'.format(len(anagrams)))
    #for missing in sorted(words - anagrams):
    #    print(missing)
