#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    pydocker.py
    Easy generator Dockerfile for humans.
--------------------------------------------------------------------------------
manual

>_ install:
sudo wget -v -N raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py  "$(python -m site --user-site)/pydocker.py"


>_ usage:
[Dockerfile.py]
import os
from pydocker import DockerFile

d = DockerFile(name=os.path.basename(__file__).rsplit('.', 1)[0])

d.FROM = 'debian:8.2'
d.LABEL = 'maintainer="jen-soft <jen.soft.master@gmail.com>"'
d.RUN = 'apt-get update'
d.RUN_file_bash('/opt/init_pg.sh', '''
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf &
sleep 20
cd ~postgres/
su postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'postgres';\" "
''')


def py_version():
    import os, sys, pwd
    with open('py-version.txt', 'w+') as f:
        f.write('user: '.format(pwd.getpwuid(os.getuid()).pw_name))
        f.write('python-version'.format(sys.version))
#   #

d.RUN_file_python('/opt/run_up_info.py', py_version, True)
d.WORKDIR = '/opt'
d.CMD = ["supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]

d.create_files()
# will created next files:
#   Dockerfile
#   Dockerfile.0@init_pg.sh         # d.RUN_file_bash
#   Dockerfile.1@run_up_info.py     # d.RUN_file_python

# >_ console:
# python3 Dockerfile.py
# ls -lah; cat -n Dockerfile
# docker build  --tag jen-soft/debian:8.2  --file=Dockerfile ./
# docker run -it --rm jen-soft/debian:8.2 ls -lah /opt

# END ------------------------------------------------------------------------ #


>_ * alternative usage:
[Dockerfile.py]
try: from pydocker import DockerFile
except ImportError:
    try: from urllib.request import urlopen         # python-3
    except ImportError: from urllib import urlopen  # python-2
    exec(urlopen('https://raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py').read())
#
d = DockerFile(name=os.path.basename(__file__).rsplit('.', 1)[0])
# ...

--------------------------------------------------------------------------------
change log:
    v0.0.1      Tue 30 Apr 2019 06:12:04 AM UTC     jen
            - created

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
import re

# ############################################################################ #


# ############################################################################ #
class DockerFile(object):
    # https://docs.docker.com/engine/reference/builder/
    FROM, LABEL, COPY, RUN, WORKDIR, ENV, SHELL, EXPOSE, ENTRYPOINT, CMD, \
        ADD, STOPSIGNAL, USER, VOLUME, ARG, ONBUILD, HEALTHCHECK, = '*'*17

    def __init__(self, name='Dockerfile'):
        self.content = ''
        self.name = name
        self.files = []

    def __setattr__(self, key, value):
        if key in ['content', 'name', 'files']:
            return super(DockerFile, self).__setattr__(key, value)
        #
        if key in ['WORKDIR', 'SHELL', 'ENTRYPOINT', 'CMD', 'USER', ]:
            self.content += '\n'
        #
        self.content += '{} {}\n'.format(key, value)
        #

    def add_raw(self, text):
        self.content += text

    def file(self, dst_path, content):
        local_name = './{}.{}@{}'.format(
            self.name, len(self.files), os.path.basename(dst_path)
        )
        self.files.append([
            local_name, content,
        ])
        return '{} {}'.format(local_name, dst_path)

    def create_files(self):
        for name in os.listdir('./'):
            if re.findall(r'^{}.[0-9]+@'.format(self.name), name):
                os.remove(name)
        #   #
        for name, content in [[self.name, self.content], *self.files]:
            with open(name, 'w+') as file:
                file.write(content)
                file.flush()
        #   #

    # -------------------------------------------------------------------- #

    def RUN(self, *args):
        for cmd in args:
            self.__setattr__('RUN', cmd)
        #

    def COPY(self, dst_path, content):
        self.__setattr__('COPY', self.file(dst_path, content))

    def RUN_file(self, dst_path, content, keep_file=False):
        self.add_raw('\n')
        self.COPY(dst_path, content + '\n')
        self.RUN = 'chmod +x {}'.format(dst_path)
        self.RUN = dst_path
        if not keep_file:
            self.RUN = 'rm {}'.format(dst_path)
        #

    def RUN_file_python(self, dst_path, fn, keep_file=False):
        if not isinstance(fn, str):
            from inspect import getsource
            fn = '{}\n{}()'.format(getsource(fn), fn.__name__)
        #
        content = '#!/usr/bin/env bash\n# -*- coding: utf-8 -*-\n' + fn
        self.RUN_file(dst_path, content, keep_file)

    def RUN_file_bash(self, dst_path, content, keep_file=False):
        content = '#!/usr/bin/env bash\n' + content
        self.RUN_file(dst_path, content, keep_file)
#

# ############################################################################ #

