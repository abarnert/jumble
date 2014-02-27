#!/usr/bin/env python
"""jumble.py WORD [DICTFILE]

Searches for all anagrams that can be made from WORD or subsets of it
in the DICTFILE, which is a file in Unix dict format (one word per
line; does not have to be sorted).

If no DICTFILE is given, a file named "words" in the same
directory as the script will be used. (The repository has a copy of
the web2 dictionary, as found in the FreeBSD sources--which may
not be ideal, as it's from 1934, and includes words like "g".)

The comparison is a simple string match. This means it's case
sensitive, so anorak will not find Aaron. This also means you need
Python 3.1+ if you want to use Unicode word lists.

Example:

    $ ./jumble.py gram
	a
    ga
    g
    gam
    mag
    am
    ma
    m
    gram
    arm
    mar
    ram
    gar
    gra
    rag
    ar
    ra
    r

If you use it to cheat at Scrabble, you're only cheating
yourself. (Also, a better Scrabble cheater would give you some way to
specify that certain letters are required, or, even better, required
at specific positions.)
"""

import collections

def group(iterable, key):
    """group([1, 2, -3, -2], abs) -> {1: [1], 2: [2, -2], 3: [-3]}"""
    d = collections.defaultdict(list)
    for element in iterable:
        d[key(element)].append(element)
    return d

def powerset(seq):
    """powerset([1, 2] -> () (1,) (2,) (1,2)"""
    if seq:
        first, rest = seq[0], seq[1:]
        yield first
        for subset in powerset(rest):
            yield first + subset
            yield subset

def unique(iterable):
    """unique('abcbcdcde') -> a b c d e"""
    seen = set()
    for element in iterable:
        if element not in seen:
            yield element
            seen.add(element)

def sortword(word):
    return ''.join(sorted(word))

def jumble(words, word):
    """Yield all words in the iterable words that are (partial) anagrams
    of word."""
    # For smallish words and a largish wordlist, grouping the wordlist
    # and iterating the powerset of the word's letters will be much
    # faster than iterating the wordlist and testing each against the
    # letters; for huge words, the reverse is true. See README.md for
    # more details.
    if len(word) < 12:
        subsets = unique(powerset(sortword(word)))
        words = group(words, sortword)
        for subset in map(''.join, subsets):
            for word in words[subset]:
                yield word
    else:
        letters = collections.Counter(word)
        def match(w):
            return not collections.Counter(w) - letters
        for m in filter(match, words):
            yield m

if __name__ == '__main__':
    import os.path
    import sys
    word = sys.argv[1]
    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = os.path.join(os.path.dirname(__file__), 'words')
    with open(path) as f:
        words = map(str.strip, f)
        for word in jumble(words, sys.argv[1]):
            print(word)
                    
