jumble
======

Simple anagram finder: finds all words in a wordlist that are anagrams
or partial anagrams of an input word. See docstring in source for
details.

Requires Python 2.5+, or 3.1+ if you want it to work well with
Unicode. (It may also be slightly more efficient with 3.x.)

The included words file is the web2 wordlist from the FreeBSD
repository. From its README:

> Welcome to web2 (Webster's Second International) all 234,936 words worth.
> The 1934 copyright has lapsed, according to the supplier.  The
> supplemental 'web2a' list contains hyphenated terms as well as assorted
> noun and adverbial phrases.  The wordlist makes a dandy 'grep' victim.
>
>     -- James A. Woods    {ihnp4,hplabs}!ames!jaw    (or jaw@riacs)

Implementation 
=== 

By definition, iterating over all partial
permutations of the input word and looking each one up in the set of
words will give you all anagrams. But that's inefficient--if the word
has `N` distinct characters, it's `O(N!)`. (There's also a factor for the
numnber of repeated characters, but let's ignore that; worst-case
behavior is when all of the characters are distinct.)

If we build a group dictionary, mapping each sorted word to the list
of words that sort that way, we only need to iterate over the powerset
of the sorted word, instead of its permutation set, which is much
better--`O(2**N)`.

If we instead just iterate the dict and look for matches within the
word, it becomes `O(N*M)`, where `M` is the size of the dict.

Normally, you don't consider exponential time to be good. But
considering the numbers we're likely to be dealing with, it's actually
much better. For example, for N=10 and M=235886, the powerset
algorithm is about 8x as fast. The cutoff seems to be around N=12+/-1
for any M in the range 20000-1000000. (The cutoff is lower if you use
PyPy instead of CPython, presumably because checking `Counter` subsets
gets an order of magnitude faster while dict lookups don't speed up at
all? But 12 still works fine.)
