"""Unit tests for internal functions"""

import unittest

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from topy import topy


class OutputTest(unittest.TestCase):
    def test_print_diff(self):
        """Tests diff printing output"""

        # Simple ASCII diff
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

        # Unicode diff
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

        # Unicode filename
        filename = 'ünicöde.txt'
        self.diff_inner(
            filename,
            "Foobar\n",
            "Foobaz\n",
            """\
--- ünicöde.txt
+++ ünicöde.txt
@@ -1 +1 @@
-Foobar
+Foobaz
""")

        # Filename with invalid characters
        filename = b'foo\xffbar.txt'
        self.diff_inner(
            filename.decode(errors='surrogateescape'),
            "Foobar\n",
            "Foobaz\n",
            """\
--- foo�bar.txt
+++ foo�bar.txt
@@ -1 +1 @@
-Foobar
+Foobaz
""")

    def diff_inner(self, filename, old, new, expected):
        out = StringIO()
        topy.print_diff(topy.sanitize_filename(filename), old, new, out)
        diff = out.getvalue()
        self.assertEqual(diff, expected)
        # Must be correct type too, otherwise writelines() fails
        self.assertEqual(type(diff), type(expected))


class ParsingTest(unittest.TestCase):
    def test_parse_replacement(self):
        cases = [
            (r'', r''),
            (r'$1', r'\1'),
            (r'$1$2', r'\1\2'),
            (r'US$ $CAD', r'US$ $CAD'),
        ]
        for replacement, expect in cases:
            self.assertEqual(topy.parse_replacement(replacement), expect)


if __name__ == '__main__':
    unittest.main()
