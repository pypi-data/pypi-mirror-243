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
{'console_scripts': ['gptsql = gptsql.main:main']}

setup_kwargs = {
    'name': 'gptsql',
    'version': '0.1.0',
    'description': 'LLM helper for psql',
    'long_description': '# gptsql\n\nAn LLM wrapper around your database connection. Think of it as a "smart" version of the psql cli.\n\nExample:\n\n```\n    python -m gptsql\n    > show me the schemas\n    thinking...\n    Running select query: SELECT schema_name FROM information_schema.schemata;\n    processing the function response...\n    Here are the schemas in your database:\n\n    1. pg_catalog\n    2. information_schema\n    3. analytics\n    4. public\n    5. aws_commons\n    6. bi_staging\n    7. rds_tools\n\n    > show me tables that start with "streaming_"\n    thinking...\n    Running select query: SELECT table_name FROM information_schema.tables WHERE table_name LIKE \'streaming_%%\';\n    processing the function response...\n    Here are the tables that start with "streaming_":\n\n    1. streaming_bookings\n    2. streaming_campaign_vast_tags\n    3. streaming_campaigns\n    4. streaming_cpx_predictions\n    5. streaming_hourly_counts\n    6. streaming_hourly_lift\n    7. streaming_hourly_lift_dbx\n    8. streaming_hourly_lift_dbx_staging\n    9. streaming_impressions_log_entries\n    10. streaming_impressions_logs\n    11. streaming_network_extreme_reach_inventory_id_map\n    12. streaming_networks\n    13. streaming_provider_company_map\n    14. streaming_providers\n    15. streaming_reconciliations\n    16. streaming_spends\n    17. streaming_spends_dbx\n    18. streaming_spends_dbx_staging    \n```\n\n## Getting started\n\nSetup your `.env` file from `env.example`. Then source the values into your environment.\n\nRun the CLI with:\n\n    python -m gptsql\n    ',
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
