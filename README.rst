Topy
====

Topy (anagram of "typo") is a Python script to fix typos in text, using rulesets developed by the RegExTypoFix_ project
from Wikipedia. The English ruleset is included with Topy and is used by default. Different rulesets need to be manually
downloaded.

.. _RegExTypoFix: https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos

Topy runs with either Python 2 or 3; you need to install dependencies listed in requirements.txt, easiest way is to use
pip::

    pip install -r requirements.txt

Usage::

    Usage: topy [options] FILES/DIRS...

    Options:
      -h, --help            show this help message and exit
      -q, --quiet           silence information messages
      -a, --apply           overwrite files in place
      -r FILE, --rules=FILE
                            specify custom ruleset file to use


Resources
---------

* https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
* https://github.com/intgr/topy
* Rulesets for other languages: https://www.wikidata.org/wiki/Q6585066

Contributing
------------

Code style:

* In general follow the Python PEP-8_ coding style, except line length can go up to 120 chars.
* Strings that have meaning for humans use double quotes (``"``), otherwise single quotes (``'``). When in doubt, don't
  worry about it.

Run the test suite using ``python setup.py test``.

Submit your changes as pull requests on GitHub.

.. _PEP-8: https://www.python.org/dev/peps/pep-0008/

License
-------

The Topy software is licensed under the MIT license (see LICENSE.txt)

The bundled ``retf.txt`` file, copied from `Wikipedia:AutoWikiBrowser/Typos`_ by Wikipedia contributors is licensed
under CC-BY-SA_. See the page on Wikipedia for authorship information.

.. _`Wikipedia:AutoWikiBrowser/Typos`: https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
.. _CC-BY-SA: https://creativecommons.org/licenses/by-sa/3.0/

