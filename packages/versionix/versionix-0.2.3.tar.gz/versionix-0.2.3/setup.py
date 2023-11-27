# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versionix']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0', 'rich-click>=1.7.1,<2.0.0']

entry_points = \
{'console_scripts': ['versionix = versionix.scripts:main']}

setup_kwargs = {
    'name': 'versionix',
    'version': '0.2.3',
    'description': 'Get version of any tools',
    'long_description': 'Versionix\n###########\n\n\n.. image:: https://badge.fury.io/py/versionix.svg\n    :target: https://pypi.python.org/pypi/versionix\n\n\n.. image:: https://github.com/sequana/versionix/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/sequana/versionix/actions/workflows/main.yml\n\n.. image:: https://coveralls.io/repos/github/sequana/versionix/badge.svg?branch=main\n    :target: https://coveralls.io/github/sequana/versionix?branch=main\n\n.. image:: https://zenodo.org/badge/658721856.svg\n   :target: https://zenodo.org/badge/latestdoi/658721856\n\n:Python version: Python 3.8, 3.9, 3.10, 3.11\n:Source: See  `http://github.com/sequana/versionix <https://github.com/sequana/versionix/>`__.\n:Issues: Please fill a report on `github <https://github.com/sequana/versionix/issues>`__\n\nOverview\n========\n\nVersionix is a simple tool that attemps to print on screen the version of a given standalone.\n\nInstallation\n----------------\n\nIf you are in a hurry, just type::\n\n    pip install versionix  --upgrade\n\nThis is pure Python so no need for fancy libraries.\n\nUsage\n-----\n\nThen, just type e.g::\n\n    versionix  fastqc\n\nThis tool uses a registry so it will work only with resgistered tools, which list can be obtained with::\n\n    versionix --registered\n\nType::\n\n    versionix --help \n\nto get more help like this example:\n\n.. image:: doc/versionix_usage.png\n\n\nDESCRIPTION\n===========\n\n\nThe first difficulty is that standalone applications have different ways to obtain their version information. Some require the use of a long or short argument (--version or -v), while others do not require any argument at all. In addition, display channels (stdout or stderr) and formats of the version output differs between applications. To handle these various cases, we define a dictionnary of **metadata** related to the different standalones. These metadata helps in the identification of the command to run, the options to use, if the information is directed to stdout or stderr and the method to parse the output to obtain the version number.\n\nVersionix is designed to be used with all Sequana pipelines and is not intended to be universal. It will only work for tools that are registered. You can add your own standalone version in the versionix/register.py file and provide a Pull Request.\n\nChangelog\n=========\n\n========= ========================================================================\nVersion   Description\n========= ========================================================================\n0.2.3     More tools in the registry\n0.2.2     add all tools required by sequana pipelines (oct 2023)\n0.2.1     More tools added.\n0.2       simplification. Add tests. Add more tools\n0.1       first draft\n========= ========================================================================\n',
    'author': 'Sequana Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sequana/versionix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
