# -*- coding: utf-8 -*-
# @Time    : 2023/11/28 21:12:15
# @Author  : ZMF
# @FileName: __init__.py
# @Software: PyCharm
# @IDE: PyCharm
# @E-Mail: ZZMF20110806@163.com
'''
已弃用模块
import tkinter.tix
import sys.monitoring
from future import *
import importlib.resources.abc
import sys.path
import optparse
'''

# 可能不可用的模块
try:
    import readline
except ModuleNotFoundError:
    pass
else:
    import readline

try:
    import tomlilib
except ModuleNotFoundError:
    pass
else:
    import tomlilib

try:
    import curses
except ModuleNotFoundError:
    pass
else:
    import curses
    import curses.textpad
    import curses.ascii
    import curses.panel

try:
    import crypt
except ImportError:
    pass
else:
    import crypt

try:
    import nis
except ModuleNotFoundError:
    pass
else:
    import nis

try:
    import ossaudiodev
except ModuleNotFoundError:
    pass
else:
    import ossaudiodev

try:
    import spwd
except ModuleNotFoundError:
    pass
else:
    import spwd

# 文本处理服务
import string
import re
import difflib
import textwrap
import unicodedata
import stringprep
import rlcompleter

# 二进制数据服务
import struct
import codecs

# 数据类型
import datetime
import zoneinfo
import calendar
import collections
import collections.abc
import heapq
import bisect
import array
import weakref
import types
import copy
import pprint
import reprlib
import enum
import graphlib

# 数字和数学模块
import numbers
import math
import cmath
import decimal
import fractions
import random
import statistics

# 函数式编程模块
import itertools
import functools
import operator

# 文件和目录访问
import pathlib
import os.path
import fileinput
import stat
import filecmp
import tempfile
import glob
import fnmatch
import linecache
import shutil

# 数据持久化
import pickle
import copyreg
import shelve
import marshal
import dbm
import sqlite3

# 数据压缩和存档
import zlib
import gzip
import bz2
import lzma
import zipfile
import tarfile

# 文件格式
import csv
import configparser
import netrc
import plistlib

# 加密服务
import hashlib
import hmac
import secrets

# 通用操作系统服务
import os
import io
import time
import argparse
import getopt
import logging
import logging.config
import logging.handlers
import getpass
import platform
import errno
import ctypes

# 并发执行
import threading
import multiprocessing
import multiprocessing.shared_memory
import concurrent
import concurrent.futures
import subprocess
import sched
import queue
import contextvars
import _thread

# 网络和进程间通信
import asyncio
import socket
import ssl
import select
import selectors
import signal
import mmap

# 互联网数据处理
import email
import json
import mailbox
import mimetypes
import base64
import binascii
import quopri

# 结构化标记处理工具
import html
import html.parser
import html.entities
import xml
import xml.etree.ElementTree
import xml.dom
import xml.dom.minidom
import xml.dom.pulldom
import xml.sax
import xml.sax.handler
import xml.sax.saxutils
import xml.sax.xmlreader
import xml.parsers.expat

# 互联网协议和支持
import webbrowser
import wsgiref
import urllib
import urllib.request
import urllib.response
import urllib.parse
import urllib.error
import urllib.robotparser
import http
import http.client
import ftplib
import poplib
import imaplib
import smtplib
import uuid
import socketserver
import http.server
import http.cookies
import http.cookiejar
import xmlrpc
import xmlrpc.client
import xmlrpc.server
import ipaddress

# 多媒体服务
import wave
import colorsys

# 国际化
import gettext
import locale

# 程序框架
import turtle
import cmd
import shlex

# Tk图形用户界面(GUI)
import tkinter
import tkinter.colorchooser
import tkinter.font
import tkinter.simpledialog
import tkinter.messagebox
import tkinter.scrolledtext
import tkinter.dnd
import tkinter.ttk

# 开发工具
import typing
import pydoc
import doctest
import unittest
import unittest.mock
import lib2to3

# 调试和分析
import bdb
import faulthandler
import pdb
import timeit
import trace
import tracemalloc

# 软件打包和分发
import ensurepip
import venv
import zipapp

# Python运行时服务
import sys
import sysconfig
import builtins
import __main__
import warnings
import dataclasses
import contextlib
import abc
import atexit
import traceback
import gc
import inspect
import site

# 自定义Python解释器
import code
import codeop

# 导入模块
import zipimport
import pkgutil
import modulefinder
import runpy
import importlib
import importlib.resources
import importlib.metadata

# Python语言服务
import ast
import symtable
import token
import keyword
import tokenize
import tabnanny
import pyclbr
import py_compile
import compileall
import dis
import pickletools

# Windows系统相关模块
if sys.platform == 'win32' or sys.platform == 'cygwin':
    import msvcrt
    import winreg
    import winsound
else:
    pass

# Unix专有服务
if sys.platform == 'linux':
    import posix
    import pwd
    import grp
    import termios
    import tty
    import pty
    import fcntl
    import resource
    import syslog
else:
    pass

# 被取代的模块
import aifc
import audioop
import cgi
import cgitb
import chunk
import imghdr
import mailcap
import msilib
import nntplib
import pipes
import sndhdr
import sunau
import telnetlib
import uu
import xdrlib

# 私货
from . import information
from . import help

if __name__ == '__main__':
    sys.exit()
