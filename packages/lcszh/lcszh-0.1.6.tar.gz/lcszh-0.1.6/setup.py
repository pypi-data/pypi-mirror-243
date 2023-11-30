#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='lcszh',
    version='0.1.6',
    description=(
        'utils for lcszhlcy'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='yyszh',
    author_email='yyszhyyy@163.com',
    license='Apache License 2.0',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'xlrd==1.2.0',
        'numpy',
        'tqdm',
        'python-docx',
        'configparser',
        'jieba',
        'matplotlib',
        'wordcloud',
        'xlsxwriter==3.0.1'
    ],
)
