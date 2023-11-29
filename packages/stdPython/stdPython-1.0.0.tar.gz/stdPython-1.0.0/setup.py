# -*- coding: utf-8 -*-
# @Time    : 2023/11/28 21:38:40
# @Author  : ZMF
# @FileName: setup.py
# @Software: PyCharm
# @IDE: PyCharm
# @E-Mail: ZZMF20110806@163.com
from setuptools import setup, find_packages

setup(
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    name="stdPython",
    version="1.0.0",
    author="ZMF",
    author_email="ZZMF20110806@163.com",
    description="Python package importing all in one!!!!",
    python_requires='>=3',
    packages=find_packages()
)