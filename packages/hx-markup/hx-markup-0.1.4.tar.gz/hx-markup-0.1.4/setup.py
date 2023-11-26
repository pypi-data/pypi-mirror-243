# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hx_markup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hx-markup',
    'version': '0.1.4',
    'description': 'HTML markup using python classes, including HTMX language.',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
