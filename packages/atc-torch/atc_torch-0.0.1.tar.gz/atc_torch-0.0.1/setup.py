# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['attnconv']

package_data = \
{'': ['*']}

install_requires = \
['einops', 'torch']

setup_kwargs = {
    'name': 'atc-torch',
    'version': '0.0.1',
    'description': 'atc-torch - Pytorch',
    'long_description': '[![Multi-Modality](agorabanner.png)](https://discord.gg/qUtxnK2NMf)\n\n# Attention + Convolution transformer\nThis is an experimental architecture leveraging convolution blocks with attention blocks to model both the short and long range dynamics of the input tokens. The flow is the following: x -> convolution block -> attn -> FFN\n\n# Install\n``\n\n\n## Usage\n```python\nimport torch\nfrom attnconv.main import ATCTransformer\n\nmodel = ATCTransformer(\n    dim=512,\n    depth=6,\n    num_tokens=20000,\n    dim_head=64,\n    heads=8,\n    ff_mult=4,\n)\n\nx = torch.randint(0, 20000, (1, 512))\nlogits = model(x)  # (1, 1024, 20000)\nprint(logits)\n\n```\n\n\n# License\nMIT\n\n\n\n',
    'author': 'Kye Gomez',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/AttnWithConvolutions',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
