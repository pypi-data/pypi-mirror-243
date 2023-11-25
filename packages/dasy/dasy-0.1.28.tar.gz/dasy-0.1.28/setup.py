# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dasy', 'dasy.builtin', 'dasy.parser']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'dasy-hy==0.24.2',
 'eth-abi>=4.0.0,<5.0.0',
 'eth-typing>=3.2.0,<4.0.0',
 'hyrule>=0.2,<0.3',
 'py-evm>=0.6.1a2',
 'pytest>=7.1.3,<8.0.0',
 'vyper>=0.3.10,<0.4.0']

entry_points = \
{'console_scripts': ['dasy = dasy:main']}

setup_kwargs = {
    'name': 'dasy',
    'version': '0.1.28',
    'description': 'an evm lisp',
    'long_description': 'None',
    'author': 'z80',
    'author_email': 'z80@ophy.xyz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
