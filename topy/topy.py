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

log = logging.getLogger('topy')
PY2 = sys.version_info[0] <= 2


def load_rules(filename):
    """Load and parse rules from `filename`, returns list of 3-tuples [(name, regexp, replacement), ...]"""

    with open(filename) as rulefile:
        # Use html.parser: lxml is only slightly faster & requires an additional dependency.
        soup = BeautifulSoup(rulefile, 'html.parser')
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
            log.debug("cannot compile %s %r: %s", word, find, err)
            n_errors += 1

    log.info("Loaded %d rules (except %d errors, %d disabled)", n_loaded, n_errors, n_disabled)

    return regs


def read_text_file(filename):
    """Reads file `filename` and returns contents as Unicode string. On failure, returns None and logs error."""

    try:
        with open(filename, 'rb') as f:
            return f.read().decode(ENCODING)
    except (IOError, OSError) as err:
        log.error("Cannot open %r: %s", filename, err)
    except UnicodeDecodeError:
        # We could implement configurable encodings or automatic fallback, but really, people should just quit that
        # nonsense and use UTF-8. If you have a valid use case, please open an issue and explain.
        log.info("Skip %s", sanitize_filename(filename))

    return None


def sanitize_filename(filename):
    """Converts `filename` to unicode, replaces invalid (un-encodable) characters."""

    if PY2:
        # This may break on Windows with Unicode filenames? Please tell me how to fix it if anyone out there cares.
        if isinstance(filename, str):
            # noinspection PyUnresolvedReferences
            filename = filename.decode(sys.getfilesystemencoding() or ENCODING, 'replace')
        return filename
    else:
        # Input filename is always unicode with surrogate escapes.
        return filename.encode('utf8', 'surrogateescape').decode('utf8', 'replace')


def print_diff(filename, old, new, stream=sys.stdout):
    """Diffs the `old` and `new` strings and prints as unified diff to file-like object `stream`."""

    # TODO: color output for terminals
    if PY2:
        # On Python 2, unified_diff() requires non-Unicode str
        filename = filename.encode(ENCODING)
    lines = unified_diff(old.splitlines(True), new.splitlines(True), filename, filename)
    if PY2:
        # Encode lines that aren't already str
        lines = (line if isinstance(line, str) else line.encode(ENCODING)
                 for line in lines)
    stream.writelines(lines)


def handle_file(regs, filename):
    """Apply rules from `regs` to file `filename`

    If `apply` is True, the file is overwritten. Otherwise a unified diff is printed to stodut.
    """

    oldtext = text = read_text_file(filename)
    if not text:
        return

    safe_name = sanitize_filename(filename)

    replaced = 0
    for word, r, replace in regs:
        try:
            newtext, count = r.subn(replace, text)
            if count > 0 and newtext != text:
                replaced += count
                log.debug("%s: replaced %s x %d", safe_name, word, count)
            text = newtext
        except regex.error as err:
            log.error("%s: error replacing %s (%r=>%r): %s", safe_name, word, r, replace, err)

    if replaced > 0:
        if opts.apply:
            log.info("Writing %s", safe_name)
            with open(filename, 'wb') as f:
                f.write(text.encode(ENCODING))
        else:
            print_diff(safe_name, oldtext, text)


def walk_dir_tree(dirpath):
    """Walk a directory tree, yielding filenames recursively, except those starting with a dot (.)"""

    for root, dirs, files in os.walk(dirpath):
        # Modify 'dirs' list in place, so walk() doesn't recurse into them
        # str(".") fixes issue #14: Python 2 has non-Unicode str pathnames, Python 3 uses Unicode
        dirs[:] = (d for d in dirs if not d.startswith(str(".")))
        for f in files:
            if not f.startswith(str(".")):
                yield os.path.join(root, f)


def flatten_files(paths):
    """Given a list of directories and filenames, yield a flattened sequence of filenames."""

    for path in paths:
        if os.path.isdir(path):
            # Once we can drop Python < 3.3 support, this should use 'yield from'
            for filename in walk_dir_tree(path):
                yield filename
        else:
            # Filename, or the path cannot be accessed (privilege errors, file not found, etc)
            yield path


# Argument parsing. Keep this together with main()
parser = OptionParser(usage="%prog [options] FILES/DIRS...")
parser.add_option("-q", "--quiet",
                  action='store_true', dest='quiet', default=False,
                  help="silence information messages")
parser.add_option("-a", "--apply",
                  action='store_true', dest='apply', default=False,
                  help="overwrite files in place")
parser.add_option("-r", "--rules", dest='rules', metavar="FILE",
                  help="specify custom ruleset file to use")


def main(args=None):
    global opts

    (opts, paths) = parser.parse_args(args=args)

    logging.basicConfig(
        level=logging.WARNING if opts.quiet else logging.INFO,
        format='%(message)s'
    )

    if not paths:
        log.error("No paths specified")
        parser.print_help()
        sys.exit(1)

    if opts.rules is None:
        # TODO: Are there any better ways to bundle data files with Python packages?
        opts.rules = os.path.join(os.path.dirname(__file__), RETF_FILENAME)

    try:
        regs = load_rules(opts.rules)
    except (IOError, OSError) as err:
        log.error("Cannot load ruleset: %s", err)
        sys.exit(1)

    for filename in flatten_files(paths):
        handle_file(regs, filename)


if __name__ == '__main__':
    main()
