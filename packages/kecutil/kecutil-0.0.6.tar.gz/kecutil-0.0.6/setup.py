from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.6'
DESCRIPTION = 'Simple utility functions for KEC\'s Intro To Programming: Python Course'
LONG_DESCRIPTION = 'A package that allows you to easily use utility functions for KEC\'s Intro To Programming: Python Course'

# Setting up
setup(
    name="kecutil",
    version=VERSION,
    author="Hycord (Masen Toplak)",
    author_email="<hello@masen.dev>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)