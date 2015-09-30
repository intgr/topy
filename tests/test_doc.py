"""Documentation tests"""

import os
import unittest

from topy import topy


class ReadmeTest(unittest.TestCase):
    def test_usage(self):
        """Make sure that README contains up to date --help output."""

        topy.parser.prog = 'topy'
        helplines = topy.parser.format_help().splitlines()

        path = os.path.join(os.path.dirname(__file__), '..', 'README.rst')
        with open(path) as f:
            lines = list(f.readlines())

        # This all looks a bit crazy, but it works...
        # Locate "Usage::" line in readme
        idx = lines.index("Usage::\n")

        # Preceding empty line
        self.assertEqual("\n", lines[idx+1])

        idx += 2
        # Enumerate lines in help output and match up to readme
        matchlines = lines[idx:idx+len(helplines)]
        for hline, rline in zip(helplines, matchlines):
            self.assertEqual(hline.strip(), rline.strip())

        # Following line must be empty
        self.assertEqual("\n", lines[idx+len(helplines)])


if __name__ == '__main__':
    unittest.main()
