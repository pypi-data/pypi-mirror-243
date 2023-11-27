# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['izaber_wamp']

package_data = \
{'': ['*']}

install_requires = \
['cbor2>=4.1.2', 'izaber>=3.1.20231029', 'swampyer>=3.0.20231027']

setup_kwargs = {
    'name': 'izaber-wamp',
    'version': '3.0.20231125a2',
    'description': 'Base load point for iZaber WAMP code',
    'long_description': 'None',
    'author': 'Aki Mimoto',
    'author_email': 'aki@zaber.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0',
}


setup(**setup_kwargs)
