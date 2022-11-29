#!/usr/bin/env python

# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fx_py_sdk",
    version="0.1",
    platforms='any',
    description="Python library for Fx(dex) chain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url='https://github.com/falcons-x/fx-py-sdk',
    keywords=["FX", "DEX", "BLOCKCHAIN"],
    install_requires=["bech32", "hdwallets", "sqlalchemy", "requests", "pandas",
                      "ecdsa", "mnemonic", "grpcio", "protobuf", "psycopg2-binary",
                      "eth-utils", "eth-account"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True
)
