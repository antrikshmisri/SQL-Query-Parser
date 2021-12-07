"""
===================
Subquery Processing
===================

This example shows subquery processing that sqlparse performs.

First, some imports.
"""
from sqlparser.query import Query, create_query_dict
from sqlparser.tokens import Identifier
from sqlparser.validators import base_query_validation

PRINT_RAW_RESULT = False


q = Query("SELECT SUM(height) as total_height, AVG(height) as average_height FROM ( SELECT id, height FROM person GROUP BY id, height ) WHERE height>100")
base_query_validation(q)

q_dict = create_query_dict(q)


def print_query_dict(query_dict, depth=0):
    for key, value in query_dict.items():
        if key == 'FROM' and isinstance(value[0], dict):
            print(f"{key}: Query(", end="")
            print_query_dict(value[0], depth + 1)
        else:
            print(
                f'{key}: {[val.value if isinstance(val, Identifier) else val for val in value]}', end=" ")


if not PRINT_RAW_RESULT:
    print_query_dict(q_dict)
else:
    print(q_dict)
