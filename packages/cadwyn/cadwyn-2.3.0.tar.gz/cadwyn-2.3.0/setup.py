# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cadwyn', 'cadwyn.structure']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.96.1',
 'pydantic>=1.10.0,<2.0.0',
 'typing-extensions',
 'verselect-zmievsa>=0.0.5']

extras_require = \
{'cli': ['typer>=0.7.0']}

entry_points = \
{'console_scripts': ['cadwyn = cadwyn.__main__:app']}

setup_kwargs = {
    'name': 'cadwyn',
    'version': '2.3.0',
    'description': 'Modern Stripe-like API versioning in FastAPI',
    'long_description': '# Cadwyn\n\nModern [Stripe-like](https://stripe.com/blog/api-versioning) API versioning in FastAPI\n\n---\n\n<p align="center">\n<a href="https://github.com/zmievsa/cadwyn/actions?query=workflow%3ATests+event%3Apush+branch%3Amain" target="_blank">\n    <img src="https://github.com/zmievsa/cadwyn/actions/workflows/test.yaml/badge.svg?branch=main&event=push" alt="Test">\n</a>\n<a href="https://codecov.io/gh/ovsyanka83/cadwyn" target="_blank">\n    <img src="https://img.shields.io/codecov/c/github/ovsyanka83/cadwyn?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://pypi.org/project/cadwyn/" target="_blank">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/cadwyn?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/cadwyn/" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/cadwyn?color=%2334D058" alt="Supported Python versions">\n</a>\n</p>\n\n## Who is this for?\n\nCadwyn allows you to support a single version of your code, auto-generating the code/routes for older versions. You keep versioning encapsulated in small and independent "version change" modules while your business logic knows nothing about versioning.\n\nIts [approach](./docs/theory.md#ii-migration-based-response-building) will be useful if you want to:\n\n1. Support many (>2) API versions for a long time\n2. Effortlessly backport features and bugfixes to older API versions\n\n## Get started\n\nThe [documentation](https://docs.cadwyn.dev) has everything you need to get started. It is recommended to read it in the following order:\n\n1. [Tutorial](./tutorial.md)\n2. [Recipes](./recipes.md)\n3. [Reference](./reference.md)\n4. [Theory](./theory.md) <!-- TODO: Move section about cadwyn\'s approach to the beginning and move other approaches and "how we got here" to another article  -->\n\n## Similar projects\n\nThe following projects are trying to accomplish similar results with a lot more simplistic functionality.\n\n- <https://github.com/sjkaliski/pinned>\n- <https://github.com/phillbaker/gates>\n- <https://github.com/lukepolo/laravel-api-migrations>\n- <https://github.com/tomschlick/request-migrations>\n- <https://github.com/keygen-sh/request_migrations>\n',
    'author': 'Stanislav Zmiev',
    'author_email': 'zmievsa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zmievsa/cadwyn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
