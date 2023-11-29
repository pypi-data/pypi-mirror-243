# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_tort_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1']

extras_require = \
{'all': ['isort>=5.12.0',
         'black>=23.9.1',
         'ruff>=0.0.292',
         'typer[all]>=0.9.0',
         'mypy>=1.5.0',
         'coverage>=6.5.0',
         'bumpversion>=0.6.0,<0.7.0',
         'pytest>=7.4.2,<8.0.0']}

entry_points = \
{'console_scripts': ['fast = fast_tort_cli:cli']}

setup_kwargs = {
    'name': 'fast-tort-cli',
    'version': '0.5.1',
    'description': '',
    'long_description': '<p align="center">\n  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>\n  <a href="https://tortoise.github.io"><img src="https://avatars.githubusercontent.com/u/42678965" alt="TortoiseORM"></a>\n</p>\n<p align="center">\n    <em>Toolkit for FastAPI+TortoiseORM projects to runserver/migration/lint ...</em>\n</p>\n<p align="center">\n<a href="https://pypi.org/project/fast-tort-cli" target="_blank">\n    <img src="https://img.shields.io/pypi/v/fast-tort-cli?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/fast-tort-cli" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/fast-tort-cli.svg?color=%2334D058" alt="Supported Python versions">\n</a>\n<a href="https://github.com/waketzheng/fast-tort-cli/actions?query=workflow:ci" target="_blank">\n    <img src="https://github.com/waketzheng/fast-tort-cli/workflows/ci/badge.svg" alt="GithubActionResult">\n</a>\n<a href="https://coveralls.io/github/waketzheng/fast-tort-cli?branch=main" target="_blank">\n    <img src="https://coveralls.io/repos/github/waketzheng/fast-tort-cli/badge.svg?branch=main" alt="Coverage Status">\n</a>\n</p>\n\n---\n\n**Documentation**: <a href="https://waketzheng.github.io/fast-tort-cli" target="_blank">https://waketzheng.github.io/fast-tort-cli</a>\n\n**Source Code**: <a href="https://github.com/waketzheng/fast-tort-cli" target="_blank">https://github.com/waketzheng/fast-tort-cli</a>\n\n## Requirements\n\nPython 3.11+\n\n## Installation\n\n<div class="termy">\n\n```console\n$ pip install "fast-tort-cli[all]"\n---> 100%\nSuccessfully installed fast-tort-cli\n```\n\n## Usage\n\n- Lint py code:\n```bash\nfast lint /path/to/file-or-directory\n```\n- Bump up version in pyproject.toml\n```bash\nfast bump\n```\n- Export requirement file and install `pip install -r `\n```bash\nfast sync\n```\n- Upgrade main/dev dependenices to latest version\n```bash\nfast upgrade\n```\n- Run unittest and report coverage\n```bash\nfast test\n```\n',
    'author': 'Waket Zheng',
    'author_email': 'waketzheng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
