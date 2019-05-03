#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""


# [ ~/.pypirc ] ----------------------------------------------------------------
[distutils]
index-servers =
  testpypi
  pypi

[testpypi]
repository=https://test.pypi.org/legacy/
username=jen-soft
password=secret

[pypi]
repository=https://pypi.python.org/pypi
username=jen-soft
password=secret

# ------------------------------------------------------------------------------
# python setup.py bdist_wheel       # WHL
python setup.py sdist             # EGG
python setup.py sdist upload -r testpypi

# https://test.pypi.org/project/pydocker
# pip install --no-cache-dir -U -i https://test.pypi.org/pypi pydocker

# git tag -a v1.0.1 -m 'version 1.0.1'

# ------------------------------------------------------------------------------
rm -rf ./dist
# change version
# commit, add git tag, add download url
python setup.py sdist             # EGG

# ------------------------------------------------------------------------------

"""
from distutils.core import setup

try:
    import pypandoc  # apt-get install pandoc &&  pip install pypandoc
    long_description = pypandoc.convert('README.md', format='md', to='rst', )
except Exception as e:
    print(e)
    with open("README.md", "r") as fh:
        long_description = fh.read()
#   #


setup(
    name='pydocker',
    version='1.0.1',

    description='Easy generator Dockerfile for humans.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jen-soft/pydocker',  # home-page

    author='Jen-Soft',
    author_email='jen.soft.master@gmail.com',
    license='Apache License 2.0 and MIT License',

    maintainer='Jen-Soft',
    maintainer_email='jen.soft.master@gmail.com',

    platforms=['any', ],
    download_url='https://github.com/jen-soft/pydocker/archive/v0.0.1.zip',

    # packages=['pydocker', ],
    py_modules=['pydocker', ],

    install_requires=[
    ],
    keywords=[
        'dockerfile',
        'docker',
        'pydocker',
        'python',
        'deploy',
        'docker-image',
        'for-humans',

    ],
    classifiers=[
        # https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',
        'Intended Audience :: Developers',

        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: Apple Public Source License",
        "License :: OSI Approved :: MIT License",

        "Natural Language :: English",
        "Natural Language :: Russian",

        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2',

        'Programming Language :: Python :: Implementation',

        'Topic :: Software Development',
        'Topic :: System',
        'Topic :: System :: Clustering',
        'Topic :: System :: Emulators',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
)
