#!/usr/bin/env python

from setuptools import setup

setup(
    name='topy',
    version='1.1.0',

    # PyPI metadata
    author='Marti Raudsepp',
    author_email='marti@juffo.org',
    url='https://github.com/intgr/topy',
    download_url='https://pypi.python.org/pypi/topy/',
    license='MIT, CC-BY-SA',
    description='Fixes typos in text using regular expressions, based on RegExTypoFix from Wikipedia',
    long_description=open('README.rst').read(),
    platforms='any',
    keywords='typo spelling grammar text',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # Until we have a test suite we're conservative about Python version compatibility claims
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Documentation',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Text Processing :: Filters',
    ],

    # Installation settings
    packages=['topy'],
    entry_points={'console_scripts': ['topy = topy.topy:main']},
    package_data={
        '': ['*.txt']
    },
    install_requires=[
        'regex>=2016.07.14',
        'beautifulsoup4',
    ],
    test_suite='tests',
)
