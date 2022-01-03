#!/usr/bin/env python3
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
repository=https://upload.pypi.org/legacy/
username=jen-soft
password=secret

# ------------------------------------------------------------------------------
# curl https://bootstrap.pypa.io/get-pip.py | python3.4
# python3.4 -m pip install -U setuptools
# python3.4 -m pip install -U pip
# python3.4 -m pip install -U six
# python3.4 -m pip install -U twine

# python3.4 setup.py bdist_wheel       # WHL
python3.4 setup.py sdist            # EGG
python3.4 -m twine upload dist/* -r testpypi

# https://test.pypi.org/project/pydocker
# pip install --no-cache-dir -U -i https://test.pypi.org/pypi pydocker

# git tag -a v1.0.6 -m 'version 1.0.6'
# git push origin --tags

# ------------------------------------------------------------------------------
rm -rf ./dist
rm -rf ./pydocker.egg-info/
# change version, commit, add download url, add git tag,
python3.4 setup.py sdist             # EGG
python3.4 -m twine upload dist/* -r pypi

# pip install --no-cache-dir -U pydocker==1.0.6
# ls -lah /usr/local/lib/python2.7/dist-packages | grep pydocker

# ------------------------------------------------------------------------------

"""

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
#   #


setup(
    name='pydocker',
    version='1.0.6',

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
    download_url='https://github.com/jen-soft/pydocker/archive/v1.0.6.zip',

    # packages=['pydocker', ],
    py_modules=['pydocker', ],

    install_requires=[],
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
