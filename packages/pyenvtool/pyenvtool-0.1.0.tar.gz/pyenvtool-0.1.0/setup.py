# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyenvtool', 'pyenvtool.tests']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12.2,<5.0.0',
 'click>=8.1.7,<9.0.0',
 'requests>=2.31.0,<3.0.0',
 'rich>=13.7.0,<14.0.0']

entry_points = \
{'console_scripts': ['pyenvtool = pyenvtool.__main__:cli_main']}

setup_kwargs = {
    'name': 'pyenvtool',
    'version': '0.1.0',
    'description': 'Convienience wrapper for common pyenv operations.',
    'long_description': 'None',
    'author': 'Matthew Wyant',
    'author_email': 'me@matthewwyant.com',
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
