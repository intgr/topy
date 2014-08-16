Topy
====

Topy (anagram of "typo") is a Python script to fix typos in text, based on the RegExTypoFix_ project from Wikipedia and
AutoWikiBrowser.

.. _RegExTypoFix: https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos

Topy runs with either Python 2 or 3; you need to install dependencies listed in requirements.txt, easiest way is to use
pip::

    pip install -r requirements.txt

Usage::

    Usage: topy.py [options] FILES...

    Options:
      -h, --help   show this help message and exit
      -q, --quiet  silence information messages
      -a, --apply  overwrite files in place


Resources
---------

* https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
* https://github.com/intgr/topy

Contributing
------------

Code style:

* In general follow the Python PEP-8_ coding style, except line length can go up to 120 chars.
* Strings that have meaning for humans use double quotes (``"``), otherwise single quotes (``'``). When in doubt, don't
  worry about it.

Submit your changes as pull requests on Github.

.. _PEP-8: https://www.python.org/dev/peps/pep-0008/

License
-------

The Topy software is licensed under the MIT license (see LICENSE.txt)

The bundled ``retf.txt`` file, copied from `Wikipedia:AutoWikiBrowser/Typos`_ by Wikipedia contributors is licensed
under CC-BY-SA_. See the page on Wikipedia for authorship information.

.. _`Wikipedia:AutoWikiBrowser/Typos`: https://en.wikipedia.org/wiki/Wikipedia:AutoWikiBrowser/Typos
.. _CC-BY-SA: https://creativecommons.org/licenses/by-sa/3.0/

