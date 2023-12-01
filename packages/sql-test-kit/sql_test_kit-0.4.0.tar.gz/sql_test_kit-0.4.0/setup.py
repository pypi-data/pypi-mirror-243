# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_test_kit']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.0']

setup_kwargs = {
    'name': 'sql-test-kit',
    'version': '0.4.0',
    'description': 'Framework for testing SQL queries',
    'long_description': '# sql-test-kit\n\nThis is a framework for testing SQL queries.\nIt works by directly running the queries against the targeted engine, thus being robust to any change in the\ncorresponding SQL dialect.\nMoreover, it is currently focused on interpolating test data directly inside the SQL queries, making the test much\nquicker than if it was creating actual tables.\n\n# Installation\n\nThis package is available on Pypi, so you can use your favorite dependency managment tool to install it. For example :\n* with pip : \n```shell\npip install sql-test-kit\n```\n* with poetry : \n```shell\npoetry add sql-test-kit\n```\n\n# Usage example\n\n`sql-test-kit` is currently available for most SQL engines (Postgres, Redshift, Snowflakes...), and is particularly useful\nfor those where no framework exists for locally testing SQL queries.\n\nNevertheless, a specific implementation has been written for BigQuery, in order to facilitate Table object initialization,\nas well as null values interpolation in tests.\n\nHere is a simple example of instantiating a Table object and a SQL query for BigQuery :\n```python\nfrom sql_test_kit import BigqueryTable, Column\n\n\nsales_amount_col = "SALES_AMOUNT"\nsales_date_col = "SALES_DATE"\nsales_table = BigqueryTable(\n    project="project",\n    dataset="dataset",\n    table="table",\n    columns=[\n        Column(sales_amount_col, "FLOAT64"),\n        Column(sales_date_col, "STRING"),\n    ],\n)\ncurrent_year_sales_by_day_query = f"""\n    SELECT {sales_date_col}, SUM({sales_amount_col}) AS {sales_amount_col}\n    FROM {sales_table}\n    WHERE {sales_date_col} >= "2023-01-01"\n    GROUP BY {sales_date_col}\n    """\n```\n\nYou can then test it this way :\n```python\nimport pandas as pd\nfrom google.cloud.bigquery import Client\n\nfrom sql_test_kit import QueryInterpolator\n\n\ndef test_current_year_sales_by_day_query():\n    # Given\n    sales_data = pd.DataFrame(\n        {\n            "SALES_ID": [1, 2, 3, 4],\n            sales_date_col: ["2022-12-31", "2023-01-01", "2023-01-01", "2023-01-02"],\n            sales_amount_col: [10, 20, 30, 40],\n        }\n    )\n\n    # When\n    interpolated_query = QueryInterpolator() \\\n        .add_input_table(sales_table, sales_data) \\\n        .interpolate_query(current_year_sales_by_day_query)\n    current_year_sales_by_day_data = Client().query(interpolated_query).to_dataframe()\n\n    # Then\n    expected_current_year_sales_by_day_data = pd.DataFrame(\n        {\n            sales_date_col: ["2023-01-01", "2023-01-02"],\n            sales_amount_col: [50, 40],\n        }\n    )\n\n    pd.testing.assert_frame_equal(\n        current_year_sales_by_day_data,\n        expected_current_year_sales_by_day_data,\n        check_dtype=False,\n    )\n```\n',
    'author': 'victorlandeau',
    'author_email': 'vlandeau@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
