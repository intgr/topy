"""Functional tests using the command line interface"""

import os
import shutil
import tempfile
import unittest

from topy import topy


TESTRULES = r"""
<Typo word="Foobar" find="\b([Ff])oobaz\b" replace="$1oobar"/>
"""


def writefile(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def readfile(path):
    with open(path) as f:
        return f.read()


class CommandTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.testrules = os.path.join(self.dir, 'testrules.txt')

        writefile(self.testrules, TESTRULES)

        # Suppress output during tests
        topy.log.setLevel('CRITICAL')

    def tearDown(self):
        shutil.rmtree(self.dir)

        topy.log.setLevel('NOTSET')

    def test_rules_apply(self):
        """Test --rules and --apply options"""

        txtfile = os.path.join(self.dir, 'test.txt')
        writefile(txtfile, "text\nfoobaz\n")

        topy.main(['--apply', '--rules', self.testrules, txtfile])

        self.assertEqual("text\nfoobar\n", readfile(txtfile))

    def test_notfound(self):
        """Don't crash when filename arguments can't be opened."""

        notfound = os.path.join(self.dir, "this file does not exist")

        with self.assertRaises(SystemExit):
            topy.main(['--rules', notfound, notfound])

        # Non-existent source files are ignored
        topy.main(['--rules', self.testrules, notfound])

    def test_disable_rules(self):
        """Test disabling rules with --disable."""

        original = topy.disabled.copy()
        disable = ["foo", "bar"]

        topy.main(
            ['--disable', disable[0], '--disable', disable[1], self.testrules]
        )

        self.assertEqual(topy.disabled.difference(original), set(disable))


if __name__ == '__main__':
    unittest.main()
