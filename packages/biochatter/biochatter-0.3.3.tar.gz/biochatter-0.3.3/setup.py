# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biochatter']

package_data = \
{'': ['*']}

install_requires = \
['langchain==0.0.339',
 'nltk>=3.8.1,<4.0.0',
 'openai>=1.1.0,<2.0.0',
 'pydantic==1.10.13',
 'pymilvus==2.2.8',
 'pymupdf>=1.22.3,<2.0.0',
 'redis>=4.5.5,<5.0.0',
 'retry>=0.9.2,<0.10.0',
 'stringcase>=1.2.0,<2.0.0',
 'tiktoken>=0.4.0,<0.5.0',
 'transformers>=4.30.2,<5.0.0']

extras_require = \
{'podcast': ['gTTS>=2.3.2,<3.0.0'],
 'streamlit': ['streamlit>=1.23.1,<2.0.0'],
 'xinference': ['botocore>=1.32.5,<2.0.0', 'xinference>=0.6.3,<0.7.0']}

setup_kwargs = {
    'name': 'biochatter',
    'version': '0.3.3',
    'description': 'Backend library for conversational AI in biomedicine',
    'long_description': '# BioChatter\n\n|     |     |     |     |\n| --- | --- | --- | --- |\n| __License__ | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) | __Python__ | [![Python](https://img.shields.io/pypi/pyversions/biochatter)](https://www.python.org) |\n| __Package__ | [![PyPI version](https://img.shields.io/pypi/v/biochatter)](https://pypi.org/project/biochatter/) [![Downloads](https://static.pepy.tech/badge/biochatter)](https://pepy.tech/project/biochatter) | __Build status__ | [![CI](https://github.com/biocypher/biochatter/actions/workflows/ci.yaml/badge.svg)](https://github.com/biocypher/biochatter/actions/workflows/ci.yaml) |\n| __Tests__ | Coverage coming soon. | __Docker__ | [![Latest image](https://img.shields.io/docker/v/biocypher/chatgse)](https://hub.docker.com/repository/docker/biocypher/chatgse/general) [![Image size](https://img.shields.io/docker/image-size/biocypher/chatgse/latest)](https://hub.docker.com/repository/docker/biocypher/chatgse/general) |\n| __Development__ | [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/) | __Contributions__ | [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](CONTRIBUTING.md) |\n\n## Description\n\nGenerative AI models have shown tremendous usefulness in increasing\naccessibility and automation of a wide range of tasks. Yet, their application to\nthe biomedical domain is still limited, in part due to the lack of a common\nframework for deploying, testing, and evaluating the diverse models and\nauxiliary technologies that are needed.  This repository contains the\n`biochatter` Python package, a generic backend library for the connection of\nbiomedical applications to conversational AI.  Described in [this\npreprint](https://arxiv.org/abs/2305.06488) and used in\n[ChatGSE](https://chat.biocypher.org), which is being developed at\nhttps://github.com/biocypher/ChatGSE. More to come, so stay tuned!\n\nBioChatter is part of the [BioCypher](https://github.com/biocypher) ecosystem, \nconnecting natively to BioCypher knowledge graphs. The BioChatter paper is\nbeing written [here](https://github.com/biocypher/biochatter-paper).\n\n## Installation\n\nTo use the package, install it from PyPI, for instance using pip (`pip install\nbiochatter`) or Poetry (`poetry add biochatter`).\n\n### Extras\n\nThe package has some optional dependencies that can be installed using the\nfollowing extras (e.g. `pip install biochatter[streamlit]`):\n\n- `streamlit`: support for streamlit UI functions (used in ChatGSE)\n\n- `podcast`: support for podcast text-to-speech (for the free Google TTS; the\npaid OpenAI TTS can be used without this extra)\n\n- `xinference`: support for querying open-source LLMs through Xorbits Inference\n\n## Usage\n\nAs an interim documentation until we have a proper one, check out the\n[Wiki](https://github.com/biocypher/biochatter/wiki) for some usage examples.\nMany common functionalities covered by BioChatter can be seen in use in the\n[ChatGSE](https://github.com/biocypher/ChatGSE) code base.\n\n# More information about LLMs\n\nCheck out [this repository](https://github.com/csbl-br/awesome-compbio-chatgpt)\nfor more info on computational biology usage of large language models.\n\n# Dev Container\n\nDue to some incompatibilities of `pymilvus` with Apple Silicon, we have created\na dev container for this project. To use it, you need to have Docker installed\non your machine. Then, you can run the devcontainer setup as recommended by\nVSCode\n[here](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-an-existing-folder-in-a-container)\nor using Docker directly.\n\nThe dev container expects an environment file (there are options, but the basic\none is `.devcontainer/local.env`) with the following variables:\n\n```\nOPENAI_API_KEY=(sk-...)\nDOCKER_COMPOSE=true\nDEVCONTAINER=true\n```\n\nTo test vector database functionality, you also need to start a Milvus\nstandalone server. You can do this by running `docker-compose up` as described\n[here](https://milvus.io/docs/install_standalone-docker.md) on the host machine\n(not from inside the devcontainer).\n',
    'author': 'Sebastian Lobentanzer',
    'author_email': 'sebastian.lobentanzer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
