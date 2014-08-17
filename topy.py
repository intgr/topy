#!/usr/bin/env python
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
import sys
import logging
import os
from optparse import OptionParser
from difflib import unified_diff

import regex
from bs4 import BeautifulSoup


RETF_FILENAME = 'retf.txt'
ENCODING = 'utf8'

# some rules are not working with regex or are not useful
disabled = {
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
    "of xxx of xxx",     # causes an infinite loop in regex?
    "Apache",
    "Arabic",
}


def load_rules(filename):
    """Load and parse rules from `filename`, returns list of 3-tuples [(name, regexp, replacement), ...]"""

    soup = BeautifulSoup(open(filename))
    regs = []

    n_disabled = 0
    n_errors = 0
    n_loaded = 0

    for typo in soup.findAll('typo'):
        if 'word' not in typo.attrs or typo.attrs['word'] in disabled:
            n_disabled += 1
            continue

        word = typo.attrs['word']
        find = typo.attrs['find']
        replace = typo.attrs['replace']

        try:
            r = regex.compile(find)
            # Use \1 instead of $1 etc
            replace = replace.replace('$', '\\')

            regs.append((word, r, replace))
            n_loaded += 1
        except regex.error as err:
            logging.debug("cannot compile %s %r: %s" % (word, find, err))
            n_errors += 1

    logging.info("Loaded %d rules (except %d errors, %d disabled)" % (n_loaded, n_errors, n_disabled))

    return regs


def read_text_file(filename):
    """Reads file `filename` and returns contents as Unicode string. On failure, returns None and logs error."""

    try:
        with open(filename, 'rb') as f:
            return f.read().decode(ENCODING)
    except (IOError, OSError) as err:
        logging.error("Cannot open %r: %s" % (filename, err))
    except UnicodeDecodeError:
        # We could implement configurable encodings or automatic fallback, but really, people should just quit that
        # nonsense and use UTF-8. If you have a valid use case, please open an issue and explain.
        logging.info("Skip %s" % filename)

    return None


def print_diff(filename, old, new):
    """Diffs the `old` and `new` strings and prints as unified diff to stdout."""

    # TODO: color output for terminals
    lines = unified_diff(old.splitlines(True), new.splitlines(True), filename, filename)
    sys.stdout.writelines(lines)


def handle_file(regs, filename):
    """Apply rules from `regs` to file `filename`

    If `apply` is True, the file is overwritten. Otherwise a unified diff is printed to stodut.
    """

    oldtext = text = read_text_file(filename)
    if not text:
        return

    replaced = 0
    for word, r, replace in regs:
        logging.debug(word, r, replace)
        try:
            newtext, count = r.subn(replace, text)
            if count > 0 and newtext != text:
                replaced += count
                logging.debug("%s: replaced %s x %d" % (filename, word, count))
            text = newtext
        except regex.error as err:
            logging.error("%s: error replacing %s (%r=>%r): %s" % (filename, word, r, replace, err))

    if replaced > 0:
        if opts.apply:
            logging.info("Writing %s" % filename)
            with open(filename, 'wb') as f:
                f.write(text.encode(ENCODING))
        else:
            print_diff(filename, oldtext, text)


parser = OptionParser(usage="%prog [options] FILES OR DIRECTORIES...")
parser.add_option("-q", "--quiet",
                  action='store_true', dest='quiet', default=False,
                  help="silence information messages")
parser.add_option("-a", "--apply",
                  action='store_true', dest='apply', default=False,
                  help="overwrite files in place")


def walk_dir_tree(dirpath):
    """Walk a directory tree, yielding files exclude hidden directories
       (*nix only), files and also binary files"""

    for root, dirs, files in os.walk(dirpath):
        dirs[:] = (d for d in dirs if not d.startswith("."))
        for f in files:
            if not f.startswith("."):
                yield os.path.join(root, f)


def flatten_files(filelist):
    """ Given a list of dirs and filenames, yield a
    flattened list of filenames"""

    for item in filelist:
        if os.path.isdir(item):
            for filename in walk_dir_tree(item):
                yield filename
        else:
            yield item


def main():
    global opts

    (opts, files) = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING if opts.quiet else logging.INFO,
        format='%(message)s'
    )

    if not files:
        logging.error("No files specified")
        parser.print_help()
        exit(1)

    path = os.path.join(os.path.dirname(__file__), RETF_FILENAME)
    regs = load_rules(path)

    for filename in flatten_files(files):
        handle_file(regs, filename)


if __name__ == '__main__':
    main()
