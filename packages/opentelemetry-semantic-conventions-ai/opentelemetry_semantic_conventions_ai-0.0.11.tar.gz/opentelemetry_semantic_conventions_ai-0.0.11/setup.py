# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'opentelemetry-semantic-conventions-ai',
    'version': '0.0.11',
    'description': 'OpenTelemetry Semantic Conventions Extension for Large Language Models',
    'long_description': '# opentelemetry-semantic-conventions-llm\n\nProject description here.\n',
    'author': 'Gal Kleinman',
    'author_email': 'gal@traceloop.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
