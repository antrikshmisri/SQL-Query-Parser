# SQL-Query-Parser

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d61821777bff4e6a9aa09bfdd1945d6a)](https://app.codacy.com/gh/antrikshmisri/SQL-Query-Parser?utm_source=github.com&utm_medium=referral&utm_content=antrikshmisri/SQL-Query-Parser&utm_campaign=Badge_Grade_Settings)

Query parser for SQL.

The parser's architecture is loosely based on the open source [sqlparse](https://github.com/andialbrecht/sqlparse) with some additions and complete rewrites. Below is a brief overview of how this parser works:

## Working

The basic building blocks for `sqlparser` are `Tokens` and `Query`. These classes represent `tokens` in a `query` and the `query` itself in an object format. Each query has a list of tokens present in it which may include subqueries. These tokens are validated before adding them to the query these validations may include token order checks/token validity etc (This is an optional step and can be enabled with `-vq` flag).

This package does some processing and filtering before generating the `query_dict`. These procesing/filtering operations make sure that every unwanted token gets removed from the final query object. The processing helps in shaping the string query so that there has to be minimal processing while generating the query object from the string. The filtering helps in removing/adding/updating certain tokens/token pairs in the query object so that the query can be processed to form a `dict`

## Using the CLI

The package provides a command line interface that can be used to interact with the package itself. Below is the list of commands/flags.

**Generating the query dict without validations**
```bash
sqlparser -q "SELECT SUM(height) as total_height, AVG(height) as average_height FROM ( SELECT id, height FROM person GROUP BY id, height ) WHERE height>100"
```

**Generating the query dict with validations**
```bash
sqlparser -q "SELECT SUM(height) as total_height, AVG(height) as average_height FROM ( SELECT id, height FROM person GROUP BY id, height ) WHERE height>100" -vq"
```

**Displaying the raw query dict**
```bash
sqlparser -q "SELECT SUM(height) as total_height, AVG(height) as average_height FROM ( SELECT id, height FROM person GROUP BY id, height ) WHERE height>100" -vq -r
```

## Using `sqlparser` in development environment

1. Get the source code by cloning from remote repository.
```bash
git clone https://github.com/antrikshmisri/SQL-Query-Parser.git
```

2. Create and activate a virtual environment.
```bash
python -m venv venv
source venv/bin/activate
```

3. Get the dependencies
```bash
pip install -r requirements.txt
```

4. Install as a local project
```bash
pip install .
```

5. Run the tests ***(Tests for some module are yet to be added)***
```bash
pytest -v sqlparser/tests/
```

### Requirements

Below is the list of requirements
* `numpy`
* `pytest`
