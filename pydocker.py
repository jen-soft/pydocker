#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    pydocker.py
    Easy generator Dockerfile for humans.
--------------------------------------------------------------------------------
manual

>_ install:
F=$(python -c "import site; print(site.getsitepackages()[0]+'/pydocker.py')")
sudo wget -v -N raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py -O $F

>_ usage:
[Dockerfile.py]
import sys
import logging
import pydocker  # github.com/jen-soft/pydocker

logging.getLogger('').setLevel(logging.INFO)
logging.root.addHandler(logging.StreamHandler(sys.stdout))


class DockerFile(pydocker.DockerFile):
    '''   add here your custom features   '''

d = DockerFile(base_img='debian:8.2', name='jen-soft/custom-debian:8.2')

d.RUN_bash_script('/opt/set_repo.sh', r'''
cp /etc/apt/sources.list /etc/apt/sources.list.copy

cat >/etc/apt/sources.list <<EOL
deb     http://security.debian.org/ jessie/updates main
deb-src http://security.debian.org/ jessie/updates main
deb     http://ftp.nl.debian.org/debian/ jessie main
deb-src http://ftp.nl.debian.org/debian/ jessie main
deb     http://ftp.nl.debian.org/debian/ testing main
EOL

apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC
apt-get clean && apt-get update

''')

d.EXPOSE = 80
d.WORKDIR = '/opt'

# d.ENTRYPOINT = ["/opt/www-data/entrypoint.sh"]
d.CMD = ["python", "--version"]

d.build_img()



>_ * alternative usage:
[Dockerfile.py]
try: from pydocker import DockerFile
except ImportError:
    try: from urllib.request import urlopen         # python-3
    except ImportError: from urllib import urlopen  # python-2
    exec(urlopen('https://raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py').read())
#
d = DockerFile(base_img='debian:8.2', name='jen-soft/custom-debian:8.2')
# ...


--------------------------------------------------------------------------------
change log:
    v0.0.1      Tue 30 Apr 2019 06:12:04 AM UTC     jen
            - created
    v1.0.3      Fri May  3 13:19:29 UTC 2019     jen
            - release 1.0.3
    v1.0.4      Fri May  3 14:18:31 UTC 2019     jen
            - fix regex validation of img name

    v1.0.5      Sat Jun 15 11:21:02 UTC 2019     jen
            - add error trace for RUN_bash_script

    v1.0.6      Mon Jan  3 22:35:21 UTC 2022     jen
            - add DockerFileV105a
            - allow run sh script without provide dst-path
            - unique tag - useful for development new dockerfile

            - add generate_img_name


--------------------------------------------------------------------------------
contributors:
    jen:
        name:       Evgheni Amanov
        email:      jen.soft.master@gmail.com
        skype:      jen.soft.master

--------------------------------------------------------------------------------
Copyright 2019 Jen-soft

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import os
import sys
import re
import json
import subprocess
import hashlib
import datetime

import logging

log = logging.getLogger(__name__)

# ############################################################################ #


# ############################################################################ #
class DockerFileV105(object):
    # https://docs.docker.com/engine/reference/builder/

    FROM, LABEL, COPY, RUN, WORKDIR, ENV, SHELL, EXPOSE, ENTRYPOINT, CMD, \
        ADD, STOPSIGNAL, USER, VOLUME, ARG, ONBUILD, HEALTHCHECK, = [
            None for i in range(17)]

    _regex = re.compile(
        r'(?P<namespace>[0-9A-Za-z-\_\.]+)/'
        r'(?P<name>[0-9A-Za-z\-\_\.]+):'
        r'(?P<version>[0-9A-Za-z\-\_\.]+)'
    )

    def __init__(self, base_img, name):
        self._instructions = []
        self._instructions.append({
            'type':     'instruction',
            'name':     'FROM',
            'value':    base_img,
        })
        # parse new img name
        _r = self._regex.search(name.strip())
        if _r is None:
            raise ValueError('invalid img name "{}", '
                             'should be as "local/base:0.0.1"'.format(name))
        self._namespace = _r.group('namespace')
        self._name = _r.group('name')
        self._version = _r.group('version')

    def get_img_name(self):
        return '{}/{}:{}'.format(
            self._namespace, self._name, self._version)

    def __setattr__(self, key, value):
        if key.startswith('_'):
            return super(DockerFileV105, self).__setattr__(key, value)
        #
        if not isinstance(value, str):
            value = json.dumps(value)
        #
        self._instructions.append({
            'type':     'instruction',
            'name':     key,
            'value':    value,
        })
        #

    # -------------------------------------------------------------------- #
    def LABEL(self, *args, **kwargs):
        assert not args
        #
        for k, v in kwargs.items():
            self.__setattr__('LABEL', '{}="{}"'.format(k, v))
        #

    # -------------------------------------------------------------------- #
    def add_new_file(self, dst_path, content, chmod=None):
        content = content.strip() + '\n'
        self._instructions.append({
            'type':         'file',
            'path':         dst_path,
            'content':      content,
        })
        if chmod is not None:
            self.RUN = 'chmod {} {}'.format(chmod, dst_path)
        #

    def COPY(self, dst_path, content, chmod=None):
        self.add_new_file(dst_path, content, chmod=chmod)

    def RUN_bash_script(self, dst_path, content, keep_file=False):
        # https://stackoverflow.com/questions/22009364/is-there-a-try-catch-command-in-bash
        # https://unix.stackexchange.com/questions/462156/how-do-i-find-the-line-number-in-bash-when-an-error-occured
        content = '''
#!/usr/bin/env bash
set -e -o xtrace

function _failure() {
  echo -e "\\r\\nERROR: bash script [ %(script_name)s ] failed at line $1: \\"$2\\""
}
trap '_failure ${LINENO} "$BASH_COMMAND"' ERR

# ############################################################################ #
        '''.strip() % {'script_name': dst_path} + '\n\n'+ content

        self.COPY(dst_path, content, chmod='+x')
        self.RUN = dst_path
        if not keep_file:
            self.RUN = 'rm {}'.format(dst_path)
        #

    def RUN_python_script(self, dst_path, fn, keep_file=False,
                          python='/usr/bin/python'):
        if not isinstance(fn, str):
            from inspect import getsource
            fn = '{}\n{}()'.format(getsource(fn), fn.__name__)
        #
        self.COPY(dst_path, '# -*- coding: utf-8 -*-\n' + fn, chmod='+x')
        self.RUN = '{} {}'.format(python, dst_path)
        if not keep_file:
            self.RUN = 'rm {}'.format(dst_path)
        #

    # -------------------------------------------------------------------- #
    def generate_files(self, dockefile_name=None, path='./',
                       remove_old_files=True):
        if dockefile_name is None:
            dockefile_name = 'Dockerfile.{}'.format(self._name)
        #
        log.info('Generate dockerfile and additional files: {}'
                 ''.format(dockefile_name))
        #
        result = ''
        files = []
        for instruction in self._instructions:
            if instruction['type'] == 'file':
                dst_path = instruction['path']
                local_name = '{}.{}@{}'.format(
                    dockefile_name, len(files), os.path.basename(dst_path))
                #
                files.append([local_name, instruction['content']])
                result += '\nCOPY {} {}'.format(local_name, dst_path)
            elif instruction['type'] == 'instruction':
                result += '\n{name} {value}'.format(**instruction)
            else:
                raise ValueError(
                    'invalid instruction type {}'.format(instruction))
            #
        #
        files = [[dockefile_name, result], ] + files
        return self._create_files(path, files, remove_old_files)

    @staticmethod
    def _create_files(path, files, remove_old_files):
        dockerfile_name = files[0][0]
        if remove_old_files:
            for name in os.listdir(path):
                if re.findall(r'^{}.[0-9]+@'.format(dockerfile_name), name):
                    os.remove(name)
        #   #   #

        result_files = []
        for name, content in files:
            file_path = os.path.join(path, name)
            with open(file_path, 'w+') as file:
                file.write(content)
                file.flush()
            #
            result_files.append(file_path)
        #
        return result_files

    # -------------------------------------------------------------------- #
    def build_img(self, remove_out_files=True):

        log.info('Build new docker img {}'.format(self.get_img_name()))
        #
        files = self.generate_files()
        dirname, filename = os.path.split(files[0])

        cmd = 'docker build  --tag {tag}  --file={docker_file} {path}/ '.format(
            tag=self.get_img_name(),
            docker_file=filename,
            path=dirname,
        )
        #
        cmd = re.sub(r'[\r\n\s\t]+', ' ', cmd).strip()
        #
        log.info('Execute "{}"'.format(cmd))
        #
        p = subprocess.Popen(
            [cmd, ], shell=True,
            stdout=sys.stdout, stderr=sys.stderr,
            stdin=subprocess.PIPE,
        )
        p.communicate()
        if remove_out_files and p.returncode == 0:
            for file in files:
                os.remove(file)
        #   #   #
#

# ############################################################################ #

class DockerFileV106(DockerFileV105):
    """
        add features:
            - allow run sh script without provide dst-path
            - unique tag - useful for development new dockerfile

            - add generate_img_name
    """
    def __init__(self, base_img, name, use_build_time_prefix=False):
        super(DockerFileV106, self).__init__(base_img, name)
        self._use_build_time_prefix = use_build_time_prefix

    def RUN_bash_script(self, dst_path: str, content=None, keep_file=False):
        if content is None:
            # feature - allow run sh script without provide dst-path
            assert keep_file is False
            content = dst_path
            _name_sold = hashlib.sha256(
                content.encode()
            ).hexdigest()[:24]
            _counter = getattr(self, '_counter', 0)
            _counter += 1
            setattr(self, '_counter', _counter)
            dst_path = f'/opt/random_{_counter:02d}_{_name_sold}.sh'
        #
        return super(DockerFileV106, self).RUN_bash_script(dst_path, content, keep_file)

    def get_img_name(self):
        _img_name = getattr(self, '_img_name', None)
        if _img_name is None:
            # use cashing for ime_prefix feature
            _img_name = self.generate_img_name()
            setattr(self, '_img_name', _img_name)
        #
        return _img_name

    def generate_img_name(self):
        if self._use_build_time_prefix is True:
            # feature - unique tag - useful for development new dockerfile
            # need to check if docker-file has new changes
            _build_time_id = f'{datetime.datetime.utcnow():%y%m%d%H%M%S}'
            return f'{self._namespace}/{self._name}' \
                   f':' \
                   f'{self._version}-build-{_build_time_id}'
        #
        return super(DockerFileV106, self).get_img_name()

# ############################################################################ #


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
DockerFileLatestStable = DockerFileV105     # stable using for long time
DockerFileLatestAlpha = DockerFileV106      # newest version for more features

DockerFile = DockerFileLatestStable         # by default - stable

# it's allow you to use more appropriate release in your code
# you can user full compatibility version DockerFileLatestStable
# or maximum feature DockerFileLatestAlpha
# or take direct DockerFileV106 for fixation any api changes in feature


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# aliases - using naming Dockerfile instead DockerFile
DockerfileV105 = DockerFileV105
DockerfileV106 = DockerFileV106

DockerfileLatestStable = DockerFileLatestStable
DockerfileLatestAlpha = DockerFileLatestAlpha
Dockerfile = DockerFile






