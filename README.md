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
<pre>
F=$(python -c "import site; print(site.getsitepackages()[0]+'/pydocker.py')")
sudo wget -v -N raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py -O $F
</pre>

# Using 
<pre># Dockerfile.py</pre>
```python
import sys
import logging
import pydocker  # github.com/jen-soft/pydocker

logging.getLogger('').setLevel(logging.INFO)
logging.root.addHandler(logging.StreamHandler(sys.stdout))


class DockerFile(pydocker.DockerFile):
    '''   add here your custom features   '''

d = DockerFile(base_img='debian:8.2', name='jen-soft/custom-debian:8.2')

d.RUN_bash_script('/opt/set_repo.sh', r'''
```
```bash
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
```
```python
''')

d.EXPOSE = 80
d.WORKDIR = '/opt'

# d.ENTRYPOINT = ["/opt/www-data/entrypoint.sh"]
d.CMD = ["python", "--version"]

d.build_img()

```

```bash
# >_ console:

python3 Dockerfile.py
docker images
```


## Alternative usage (without installation):
```python
try: from pydocker import DockerFile
except ImportError:
    try: from urllib.request import urlopen         # python-3
    except ImportError: from urllib import urlopen  # python-2
    exec(urlopen('https://raw.githubusercontent.com/jen-soft/pydocker/master/pydocker.py').read())
#
d = DockerFile(base_img='debian:8.2', name='jen-soft/custom-debian:8.2')
# ...
```
