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
    'version': '0.1.3',
    'description': 'Convienience wrapper for common pyenv operations.',
    'long_description': '# PyEnv Tool\n\nA convienience wrapper for common pyenv operations.\n\nThis tool is designed for Python developers who primarily use pyenv to keep\na complete array of up-to-date Python executables installed. This tool should\nbe considered porcelain to pyenv\'s plumbing, but NOT as a complete interface\nreplacement. Many pyenv operations will still need to be perfomed via pyenv\'s\ninterface.\n\n## Operational Goal\n\n`pyenvtool` is built around the concept of a "main" version which is composed\nof a major and minor version, but ignores any bugfix, prerelease, or build\ninformation. That is, `3.11.0`, `3.11-dev`, and `3.11.2` are all the same\n"main" version of `3.11`.\n\n`pyenvtool` operates with the goal that any existing main version of Python\nshould be left on the system, but updated if possible, and any supported main\nversions of Python should be installed if absent.\n\n-   For every main version that is _supported_ and _not present_ on the system:\n\n    -   The latest bugfix version is installed\n\n-   For every main version that is _supported_ and _present_ on the system:\n\n    -   The latest bugfix version is installed if not already present\n    -   Bugfix versions _prior_ to the latest are uninstalled, unless the\n        `--keep-bugfix` option is provided\n\n-   For every main version that is _unsupported_ and _present_ on the system:\n    -   The latest bugfix version is installed if not already present, unless the\n        `--remove-minor` option is provided\n    -   Bugfix versions _prior_ to the latest are uninstalled, unless the\n        `--keep-bugfix` option is provided\n\n## Usage\n\nComplete help documentation can be found by running `pyenvtool --help`, the\nfollowing is only a quick-start introduction.\n\nThe primary usage will be the `pyenvtool upgrade` command, which will perform\nwhatever pyenv operations are required to leave the system with a complete\narray of up-to-date Python executables. By default, this command will:\n\n-   Scrape python.org to determine which Python versions are currently supported\n-   Update pyenv with the latest list of available versions (and possibly also\n    update the pyenv tool itself).\n-   Update any installed Python versions to the latest bugfix version (by\n    installing the new version and uninstalling any old versions)\n-   Install any supported Python versions, at the latest bugfix, which are not\n    currently installed\n-   Uninstall any unsupported Python versions EXCEPT for the latest bugfix\n\nThis behavior can be changed with the following command arguments:\n\n`--keep-bugfix/-k`\nKeep any existing python versions even if a newer bugfix is available.\n\n`--remove-minor/-r`\nRemove ALL unsupported python versions, including the latest bugfix.\n\n`--no-update`\nDo not update the pyenv tool or the list of available versions\n\n`--dry-run/-n`\nCheck the system and determine the necessary changes, but do not execute\nthem.\n\n## Installation\n\nTo install `pyenvtool`, run the following command. `python3` should point to\nwhatever Python binary you want to install it under, version 3.8 or later.\n\n    python3 -m pip install pyenvtool\n\n### Prerequisites\n\nThis tool requires `pyenv` to be installed and available in the path. The\n`pyenv` project can be found at https://github.com/pyenv/pyenv along with\ndocumentation and installation instructions.\n\n## Credits\n\nThis package was created with\n[Cookiecutter](https://github.com/audreyr/cookiecutter) and the\n[zanfar/cookiecutter-pypackage](https://gitlab.com/zanfar/cookiecutter-pypackage)\nproject template.\n',
    'author': 'Matthew Wyant',
    'author_email': 'me@matthewwyant.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/therealzanfar/pyenvtool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
