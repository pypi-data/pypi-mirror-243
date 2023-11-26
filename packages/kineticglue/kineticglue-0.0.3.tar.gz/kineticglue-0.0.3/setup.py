from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Glue Library for KineticEmail, KineticPdf, KineticForms, and KineticAuth.'
LONG_DESCRIPTION = 'Email, PDF, Forms workflow processing.'

# Setting up
setup(
    name="kineticglue",
    version=VERSION,
    author="Kinetic Seas (Ed Honour / Joe Lehman), pdfrw, pypdf2",
    author_email="<edward.honour@kineticseas.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['kineticpdf', 'kineticemail', 'kineticauth', 'kineticforms'],
    keywords=['python', 'KineticPdf', 'KineticForms', 'KineticEmail', 'extract PDF text', 'extract PDF Form fields'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
