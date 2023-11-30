from setuptools import setup, find_packages
import codecs
import os
VERSION = '0.0.4'
DESCRIPTION = 'Python Package to flatten the complex json data'
with open('README.md',"r") as fh:
    LONG_DESCRIPTION=fh.read()

# Setting up
setup(
    name="flatten_complex_json",
    version=VERSION,
    author="abhishek",
    author_email="abhishekaggarwal1211@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['flatten json', 'flatten api data', 'flat json data', 'python flatten dataframe', 'abhishek aggarwal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)