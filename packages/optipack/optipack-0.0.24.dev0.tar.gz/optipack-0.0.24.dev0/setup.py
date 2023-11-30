# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optipack',
 'optipack.core',
 'optipack.core.automl.builder',
 'optipack.core.automl.runner',
 'optipack.core.fileio',
 'optipack.core.logger',
 'optipack.core.manager',
 'optipack.core.visualizer',
 'optipack.internal_utils',
 'optipack.sdk']

package_data = \
{'': ['*'], 'optipack': ['.config/*', 'asset/*']}

install_requires = \
['Pillow==9.4.0',
 'fastcore>=1.5,<2.0',
 'fs-gcsfs>=1.5.1,<2.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'protobuf>=3.20.2,<4.0.0',
 'pyyaml==6.0',
 'rich==13.3.1',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['optipack = optipack.__main__:start']}

setup_kwargs = {
    'name': 'optipack',
    'version': '0.0.24.dev0',
    'description': 'The optimal ML package',
    'long_description': "![optipack](asset/image/logo.png)\n\n# What optipack do: \n- Workspace management: \n    - Generate folder structure for ML project \n    - Generate files following the given environment in yaml format, including: \n        - tool connection configuration \n        - hyperparameter configuration \n        - model run config\n-  Logging: 🔥 all-in-one logger\n    - Support console/file logger for users' log! 🔥 No more uggly print, no more terminal scrolling\n    - Support tensorboard metric log. \n\n# Installation:  \n## 1. Installation from PYPI: \n- Run `pip install optipack`\n## 2. Installation from source: \n- Clone this repo \n- Change directory to optipack\n- Run `pip install . `\n\n# How to use: \n## 1. Use as CLI \n- All you need is running `optipack` on terminal :) \n\n## 2. Use as library\n- ... ",
    'author': 'indigoYoshimaru',
    'author_email': 'None',
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
