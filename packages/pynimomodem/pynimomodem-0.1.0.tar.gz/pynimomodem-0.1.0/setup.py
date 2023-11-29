# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynimomodem']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'pynimomodem',
    'version': '0.1.0',
    'description': "A Python implementation of Viasat's NIMO modem interface project.",
    'long_description': None,
    'author': 'geoffbrucepayne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
