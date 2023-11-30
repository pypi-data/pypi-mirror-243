from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.2.2'
DESCRIPTION = 'A package for creating and training language models for text classification based on BERT. The package includes pre-trained models and a feature for testing the trained models.'

# Setting up
setup(
    name="categorium",
    version=VERSION,
    author="Luís Silva",
    author_email="<aluisgonalo022@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'categorium': ['modelos/*/*']
    },
    install_requires=["tensorflow>=2.12.0",
                      "transformers>=4.27.3",
                      "pandas>=1.5.3",
                      "numpy>=1.23.5"],
    keywords=['python', 'classification', 'text', 'Categorization','textCategorization','textclassification','BERT'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)