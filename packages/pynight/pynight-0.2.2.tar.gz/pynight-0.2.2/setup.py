# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynight']

package_data = \
{'': ['*']}

install_requires = \
['aiofile',
 'brish>=0.3.3,<0.4.0',
 'dnspython>=2.1.0,<3.0.0',
 'executing>=1.2.0,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'openai>=0.27.2,<0.28.0',
 'pyperclip>=1.8.2,<2.0.0',
 'spacy>=3.5.1,<4.0.0',
 'tiktoken>=0.3.3,<0.4.0']

entry_points = \
{'console_scripts': ['semantic-scholar-get = pynight.common_ss:main']}

setup_kwargs = {
    'name': 'pynight',
    'version': '0.2.2',
    'description': 'My Python utility library.',
    'long_description': 'None',
    'author': 'NightMachinary',
    'author_email': 'rudiwillalwaysloveyou@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
