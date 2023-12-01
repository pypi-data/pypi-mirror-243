# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dbt2looker_bigquery']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5',
 'importlib-metadata>=4',
 'lkml>=1.1',
 'pydantic>=1.8',
 'typing-extensions>=4.0']

entry_points = \
{'console_scripts': ['dbt2looker = dbt2looker_bigquery.cli:run']}

setup_kwargs = {
    'name': 'dbt2looker-bigquery',
    'version': '0.12.0b8',
    'description': 'Generate lookml view files from dbt models for Bigquery',
    'long_description': '# dbt2looker\nUse `dbt2looker-bigquery` to generate Looker view files automatically from dbt models in Bigquery.\n\nThis is a fork of dbt2looker that is specific to bigquery.\nThe intention is to allow one to define most of the simple and tedious lookml settings in dbt.\nThat way the lookml code gets less bloated, and can be more focused on advanced metrics and explores.\n\nWant a deeper integration between dbt and your BI tool?\nYou should also checkout [Lightdash - the open source alternative to Looker](https://github.com/lightdash/lightdash)\n\n**Features**\n\n* **Column descriptions** synced to looker\n* **Dimension** for each column in dbt model\n* **Define Dimensions** define common lookml settings in dbt like label, group label, hidden\n* **Opinionated Primary key** automatically set the first column to be the primary key, and hide it.\n* **Dimension groups** for datetime/timestamp/date columns\n* **Measures** defined through dbt column `metadata` [see below](#defining-measures)\n* Looker types\n* Warehouses: BigQuery\n\n## Quickstart\n\nRun `dbt2looker` in the root of your dbt project *after compiling looker docs*.\n\n**Generate Looker view files for all models:**\n```shell\ndbt docs generate\ndbt2looker\n```\n\n**Generate Looker view files for all models tagged `prod`**\n```shell\ndbt2looker --tag prod\n```\n\n## Install\n\n**Install from PyPi repository**\n\nInstall from pypi into a fresh virtual environment.\n\n```\n# Create virtual env\npython3.7 -m venv dbt2looker-venv\nsource dbt2looker-venv/bin/activate\n\n# Install\npip install dbt2looker-bigquery\n\n# Run\ndbt2looker\n```\n\n**Build from source**\n\nRequires [poetry](https://python-poetry.org/docs/) and python >=3.7\n\nFor development, it is recommended to use python 3.7:\n\n```\n# Ensure you\'re using 3.7\npoetry env use 3.7  \n# alternative: poetry env use /usr/local/opt/python@3.7/bin/python3\n\n# Install dependencies and main package\npoetry install\n\n# Run dbtlooker in poetry environment\npoetry run dbt2looker\n```\n\n## Defining measures\n\nYou can define looker measures in your dbt `schema.yml` files. For example:\n\n```yaml\nmodels:\n  - name: pages\n    columns:\n      - name: url\n        description: "Page url"\n      - name: event_id\n        description: unique event id for page view\n        meta:\n            looker_measures:\n              type: count_distinct\n              type: count\n\n```\n',
    'author': 'gisle r',
    'author_email': 'grognu@protonmail.com',
    'url': 'https://github.com/hubble-data/dbt2looker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
