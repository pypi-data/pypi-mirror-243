# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aipkgs_core', 'aipkgs_core.encryption', 'aipkgs_core.utils']

package_data = \
{'': ['*']}

install_requires = \
['email-validator>=1.1.3,<2.0.0',
 'emoji>=2.0.0,<3.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'phonenumbers>=8.12.54,<9.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'aipkgs-core',
    'version': '0.3.5',
    'description': '',
    'long_description': '',
    'author': 'Alexy',
    'author_email': 'alexy.ib@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/aipy/public/packages.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
