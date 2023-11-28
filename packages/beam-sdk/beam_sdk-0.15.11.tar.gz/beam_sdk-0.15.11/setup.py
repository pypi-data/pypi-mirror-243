# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src', 'beam': 'src/beam', 'beam.utils': 'src/beam/utils'}

packages = \
['beam', 'beam.utils']

package_data = \
{'': ['*'], 'beam': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'astor>=0.8.1,<0.9.0',
 'croniter>=1.3.7,<2.0.0',
 'importlib-metadata==5.2.0',
 'marshmallow-dataclass>=8.5.9,<9.0.0',
 'marshmallow==3.18.0',
 'typeguard>=2.13.3,<3.0.0',
 'typing-extensions>=4.7.1,<5.0.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'beam-sdk',
    'version': '0.15.11',
    'description': '',
    'long_description': 'None',
    'author': 'beam.cloud',
    'author_email': 'support@beam.cloud',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
