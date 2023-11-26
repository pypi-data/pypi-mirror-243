# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uconst']

package_data = \
{'': ['*']}

install_requires = \
['urllib3>=2.0.7,<3.0.0']

setup_kwargs = {
    'name': 'uconst',
    'version': '1.0.1',
    'description': '',
    'long_description': '# uconst\nSimple url constructor library.\n\n```python\nimport uconst\n\nc = uconst.Constructor("api.example.org")\n\nprint(c) # == str(c)\n\nc = c / "api" / ["v2", "get_smth"]\n\nprint(c.as_str())\n```\n',
    'author': 'Robert Stoul',
    'author_email': 'rekiiky@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
