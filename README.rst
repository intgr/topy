Topy
====
.. image:: https://badge.fury.io/py/topy.svg
   :target: https://badge.fury.io/py/topy

.. image:: https://travis-ci.com/intgr/topy.svg?branch=master
   :alt: Travis CI
   :target: https://travis-ci.com/github/intgr/topy

Topy (anagram of "typo") is a Python script to fix typos in text, using rulesets developed by the RegExTypoFix_ project
from Wikipedia. The English ruleset is included with Topy and is used by default. Other rulesets can be manually
downloaded.

.. _RegExTypoFix: https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos

Topy works with Python 3.6-3.9.

The easiest way to install it is using pip::

    pip install topy

Usage::

    Usage: topy [options] FILES/DIRS...

    Options:
      -h, --help            show this help message and exit
      -q, --quiet           silence information messages
      -a, --apply           overwrite files in place
      -r FILE, --rules=FILE
                            specify custom ruleset file to use
      -d RULE, --disable=RULE
                            disable rules by name
      --color=WHEN, --colour=WHEN
                            colorize the output; WHEN can be 'never', 'always', or
                            'auto'

For example, if you want to integrate topy in your CI pipeline, you can do something like::

    sh -c "git ls-files | xargs topy --quiet --apply --; git --no-pager diff --exit-code"

The line above will check all files tracked by git, apply fixes to them and fail if any changes are applied.
If no changes are to be applied, the command returns success.

Resources
---------

* https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
* https://github.com/intgr/topy
* https://pypi.python.org/pypi/topy
* Rulesets for other languages: https://www.wikidata.org/wiki/Q6585066

Changelog
---------

1.1.0 (2021-02-03)

* Added colors to output. Thanks to Brian de Buiteach (@debuiteb) (#25)
* Python 3.5 support is removed to allow newer syntax (#25)

1.0.1 (2021-01-30)

* Updated bundled ruleset from Wikipedia (#29)
* Python 3.9 is now officially supported and tested in CI (#27)
* Migrated tests from travis-ci.org to travis-ci.com (#28)

1.0.0 (2020-09-08)

* Updated bundled ruleset from Wikipedia (#23)
* Removed Python 2.x and <3.5 compatibility code (#22)
* Fixed Travis CI configuration (#21)

0.3.0 (2020-06-02)

Note: This was the last release to support Python 2.7.

* Updated bundled ruleset (thanks to Oscar Caballero)
* Added --disable option to disable individual rules (thanks to Oscar Caballero)
* Fixed behavior when replacement string contains $ symbol (thanks to Oscar Caballero)
* Prefer the faster lxml parser when it is installed. lxml is now an optional dependency
  (thanks to Oscar Caballero)
* Added Python 3.7 support, deprecated Python 3.3 and 3.4.

0.2.2 (2016-12-16)

* Update bundled ruleset
* Officially add Python 3.6 support

0.2.1 (2016-07-15)

* Update bundled ruleset
* Update regex dependency version to avoid `regex issue #216`_
* Officially add Python 3.5 support

.. _`regex issue #216`: https://bitbucket.org/mrabarnett/mrab-regex/issues/216/invalid-match-when-using-negative

0.2.0 (2015-09-09)

* Several fixes with Unicode on Python 2
* Can safely deal with filenames that are invalid Unicode
* Update bundled ruleset
* Fix a few warnings from used libraries

0.1.0 (2014-08-24)

* Initial public release

Contributing
------------

Code style:

* In general follow the Python PEP-8_ coding style, except line length can go up to 120 chars.
* Strings that have meaning for humans use double quotes (``"``), otherwise single quotes (``'``). When in doubt, don't
  worry about it.
* Code should be compatible with both Python 2 and 3, preferably without version-specific conditionals.

Run the test suite using ``python setup.py test``.

Submit your changes as pull requests on GitHub.

.. _PEP-8: https://www.python.org/dev/peps/pep-0008/

License
-------

The Topy software is licensed under the MIT license (see LICENSE.txt)

The bundled ``retf.txt`` file, copied from `Wikipedia AutoWikiBrowser/Typos`_ by Wikipedia contributors is licensed
under CC-BY-SA_. See the page on Wikipedia for authorship information.

.. _`Wikipedia AutoWikiBrowser/Typos`: https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
.. _CC-BY-SA: https://creativecommons.org/licenses/by-sa/3.0/
