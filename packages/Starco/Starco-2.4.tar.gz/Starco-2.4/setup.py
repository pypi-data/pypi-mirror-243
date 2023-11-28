from setuptools import setup,find_packages
import os,glob
requires = [
    'cffi==1.15.1',
    'cryptography==41.0.3',
    'pycparser==2.21',
    'beautifulsoup4==4.12.2',
    'lxml==4.9.3',
    'requests==2.31.0',
    'easy-db==0.9.15',
    'hcloud==1.26.0',
    'cloudflare==2.11.6',
    'python-socks==2.4.3'


]

# packages = [ '/'.join(i.split('/')[-2:]) for i in glob.glob('./starco/*') if os.path.isdir(i)]
# packages =['/'+i for i in packages]
setup(
    name = 'Starco',
    version='2.4',
    author='Mojtaba Tahmasbi',
    packages=find_packages(),
    install_requires=requires,
)