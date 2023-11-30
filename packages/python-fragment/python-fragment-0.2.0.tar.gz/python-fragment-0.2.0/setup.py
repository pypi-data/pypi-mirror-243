# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['fragment', 'fragment.resources']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.6,<4.0.0', 'selectolax[cython]>=0.3.17,<0.4.0']

setup_kwargs = {
    'name': 'python-fragment',
    'version': '0.2.0',
    'description': 'Reverse engineered Fragment API that mimics the official webclient',
    'long_description': '# python-fragment\n<p align="center">\n  <a href="https://github.com/ren3104/python-fragment/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ren3104/python-fragment" alt="GitHub license"></a>\n  <a href="https://pypi.org/project/python-fragment"><img src="https://img.shields.io/pypi/v/python-fragment?color=blue" alt="PyPi package version"></a>\n  <a href="https://pypi.org/project/python-fragment"><img src="https://img.shields.io/pypi/pyversions/python-fragment.svg" alt="Supported python versions"></a>\n</p>\n\n## Features\n- Fast and asynchronous\n- Fully typed\n- Easy to contribute and use\n\n## Installation\n```shell\npip install -U python-fragment\n```\nOr using poetry:\n```shell\npoetry add python-fragment\n```\n\n## Quick Start\n```python\nfrom fragment import FragmentAPI\n\nimport asyncio\n\n\nasync def main():\n    api = FragmentAPI()\n    async with api:\n        # Get username auctions\n        usernames = await api.usernames.search()\n        for username in usernames[:5]:\n            print(username)\n            # {\n            #     \'username\': \'lynx\',\n            #     \'status\': \'auction\',\n            #     \'value\': 6619.0,\n            #     \'datetime\': \'2023-10-31T06:11:25+00:00\',\n            #     \'is_resale\': False\n            # }\n\n\nasyncio.run(main())\n```\n',
    'author': 'ren3104',
    'author_email': '2ren3104@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ren3104/python-fragment',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
