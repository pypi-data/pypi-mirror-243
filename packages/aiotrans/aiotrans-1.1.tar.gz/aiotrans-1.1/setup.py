# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiotrans', 'aiotrans.cache', 'aiotrans.cache.storage', 'aiotrans.transport']

package_data = \
{'': ['*']}

install_requires = \
['uconst>=1.0.1,<2.0.0']

extras_require = \
{'aiohttp': ['aiohttp>=3.8.6,<4.0.0'], 'httpx': ['httpx>=0.25.1,<0.26.0']}

setup_kwargs = {
    'name': 'aiotrans',
    'version': '1.1',
    'description': '',
    'long_description': '# Simple async Google Translate library\n\n#### Instalation:\n```pip install aiotrans[aiohttp]``` or ```pip install aiotrans[httpx]```\n\n#### Featrures\n* Fast and reliable - it uses the same servers that translate.google.com uses\n* Support for httpx and aiohttp\n* Fully asyncio support\n* Simple result caching\n\n#### Example\n```python\nfrom asyncio import run\n\nfrom aiotrans import Translaitor\n\n\nasync def main():\n    t = Translaitor()\n    print(await t.translate("Hello", target=\'ru\', source=\'en\'))\n\n    await t.transport.close()\n\nrun(main())\n```\n',
    'author': 'Robert Stoul',
    'author_email': 'rekiiky@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
