# gptsql

An LLM wrapper around your database connection. Think of it as a "smart" version of the psql cli.

Example:

```
    python -m gptsql
    > show me the schemas
    thinking...
    Running select query: SELECT schema_name FROM information_schema.schemata;
    processing the function response...
    Here are the schemas in your database:

    1. pg_catalog
    2. information_schema
    3. analytics
    4. public
    5. aws_commons
    6. bi_staging
    7. rds_tools

    > show me all the tables with 'sales' in the name
    ⠸ thinking...  Running select query: SELECT table_name FROM information_schema.tables WHERE table_name LIKE '%%sales%%' ORDER BY table_name;
    [assistant] --> The tables with 'sales' in the name are as follows:

    - salesorderdetail
    - salesorderheader
    - salesorderheadersalesreason
    - salesperson
    - salespersonquotahistory
    - salesreason
    - salestaxrate
    - salesterritory
    - salesterritoryhistory
    - vsalesperson
    - vsalespersonsalesbyfiscalyears
    - vsalespersonsalesbyfiscalyearsdata

    > how many rows are in the salesperson table?
    ⠏ thinking...  Running select query: SELECT COUNT(*) FROM sales.salesperson;
    [assistant] --> The `salesperson` table contains 17 rows.
```

## Getting started

You need credentials for your database, and you will need an OpenAI **API Key** from your OpenAI account.

Installation:

    pip install gptsql

or download the source. 

Run the CLI with:

    gptsql

or use `python -m gptsql` to run from source.
