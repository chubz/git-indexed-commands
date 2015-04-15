# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='git-indexed-commands',
    version='0.1',
    description='Working with indexes instead of filepaths in custom git commands',
    long_description=README,
    url='https://github.com/chubz/git-indexed-commands.git',
    author='Borislav Petrović',
    author_email='petrovic.borislav@gmail.com',
    license='BSD License',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': [
            'git-istatus=gic.script:git_istatus_main',
            'git-iadd=gic.script:git_iadd_main',
            'git-icheckout=gic.script:git_icheckout_main',
            'git-idiff=gic.script:git_idiff_main',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
    ],
)
