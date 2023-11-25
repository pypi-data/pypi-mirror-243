# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minerva']

package_data = \
{'': ['*']}

install_requires = \
['accelerate', 'torch', 'transformers', 'zetascale']

setup_kwargs = {
    'name': 'minerva-torch',
    'version': '0.0.1',
    'description': 'Transformers at zeta scales',
    'long_description': '# Minerva: Unleashing the Secrets of advanced Mathematics 🏛️🔢\n\n<!-- ![Minerva Next Generation Open Source Language Model](/Minerva-banner.png) -->\nMinerva is a groundbreaking language model that pushes the boundaries of mathematical understanding and problem-solving. Designed with an advanced math theme, Minerva embodies the spirit of renowned mathematicians such as Euclid, Pythagoras, and Archimedes. By harnessing their advanced wisdom, Minerva offers unparalleled capabilities in mathematical reasoning and exploration.\n\n---\n\n<div align="center">\n\n[![GitHub issues](https://img.shields.io/github/issues/kyegomez/Minerva)](https://github.com/kyegomez/Minerva/issues) [![GitHub forks](https://img.shields.io/github/forks/kyegomez/Minerva)](https://github.com/kyegomez/Minerva/network) [![GitHub stars](https://img.shields.io/github/stars/kyegomez/Minerva)](https://github.com/kyegomez/Minerva/stargazers) [![GitHub license](https://img.shields.io/github/license/kyegomez/Minerva)](https://github.com/kyegomez/Minerva/blob/main/LICENSE)\n\n</div>\n\n<div align="center">\n\n[![Share on Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Share%20%40kyegomez/Minerva)](https://twitter.com/intent/tweet?text=Unleash%20the%20power%20of%20Minerva%20-%20the%20advanced-themed%20MATH%20LLM%20from%20Google!&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FMinerva) [![Share on Facebook](https://img.shields.io/badge/Share-%20facebook-blue)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FMinerva) [![Share on LinkedIn](https://img.shields.io/badge/Share-%20linkedin-blue)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FMinerva&title=&summary=&source=)\n\n[![Share on Reddit](https://img.shields.io/badge/-Share%20on%20Reddit-orange)](https://www.reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FMinerva&title=Unleash%20the%20power%20of%20Minerva%20-%20the%20advanced-themed%20MATH%20LLM%20from%20Google!) [![Share on Hacker News](https://img.shields.io/badge/-Share%20on%20Hacker%20News-orange)](https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fgithub.com%2Fkyegomez%2FMinerva&t=Unleash%20the%20power%20of%20Minerva%20-%20the%20advanced-themed%20MATH%20LLM%20from%20Google!) [![Share on Pinterest](https://img.shields.io/badge/-Share%20on%20Pinterest-red)](https://pinterest.com/pin/create/button/?url=https%3A%2F%2Fgithub.com%2Fkyegomez%2FMinerva&media=https%3A%2F%2Fexample.com%2Fimage.jpg&description=Unleash%20the%20power%20of%20Minerva%20-%20the%20advanced-themed%20MATH%20LLM%20from%20Google!) [![Share on WhatsApp](https://img.shields.io/badge/-Share%20on%20WhatsApp-green)](https://api.whatsapp.com/send?text=Unleash%20the%20power%20of%20Minerva%20-%20the%20advanced-themed%20MATH%20LLM%20from%20Google!%20%23Minerva%20%23AI%0A%0Ahttps%3A%2F%2Fgithub.com%2Fkyegomez%2FMinerva)\n\n</div>\n\n---\n\n\n\n\n\n# Install\n\n```shell\npip install minerva\n```\n\n\n# Usage\n```python\nimport torch\nfrom minerva import Minerva, Train\n\n# Example usage\nx = torch.randint(0, 20000, (1, 1024))\n\nMinerva(x)\n\n# or train\nTrain()\n```\n\n# Training\n\nTo train Minerva, follow these steps:\n\n1. Configure the training settings by setting the environment variables:\n\n   - `ENTITY_NAME`: Your wandb project name\n   - `OUTPUT_DIR`: Specify the output directory for saving the weights (e.g., `./weights`)\n\n2. Launch the training process using Deepspeed:\n\n```shell\nAccelerate Config\nAccelerate launch train_distributed_accelerate.py\n```\n\n## Dataset Building\n\nTo build a custom dataset for Minerva, you can preprocess the data using the `build_dataset.py` script. This script performs tasks such as pre-tokenization, data chunking, and uploading to the Huggingface hub. Here\'s an example command:\n\n| Dataset | Description |\n|-|-|  \n| Mathematical Web Pages | Web pages containing mathematical expressions in MathJax format, cleaned to preserve math notation|\n| arXiv | 2 million arXiv papers up to Feb 2021, in LaTeX format |\n| General Natural Language Data | Same dataset used to pretrain PaLM models |\n\nThe mathematical web pages and arXiv datasets focus on technical and mathematical content. The general natural language data provides a broad coverage of general language.\n\nThe paper states the mathematical web pages and arXiv each account for 47.5% of the total data. The remaining 5% is general natural language data which is a subset of what was used for PaLM pretraining.\n\n## Roadmap 🗺️📍\n\n- [ ] Create a dataset of ARXVIV papers',
    'author': 'Zeta Team',
    'author_email': 'kye@apac.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kyegomez/Minerva',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
