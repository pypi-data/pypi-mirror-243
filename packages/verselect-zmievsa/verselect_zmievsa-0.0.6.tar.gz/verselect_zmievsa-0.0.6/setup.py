# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verselect', 'verselect.docs']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.103.1', 'httpx>=0.25.0', 'jinja2>=3.1.2']

setup_kwargs = {
    'name': 'verselect-zmievsa',
    'version': '0.0.6',
    'description': '',
    'long_description': 'None',
    'author': 'Bogdan Evstratenko',
    'author_email': 'evstrat.bg@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/team-monite/verselect',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
