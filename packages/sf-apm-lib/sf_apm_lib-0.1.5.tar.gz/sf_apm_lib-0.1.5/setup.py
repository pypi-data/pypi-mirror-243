import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="sf_apm_lib",
    version="0.1.5",
    url="https://github.com/snappyflow/py_snappyflow",
    license='MIT',

    author="Maplelabs",
    author_email="pradeep.jaiswar@maplelabs.com",

    description="Snappyflow pip package",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',

    packages=find_packages(exclude=('tests',)),

    install_requires=['cryptography', 'pycryptodome==3.10.1', 'cffi==1.14.6', 'PyYAML==5.4.1'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
