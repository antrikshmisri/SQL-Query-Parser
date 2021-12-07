import numpy.testing as npt
from sqlparser.filters import (FilterStack, QueryFilter, process_case,
                               process_separator)
from sqlparser.query import Query


def test_process_case():
    query = "SELECT * FROM table WHERE col = 'value' OR col = 'value2'"

    processed_query = process_case(query)

    for token in processed_query.split(" "):
        if token.isalnum():
            npt.assert_equal(token.isupper(), True)


def test_process_separator():
    query = "SELECT height FROM ( SELECT id, height FROM person ) WHERE height>100"
    separators = ['(', ')']
    processed_query = process_separator(query)

    for char in processed_query:
        npt.assert_equal(char in separators, False)


def test_filter_stack():
    base_filter_stack = FilterStack(filters=[process_case, process_separator])
    query = base_filter_stack(
        "SELECT * FROM table WHERE col = 'value' OR col = 'value2'")

    for token in query.split(" "):
        if token.isalnum():
            npt.assert_equal(token.isupper(), True)

    for char in query:
        npt.assert_equal(char in ['(', ')'], False)

    def invalid_filter(query):
        return query

    with npt.assert_raises(ValueError):
        base_filter_stack.add(invalid_filter)

    base_filter_stack.remove(process_case)
    npt.assert_equal(base_filter_stack.filters, [process_separator])


def test_query_filter():
    query = Query("SELECT SUM(height) as total_height FROM person")
    query_filter = QueryFilter()

    processed_query = query_filter(query)

    npt.assert_equal(
        'as' not in [token.value for token in processed_query.tokens], True)
    npt.assert_equal('total_height' not in [
                     token.value for token in processed_query.tokens], True)
