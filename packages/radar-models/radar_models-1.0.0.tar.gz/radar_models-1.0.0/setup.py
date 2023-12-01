# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radar_models']

package_data = \
{'': ['*']}

install_requires = \
['sqlmodel>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'radar-models',
    'version': '1.0.0',
    'description': 'DB models for Radar',
    'long_description': '# radar-models',
    'author': 'Andrew Atterton',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
