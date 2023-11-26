# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['environment_backups',
 'environment_backups._legacy',
 'environment_backups.backups',
 'environment_backups.config',
 'tests',
 'tests.unit',
 'tests.unit.backups',
 'tests.unit.config']

package_data = \
{'': ['*'], 'tests': ['fixtures/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'deprecated>=1.2.14,<2.0.0',
 'google-api-python-client>=2.100.0,<3.0.0',
 'google-auth-httplib2>=0.1.1,<0.2.0',
 'google-auth-oauthlib>=1.1.0,<2.0.0',
 'pydantic>=2.4.2,<3.0.0',
 'pyzipper>=0.3.6,<0.4.0',
 'rich>=13.4.1,<14.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['environment-backups = environment_backups.cli:main',
                     'environment-backups-l = '
                     'environment_backups._legacy.cli:main_arg_parser']}

setup_kwargs = {
    'name': 'environment-backups',
    'version': '1.0.1',
    'description': 'CLI Application to backup environment variables..',
    'long_description': '# Environment backups\n\n\n\n\nCLI Application to backup environment variables.\n\n# Installation\n\n\n# Examples\n\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Luis C. Berrocal',
    'author_email': 'luis.berrocal.1942@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/luiscberrocal/environment-backups',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
