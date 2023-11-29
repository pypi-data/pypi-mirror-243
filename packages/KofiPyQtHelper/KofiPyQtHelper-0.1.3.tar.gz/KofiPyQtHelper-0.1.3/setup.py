#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-11 16:54:03
LastEditors  : Kofi
LastEditTime : 2023-07-11 16:54:03
Description  : 
"""
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="KofiPyQtHelper",
    version="0.1.3",
    author="Kofi",
    author_email="aliwkxqq@163.com",
    description="PyQt 的快速布局工具",
    long_description=long_description,
    license="BSD License",
    packages=find_packages(),
    install_requires=[
        "Jinja2==3.1.2",
        "loguru==0.6.0",
        "matplotlib==3.5.3",
        "numpy==1.21.4",
        "openpyxl==3.0.9",
        "pandas==1.3.4",
        "pdf2docx==0.5.6",
        "pypinyin==0.44.0",
        "PyQt5==5.15.10",
        "pyqtgraph==0.12.4",
        "requests==2.26.0",
        "setuptools==65.6.3",
        "SQLAlchemy==2.0.19",
    ],
)
