#!python

import setuptools
import re

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('SymptomSetModel/SymptomSetModel.py').read(),
    re.M).group(1)


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="SymptomSetModel",
    version=version,
    author="David Blair",
    author_email="david.blair@ucsf.edu",
    description="A probabilistic, symptom-driven model for estimating rare disease penetrance, expressivity, and prevalence.",
    long_description_content_type="text/markdown",
    url="https://github.com/daverblair/SymptomSetModel",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'torch',
        'PiecewiseBeta',
        'tqdm',
        'scikit-learn',
        'pytorch-minimize',
        'tensordict'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
