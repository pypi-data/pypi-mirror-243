LocalStack Snowflake Extension
=============================================

This LocalStack extension provides basic emulation of the [Snowflake](https://snowflake.com) API.

⚠️ Please note that this extension is experimental and still under development.

## Prerequisites

- LocalStack Pro
- Docker
- Python

## Installation

Before installing the extension, make sure you're logged into LocalStack. If not, log in using the following command:

```bash
localstack login
```

You can then install this extension using the following command:

```bash
localstack extensions install localstack-extension-snowflake
```

## Usage

Once the extension is installed, configure your Snowflake client connector to point to the API endpoint `https://snowflake.localhost.localstack.cloud`. For example, when using the [Snowflake Python connector](https://github.com/snowflakedb/snowflake-connector-python):
```
client = snowflake.connector.connect(
    user="test",
    password="test",
    account="test",
    host="snowflake.localhost.localstack.cloud",
)
client.cursor().execute("...")
```

## Change Log

* `0.1.3`: Add DBEngine abstraction, experimental support for duckdb; enhance support for JSON queries
* `0.1.2`: Add logic to ingest a CSV file from a Snowflake stage into a table
* `0.1.1`: Initial support for Kafka connector and snowpipe/streaming APIs
* `0.1.0`: Initial release of the extension

## License

(c) 2023 LocalStack
