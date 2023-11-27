from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

LONG_DESCRIPTION = 'A package that allows to create payment link, cancel order, confirm webhook and get payment link information'

setup(
    name='payos-lib-python',
    version='0.1.8',
    author='Casso',
    author_email='tranglq@casso.vn',
    description='A library for create Payment Link of PayOS and more',
    long_description_content_type="text/markdown",

    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
        keywords=['payos', 'vietqrpro', 'payos-python'],

)