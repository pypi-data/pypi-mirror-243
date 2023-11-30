# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynimomodem']

package_data = \
{'': ['*']}

extras_require = \
{'pyserial': ['pyserial>=3.5,<4.0']}

setup_kwargs = {
    'name': 'pynimomodem',
    'version': '0.2.0',
    'description': "A Python implementation of Viasat's NIMO modem interface project.",
    'long_description': "# pynimomodem\n\nA Python implementation of the [Viasat](www.viasat.com)\nNIMO modem interface for satellite IoT.\n\nNIMO stands for **Non-IP Modem Orbcomm** waveform\nand represents a family of low cost satellite data modems that use network\nprotocols developed by [ORBCOMM](www.orbcomm.com)\nincluding [IsatData Pro](https://www.inmarsat.com/en/solutions-services/enterprise/services/isatdata-pro.html) and its successor, OGx.\n\nThese ORBCOMM protocols can operate over the Viasat L-band global network in\ncooperation with a varietry of authorized Viasat IoT service partners, and\nare intended for event-based remote data collection and device control.\n\nExample NIMO modems available:\n* [ORBCOMM ST2100](https://www.orbcomm.com/en/partners/iot-hardware/st-2100)\n* [Quectel CC200A-LB](https://www.quectel.com/product/cc200a-lb-satellite-communication-module)\n* [uBlox UBX-S52](https://content.u-blox.com/sites/default/files/documents/UBX-R52-S52_ProductSummary_UBX-19026227.pdf)\n\n## Additional Information\n\n* [API Documentation](https://inmarsat-enterprise.github.io/pynimomodem/)\n\n> [!NOTE]\n> Obsoletes/replaces the Inmarsat `idpmodem` project, when combined with the\n> [`pynimcodec`](github.com/inmarsat-enterprise/pynimcodec) library.\n\n## Background\n\n### Overview\n\n*IsatData Pro* (**IDP**)is a store-and-forward satellite messaging technology\nwith flexible message sizes:\n\n* up to 6400 bytes Mobile-Originated (aka **MO**, From-Terminal, *Return*)\n* up to 10000 bytes Mobile-Terminated (aka **MT**, To-Terminal, *Forward*)\n\n***Message***s are sent to or collected from a ***Mobile*** using its globally\nunique *Mobile ID*,\ntransacted through a ***Mailbox*** that provides authentication, encryption and\ndata segregation for cloud-based or enterprise client applications via a\nREST **Messaging API**.\n\nData sources and controls in the field are interfaced to a modem using a serial\ninterface with *AT commands* to send and receive messages, check network status,\nand optionally use the built-in *Global Navigation Satellite System* (GNSS)\nreceiver to determine location-based information.\n\nThe first byte of the message is referred to as the\n*Service Identification Number* (**SIN**) where values below 16 are reserved\nfor system use.  SIN is intended to capture the concept of embedded\nmicroservices used by an application.\n\nThe second byte of the message can optionally be defined as the\n*Message Identifier Number* (**MIN**) intended to support remote operations \nwithin each embedded microservice with defined binary formatting.\nThe MIN concept also supports the optional *Message Definition File* feature\nallowing an XML file to be applied which presents a JSON-tagged message\nstructure on the network API.\n\n### Modem Concept of Operation\n\n1. Upon power-up or reset, the modem first acquires its location using \nGlobal Navigation Satellite Systems (GNSS).\n1. After getting its location, the modem tunes to the correct frequency, then\nregisters on the network.  Once registered it can communicate on the\nnetwork.\n1. MO messages are submitted by a microcontroller or IoT Edge device, which\nthen must monitor progress until the message is complete (either delivered or\ntimed out/failed due to blockage). Completed messages must be cleared from the\nmodem transmit queue by querying state(s) either periodically or when prompted\nby the modem's event notification pin if configured.\n1. MT messages that arrive are stored in the receive queue and the Edge device\nqueries for *New* MT messages periodically or when prompted by the modem's\nevent notification pin if configured.\n1. Network acquisition status can also be queried using AT commands.\n1. If the modem cannot find the target frequency it begins to search for other\nfrequencies from a configuration map in its non-volatile memory. It will cycle\nthrough beam acquisition attempts for a period of time before falling back to\na globally-accessible *Bulletin Board* frequency where it may need to download\na new network configuration before re-attempting. Bulletin board downloads\ntypically take less than 15 minutes but can take longer in low signal or high\ninterference locations. A modem should not be powered off during Bulletin\nBoard download.\n1. Prolonged obstruction of satellite signal will put the modem into *blockage*\nstate from which it will automatically try to recover based on an algorithm\ninfluenced by its *power mode* setting.",
    'author': 'geoffbrucepayne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inmarsat-enterprise/pynimomodem',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
