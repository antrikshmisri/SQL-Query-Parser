"""Utility functions/classes for sqlparser."""

from re import compile as regex_compile
from re import error
from re import match as regex_match

from sqlparser.tokens import __TOKEN_TYPES__ as token_type_dict
from sqlparser.tokens import (Aggregate, Identifier, Keyword, Number, Operator,
                              Separator, String, Token, Whitespace)


def get_token_class(token_name):
    """Get the resperctive token class from a token name.
    
    Parameters
    ----------
    token_name: str
        Name of the token, SELECT, WHERE, etc.
    
    Returns
    -------
    token_class: :class: `tokens.Token`
        The respective token object.
    """
    token_class_dict = {
        'keyword': Keyword,
        'operator': Operator,
        'separator': Separator,
        'identifier': Identifier,
        'number': Number,
        'string': String,
        'whitespace': Whitespace,
        'aggregate': Aggregate,
    }

    for item in token_type_dict.items():
        _name = item[0]
        _values = item[1]

        if len(_values) == 1:
            try:
                regex_compile(_values[0])
                is_valid_pattern = True
            except error:
                is_valid_pattern = False

            if is_valid_pattern:
                if regex_match(_values[0], token_name):
                    return token_class_dict[_name]

        for value in _values:
            if value == token_name:
                return token_class_dict[_name]

    raise ValueError(f"Invalid token name: {token_name}")


def raise_error_from_dict(error_dict):
    """Raise error from an error dict.
    
    Parameters
    ----------
    error_dict: dict
        Error dict.
    """
    raise error_dict['error_type'](
        f"Error at index {error_dict['index']}, {error_dict['error_message']}")


def get_error_dict(error_type, message, error_index):
    """Get an error dict for a specific error type.
    
    Parameters
    ----------
    error_type: :class: `Exception`
        Type of error
    message: str
        Error message
    error_index: int
        Index of the error
    
    Returns
    -------
    error_dict: dict
        Error dict.
    """
    return {
        'error_type': error_type,
        'error_message': message,
        'index': error_index
    }


def print_process_heading(context_text):
    """Print a process heading.
    
    Parameters
    ----------
    context_text: str
        Context text.
    """
    print('-' * len(context_text))
    print(context_text.upper())
    print('-' * len(context_text))


def token_name2type_dict():
    """Get the dictionary containing token names and their types.
    
    Returns
    -------
    dict containing token names and their types.
    """
    token_name2type = {}
    type2obj = {
        'keyword': Keyword,
        'aggregate': Aggregate,
        'operator': Operator,
        'separator': Separator,
        'number': Number,
        'string': String,
        'whitespace': Whitespace,
        'identifier': Identifier,
    }

    for item in token_type_dict.items():
        _type = item[0]
        _names = item[1]

        for name in _names:
            token_name2type[name] = type2obj[_type]

    return token_name2type


def merge_consequtive_keywords(query):
    """Merge consequtive keywords that when merged form a valid keyword.
    
    Parameters
    ----------
    query: :class: `Query`
        Query that is to be processed
    """

    for idx, token in enumerate(query.tokens):
        current_token = token
        next_token = query.tokens[idx +
                                  1] if idx < len(query.tokens) - 1 else None

        try:
            merged_value = current_token.value + " " + \
                next_token.value if next_token else ""
        except AttributeError:
            continue

        if merged_value in token_type_dict['keyword']:
            query.tokens[idx] = Keyword(merged_value, validate=False)
            query.tokens.remove(next_token)

    return query


def print_query_dict(query_dict):
    for key, value in query_dict.items():
        if key == 'FROM' and isinstance(value[0], dict):
            print(f"{key}: Query(", end="")
            print_query_dict(value[0])
        else:
            print(
                f'{key}: {[val.value if isinstance(val, Token) else val for val in value]}', end=" ")


def get_flat_query(query):
    """Create a flat query from a nested query object.
    
    Parameters
    ----------
    query: :class: `query.Query`
        The query that is to be processed
    
    Returns
    -------
    list of tokens
    """
    flat_query = []

    for token in query.tokens:
        if not isinstance(token, Token):
            flat_query.extend(get_flat_query(token))
        else:
            flat_query.append(token)

    return flat_query
