try:
  from setuptools import setup
except:
  from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'chrissav',
    'url': 'URL',
    'download_url': 'download url',
    'author_email': 'myemail',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
    }

setup(**config)
