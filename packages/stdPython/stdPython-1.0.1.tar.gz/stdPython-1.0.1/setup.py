# -*- coding: utf-8 -*-
# @Time    : 2023/11/28 21:38:40
# @Author  : ZMF
# @FileName: setup.py
# @Software: PyCharm
# @IDE: PyCharm
# @E-Mail: ZZMF20110806@163.com
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
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
    version="1.0.1",
    author="ZMF",
    author_email="ZZMF20110806@163.com",
    description="Python package importing all in one!!!!",
    url='https://github.com/ZMF-1/stdPython',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    packages=find_packages()
)