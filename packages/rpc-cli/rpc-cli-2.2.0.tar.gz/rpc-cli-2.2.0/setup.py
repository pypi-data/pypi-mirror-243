# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpc_cli']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=2.0.1,<3.0.0', 'openrpc>=9.0.0,<10.0.0', 'pydantic>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'rpc-cli',
    'version': '2.2.0',
    'description': 'Expose methods of an RPC server through a CLI.',
    'long_description': '# RPC to CLI\n\n![](https://img.shields.io/badge/License-ApacheV2-blue.svg)\n![](https://img.shields.io/badge/code%20style-black-000000.svg)\n![](https://img.shields.io/pypi/v/rpc-cli.svg)\n\nWrapper for [Python OpenRPC](https://python-openrpc.burkard.cloud/) to expose the\nmethods of an RPC Server through a CLI.\n\n## Install\n\nRPC CLI is on PyPI and can be installed with:\n\n```shell\npip install rpc-cli\n```\n\nOr with [Poetry](https://python-poetry.org/)\n\n```shell\npoetry add rpc-cli\n```\n\n## Example\n\nGiven the following in a file `demo.py`.\n\n```python\nfrom openrpc import RPCServer\nfrom pydantic import BaseModel\n\nfrom rpc_cli import cli\n\nrpc = RPCServer()\n\n\nclass Vector3(BaseModel):\n    x: float\n    y: float\n    z: float\n\n\n@rpc.method()\ndef get_distance(a: Vector3, b: Vector3) -> Vector3:\n    """Get distance between two points."""\n    return Vector3(x=a.x - b.x, y=a.y - b.y, z=a.z - b.z)\n\n\n@rpc.method()\ndef divide(a: int, b: int) -> float:\n    """Divide two integers."""\n    return a / b\n\n\n@rpc.method()\ndef summation(numbers: list[int | float]) -> int | float:\n    """Summ all numbers in a list."""\n    return sum(numbers)\n\n\nif __name__ == "__main__":\n    cli(rpc).run()\n```\n\nYou now have a CLI.\n\n![Demo](https://gitlab.com/mburkard/rpc-cli/-/raw/main/docs/demo.png)\n\n### Using the CLI\n\nMethods can be called as such, notice arrays and object parameters are passed as JSON\nstrings.\n\n```shell\npython demo.py get_distance \'{"x": 1, "y": 1, "z": 1}\' \'{"x": 1, "y": 1, "z": 1}\'\npython demo.py divide 6 2\npython demo.py summation \'[1, 2, 3]\'\n```\n\n## Auto Completions\n\nThis library uses [cleo](https://github.com/python-poetry/cleo), auto completions can be\nmade by following the instructions in the\n[cleo docs](https://cleo.readthedocs.io/en/latest/introduction.html#autocompletion).\n\n## Support The Developer\n\n<a href="https://www.buymeacoffee.com/mburkard" target="_blank">\n  <img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png"\n       width="217"\n       height="60"\n       alt="Buy Me A Coffee">\n</a>\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/rpc-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
