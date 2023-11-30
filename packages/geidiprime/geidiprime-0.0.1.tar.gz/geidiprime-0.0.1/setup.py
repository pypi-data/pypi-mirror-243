# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geidi_prime']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'local-attention', 'torch', 'zetascale']

setup_kwargs = {
    'name': 'geidiprime',
    'version': '0.0.1',
    'description': 'Paper - Pytorch',
    'long_description': "[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# GeidiPrime\nThis is an extremely experimental Transformer architecture with Macaron like FFNs with local attention. Perhap's we can add the visual expert from Zeta and make it multi-modal!\n\n\n# Install\n\n## Usage\n```python\nimport torch\nfrom geidi_prime.model import GeidiPrimeTransformer\n\nmodel = GeidiPrimeTransformer(\n    dim=4096,\n    depth=6,\n    heads=8,\n    num_tokens=20000,\n)\n\nx = torch.randint(0, 20000, (1, 4096))\n\nout = model(x)\nprint(out.shape)\n\n```\n\n\n\n# License\nMIT\n\n\n\n",
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/GiediPrime',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
