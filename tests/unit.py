"""Unit tests for internal functions"""
# encoding=utf-8

from __future__ import unicode_literals

import unittest
import sys

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from topy import topy


class OutputTest(unittest.TestCase):
    def test_print_diff(self):
        """Tests diff printing output"""

        self.diff_inner(
            'foobar.txt',
            "foo\nbar\nbaz\n",
            "foo\nbat\nbaz\n",
            """\
--- foobar.txt
+++ foobar.txt
@@ -1,3 +1,3 @@
 foo
-bar
+bat
 baz
""")

        self.diff_inner(
            'unicode.txt',
            "Ünicode\n\U0001F4A9\n",
            "Unicöde\n\U0001F4A9\n",
            """\
--- unicode.txt
+++ unicode.txt
@@ -1,2 +1,2 @@
-Ünicode
+Unicöde
 \U0001F4A9
""")

    def diff_inner(self, filename, old, new, expected):
        if sys.version_info[0] <= 2:
            expected = expected.encode('utf8')

        out = StringIO()
        topy.print_diff(filename, old, new, out)
        diff = out.getvalue()
        self.assertEquals(diff, expected)
        # Must be correct type too, otherwise writelines() fails
        self.assertEquals(type(diff), type(expected))


if __name__ == '__main__':
    unittest.main()
