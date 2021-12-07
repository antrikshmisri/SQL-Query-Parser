"""Perform validations on the SQL queries"""
import inspect
import sys

from sqlparser.constants import __TOKEN_PRECEDENCE__ as token_precedence_dict
from sqlparser.exceptions import InvalidQueryError
from sqlparser.utils import (get_error_dict, get_flat_query,
                             raise_error_from_dict)


def base_query_validation(query):
    """Basic query validtion.

    Parameters
    ----------
    query: :class: `query.Query`
        The query object that is to be validated

    Returns
    -------
    validation_result: bool or dict
        True if the query is valid or a dict that contains error type, error message and index.
    """
    is_valid = True
    keywords = ['SELECT', 'DELETE', 'UPDATE', 'ALTER', 'CREATE',
                'DROP', 'INSERT', 'GRANT', 'REVOKE', 'TRUNCATE', 'ROLLBACK']

    if query.tokens[0].value not in keywords:
        is_valid = False
        error_dict = get_error_dict(
            InvalidQueryError,
            'Invalid query. Query should begin with a keyword like, SELECT, INSERT, etc.',
            0)

    return is_valid or raise_error_from_dict(error_dict)


def validate_token_order(query):
    """Validate if the order of the tokens are correct.

    Parameters
    ----------
    query: :class: `query.Query`
        The query that is to be validated.

    Returns
    -------
    validation_result: bool or dict
        True if the query is valid or a dict that contains error type, error message and index.
    """
    is_valid = True
    tokens = get_flat_query(query)

    for token_idx, token in enumerate(tokens):
        current_token_class = token.__class__
        valid_next_tokens = token_precedence_dict[current_token_class]['valid']
        invalid_next_token_values = token_precedence_dict[current_token_class]['invalid']

        next_token = tokens[token_idx +
                            1] if token_idx < len(tokens) - 1 else None

        if next_token is not None:
            validations = [next_token.__class__ in valid_next_tokens,
                           next_token.value not in invalid_next_token_values,
                           next_token.value != token.value]

            if all(validations):
                continue
            else:
                is_valid = False
                error_dict = get_error_dict(
                    InvalidQueryError,
                    f'Invalid token order, {token.value} cannot precede {next_token.value}.',
                    token_idx + 1)

    return is_valid or raise_error_from_dict(error_dict)


__all_validators__ = [obj for _, obj in inspect.getmembers(sys.modules[__name__])
                      if (inspect.isfunction(obj) and __name__ == obj.__module__)]
