#!/usr/bin/env python3
"""
Topy (anagram of "typo") is a Python script to fix typos in text, based on
the RegExTypoFix project from Wikipedia and AutoWikiBrowser.

Topy requires BeautifulSoup version 4 and runs with either Python 2 and 3.

Usage: ./topy.py /path/to/files
NB! Files will be changed in place (overwritten)

See:
* https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
* https://github.com/intgr/topy
"""

# TODO: clean this crappy code up!

from __future__ import unicode_literals
import os
import regex
import sys

from bs4 import BeautifulSoup


RETF_FILENAME = 'retf.txt'

path = os.path.join(os.path.dirname(__file__), RETF_FILENAME)
soup = BeautifulSoup(open(path))

disabled = 0
errors = 0
parsed = 0

regs = []
my_disable = {
    "Etc.",
    "e.g.",
    "i.e.",
    "Currency symbol before number",
    "et al.",
    " ,",
    "F (farad)",  # replaces .nf => .nF ?!?
    "Newly",      # replaces newly-created => newly created
    "Recently",   # recently-commtted => recently committed, breaks "least-recently-used"
    "Highly",
    "exactly the same",  # only stylistic
}

for typo in soup.findAll('typo'):
    if 'word' not in typo.attrs or typo.attrs['word'] in my_disable:
        disabled += 1
        continue

    word = typo.attrs['word']
    find = typo.attrs['find'].encode('utf8')
    replace = typo.attrs['replace'].encode('utf8')

    try:
        r = regex.compile(find)
        # Use \1 instead of $1 etc
        replace = replace.replace(b'$', b'\\')

        regs.append((word, r, replace))
        parsed += 1
    except regex.error as err:
        #print("cannot compile %s %r: %s" % (word, find, err))
        errors += 1

print("Loaded %d rules (%d errors, %d disabled)" % (parsed, errors, disabled))


for fn in sys.argv[1:]:
    try:
        with open(fn, 'rb') as f:
            text = f.read()
    except (IOError, OSError) as err:
        print("Cannot open %r: %s" % (fn, err))

    total = 0
    for word, r, replace in regs:
        #print(word, r, replace)
        try:
            newtext, count = r.subn(replace, text)
            if count > 0 and newtext != text:
                total += count
                print("%s: replaced %s x %d" % (fn, word, count))
            text = newtext
        except regex.error as err:
            print("%s: error replacing %s (%r=>%r): %s" % (fn, word, r, replace, err))

    if total > 0:
        print("Writing %s" % fn)
        with open(fn, 'wb') as f:
            f.write(text)
