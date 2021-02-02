#!/usr/bin/env python
"""
Topy (anagram of "typo") is a Python script to fix typos in text, based on
the RegExTypoFix project from Wikipedia and AutoWikiBrowser.

Topy requires BeautifulSoup version 4 and runs with Python 3.6+

Usage: ./topy.py /path/to/files

See:
* https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
* https://github.com/intgr/topy
"""

import sys
import logging
import os
from optparse import OptionParser
from difflib import unified_diff

import regex
from bs4 import BeautifulSoup


RETF_FILENAME = 'retf.txt'

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


def parse_replacement(replace):
    """
    Parse a replacement pattern as read from the file by changing all back
    references to \\ instead of $.
    """
    return regex.sub(r'\$(\d)', r'\\\1', replace)


def load_rules(filename):
    """Load and parse rules from `filename`, returns list of 3-tuples [(name, regexp, replacement), ...]"""

    with open(filename, encoding='utf-8') as rulefile:
        # try to use lxml(slightly faster) if it's installed, otherwise default
        # to html.parser
        try:
            import lxml
            parser = 'lxml'
        except ImportError:
            parser = 'html.parser'
        soup = BeautifulSoup(rulefile, parser)
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
            replace = parse_replacement(replace)

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
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except (IOError, OSError) as err:
        log.error("Cannot open %r: %s", filename, err)
    except UnicodeDecodeError:
        # We could implement configurable encodings or automatic fallback, but really, people should just quit that
        # nonsense and use UTF-8. If you have a valid use case, please open an issue and explain.
        log.info("Skip %s", sanitize_filename(filename))

    return None


def sanitize_filename(filename):
    """Converts `filename` to unicode, replaces invalid (un-encodable) characters."""

    # Input filename is always unicode with surrogate escapes.
    return filename.encode(errors='surrogateescape').decode(errors='replace')


def print_diff(filename, old, new, stream=sys.stdout):
    """Diffs the `old` and `new` strings and prints as unified diff to file-like object `stream`."""

    lines = unified_diff(old.splitlines(True), new.splitlines(True), filename, filename)
    if is_color_output_required(stream):
        lines = map(add_output_color, lines)
    stream.writelines(lines)


def is_color_output_required(stream):
    """Determines whether to output the line diffs in color or not."""
    if opts.color == "never":
        return False
    elif opts.color == "always":
        return True
    return hasattr(stream, 'isatty') and stream.isatty()


def add_output_color(line):
    """Adds color to the output of the diff lines."""
    if line.startswith('+'):
        line = f'\033[1;32m{line}'
    elif line.startswith('-'):
        line = f'\033[1;31m{line}'
    return f'{line}\033[0m'


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
            with open(filename, 'w') as f:
                f.write(text)
        else:
            print_diff(safe_name, oldtext, text)


def walk_dir_tree(dirpath):
    """Walk a directory tree, yielding filenames recursively, except those starting with a dot (.)"""

    for root, dirs, files in os.walk(dirpath):
        # Modify 'dirs' list in place, so walk() doesn't recurse into them
        dirs[:] = (d for d in dirs if not d.startswith("."))
        for f in files:
            if not f.startswith("."):
                yield os.path.join(root, f)


def flatten_files(paths):
    """Given a list of directories and filenames, yield a flattened sequence of filenames."""

    for path in paths:
        if os.path.isdir(path):
            yield from walk_dir_tree(path)
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
parser.add_option("-d", "--disable", dest='disable', action="append",
                  metavar="RULE", help="disable rules by name")
parser.add_option("--color", "--colour", type="choice", choices=("never", "always", "auto"), default="auto",
                  dest="color", metavar="WHEN", help="colorize the output; WHEN can be 'never', 'always', or 'auto'")


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

    if opts.disable is not None:
        disabled.update(opts.disable)

    try:
        regs = load_rules(opts.rules)
    except (IOError, OSError) as err:
        log.error("Cannot load ruleset: %s", err)
        sys.exit(1)

    for filename in flatten_files(paths):
        handle_file(regs, filename)


if __name__ == '__main__':
    main()
