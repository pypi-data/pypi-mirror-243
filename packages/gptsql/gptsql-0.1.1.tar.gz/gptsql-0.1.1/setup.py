# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gptsql']

package_data = \
{'': ['*']}

install_requires = \
['halo>=0.0.31,<0.0.32',
 'openai>=1.3.6,<2.0.0',
 'pandas>=2.1.3,<3.0.0',
 'prompt-toolkit>=3.0.41,<4.0.0',
 'psycopg2>=2.9.9,<3.0.0',
 'sqlalchemy>=2.0.23,<3.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'termcolor>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['gptsql = gptsql.__main__:main']}

setup_kwargs = {
    'name': 'gptsql',
    'version': '0.1.1',
    'description': 'LLM helper for psql',
    'long_description': '# gptsql\n\nAn LLM wrapper around your database connection. Think of it as a "smart" version of the psql cli.\n\nExample:\n\n```\n    python -m gptsql\n    > show me the schemas\n    thinking...\n    Running select query: SELECT schema_name FROM information_schema.schemata;\n    processing the function response...\n    Here are the schemas in your database:\n\n    1. pg_catalog\n    2. information_schema\n    3. analytics\n    4. public\n    5. aws_commons\n    6. bi_staging\n    7. rds_tools\n\n    > show me all the tables with \'sales\' in the name\n    ⠸ thinking...  Running select query: SELECT table_name FROM information_schema.tables WHERE table_name LIKE \'%%sales%%\' ORDER BY table_name;\n    [assistant] --> The tables with \'sales\' in the name are as follows:\n\n    - salesorderdetail\n    - salesorderheader\n    - salesorderheadersalesreason\n    - salesperson\n    - salespersonquotahistory\n    - salesreason\n    - salestaxrate\n    - salesterritory\n    - salesterritoryhistory\n    - vsalesperson\n    - vsalespersonsalesbyfiscalyears\n    - vsalespersonsalesbyfiscalyearsdata\n\n    > how many rows are in the salesperson table?\n    ⠏ thinking...  Running select query: SELECT COUNT(*) FROM sales.salesperson;\n    [assistant] --> The `salesperson` table contains 17 rows.\n```\n\n## Getting started\n\nYou need credentials for your database, and you will need an OpenAI **API Key** from your OpenAI account.\n\nInstallation:\n\n    pip install gptsql\n\nor download the source. \n\nRun the CLI with:\n\n    gptsql\n\nor use `python -m gptsql` to run from source.\n',
    'author': 'Scott Persinger',
    'author_email': 'scottpersinger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
