# This file is part of filestore-cellar. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import io
import os

from setuptools import setup


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


setup(name='tryton-filestore-cellar',
    version='0.1.0',
    author='Tryton',
    author_email='foundation@tryton.org',
    description='Store Tryton files on Cellar Storage Service',
    long_description=read('README.rst'),
    url='https://pypi.org/project/tryton-filestore-cellar/',
    download_url='https://downloads.tryton.org/tryton-filestore-cellar/',
    project_urls={
        "Bug Tracker": 'https://bugs.tryton.org/tryton-filestore-cellar',
        "Forum": 'https://discuss.tryton.org/tags/filestore-cellar',
        "Source Code": 'https://code.tryton.org/tryton-filestore-cellar',
        },
    py_modules=['tryton_filestore_cellar'],
    platforms='Posix; MacOS X; Windows',
    keywords='tryton clever cloud cellar storage',
    classifiers=[
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
        ],
    license='GPL-3',
    install_requires=[
        'boto',
        'trytond > 6.0',
        ],
    )
