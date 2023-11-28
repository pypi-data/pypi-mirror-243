# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coges']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'coges',
    'version': '0.8.0',
    'description': 'Library for implementing non-linear behaviour and stream processing',
    'long_description': '* Coges\nLibrary for implementing non-linear behaviour and stream processing\n\n** Features\n- Predicate -> Action based flow control\n- Can be used as multi-state and single-state finite machine\n- Built-in dependency injector with lazy resolving and dependency tree\n- Functional approach\n- Concurrent predicate and action running\n- State checks are connected to your stream\n',
    'author': 'Jellyfish.tech',
    'author_email': 'manager@jellyfish.tech',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
