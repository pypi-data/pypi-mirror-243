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
    'version': '0.1.1',
    'description': "A Python implementation of Viasat's NIMO modem interface project.",
    'long_description': '# pynimomodem\n\nA Python implementation of the [Viasat](www.viasat.com)\nNIMO modem interface for satellite IoT.\n\nNIMO stands for **Non-IP Modem Orbcomm** waveform\nand represents a family of low cost satellite data modems that use network\nprotocols developed by [ORBCOMM](www.orbcomm.com)\nincluding [IsatData Pro](https://www.inmarsat.com/en/solutions-services/enterprise/services/isatdata-pro.html) and its successor, OGx.\n\nThese ORBCOMM protocols can operate over the Viasat L-band global network in\ncooperation with a varietry of authorized Viasat IoT service partners, and\nare intended for event-based remote data collection and device control.\n\nExample NIMO modems available:\n* [ORBCOMM ST2100](https://www.orbcomm.com/en/partners/iot-hardware/st-2100)\n* [Quectel CC200A-LB](https://www.quectel.com/product/cc200a-lb-satellite-communication-module)\n* [uBlox UBX-S52](https://content.u-blox.com/sites/default/files/documents/UBX-R52-S52_ProductSummary_UBX-19026227.pdf)',
    'author': 'geoffbrucepayne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inmarsat-enterprise/pynimomodem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
