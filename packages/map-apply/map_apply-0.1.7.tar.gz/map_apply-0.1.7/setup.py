# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['map_apply', 'map_apply.scripts']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0']

entry_points = \
{'console_scripts': ['map_apply = map_apply.scripts.map_apply:main']}

setup_kwargs = {
    'name': 'map-apply',
    'version': '0.1.7',
    'description': "Copies the input file and substitute one keyfield with another using 'map' file",
    'long_description': None,
    'author': 'Smirnov Sergey',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
