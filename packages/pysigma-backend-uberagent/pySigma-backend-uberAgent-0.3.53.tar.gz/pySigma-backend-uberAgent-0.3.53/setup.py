# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.backends.uberagent', 'sigma.pipelines.uberagent']

package_data = \
{'': ['*']}

install_requires = \
['pysigma>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'pysigma-backend-uberagent',
    'version': '0.3.53',
    'description': 'pySigma uAQL backend',
    'long_description': 'None',
    'author': 'vast limits GmbH',
    'author_email': 'info@vastlimits.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vastlimits/pySigma-backend-uberAgent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
