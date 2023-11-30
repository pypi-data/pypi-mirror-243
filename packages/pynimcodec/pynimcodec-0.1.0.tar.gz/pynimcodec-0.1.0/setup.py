# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['messagecodecs', 'messagecodecs.nimo', 'messagecodecs.nimo.fields']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pynimcodec',
    'version': '0.1.0',
    'description': 'Codecs for Satellite IoT messaging implemented in Python.',
    'long_description': '# pynimcodec\n\nA set of message codecs for use with satellite IoT products implemented\nin Python.',
    'author': 'geoffbrucepayne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inmarsat-enterprise/pynimomodem',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
