# pydocker
Easy generator Dockerfile for humans

    Let's use power of python for generate dockerfile!
    
    Advantages:
        - all features from python: variables, multiline strings, code reuse.
        - keep all your code in one file [bash, python, conf, ...]
        - generate many docker files from one template [testing, production, ]
        - generate sequence [Dockerfile.debian => Dockerfile.python => Dockefile.yourapp, ...]
        - or if you not expert in sed, awk - you can use python for modify conf files : )
<a href="https://github.com/jen-soft/pydocker/blob/master/pydocker.py#L104" target="_blank">easy code, easy costomize</a>

# Install
<pre>sudo wget -v -N raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py  "$(python -m site --user-site)/pydocker.py"</pre>

# Using 
<pre># Dockerfile.py</pre>
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
```

<pre>
# >_ console:

python3 Dockerfile.py
ls -lah
cat -n Dockerfile
docker build  --tag jen-soft/debian:8.2  --file=Dockerfile ./
docker run -it --rm jen-soft/debian:8.2 ls -lah /opt

</pre>


## Alternative usage:
<pre>
try: from pydocker import DockerFile
except ImportError:
    try: from urllib.request import urlopen         # python-3
    except ImportError: from urllib import urlopen  # python-2
    exec(urlopen('raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py').read())
#
d = DockerFile(name=os.path.basename(__file__).rsplit('.', 1)[0])
# ...
</pre>
