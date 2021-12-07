"""Various filters for sqlparser package"""
from types import MethodType

from sqlparser.tokens import __TOKEN_TYPES__ as token_types_dict
from sqlparser.tokens import Identifier


def process_separator(query):
    """Process separator in a SQL query.
    
    Parameters
    ----------
    query: str
        SQL query to be processed
    
    Returns
    -------
    process_query: str
        Processed query
    """
    separator = token_types_dict['separator']

    for separator in separator:
        query = query.replace(separator, ' ')

    return query


def process_case(query):
    """Process character case in SQL query
    
    Parameters
    ----------
    query: str
        SQL query to be processed
    
    Returns
    -------
    process_query: str
        Processed query
    """
    for string_token in query.split(' '):
        query = query.replace(string_token, string_token.upper())

    return query


class FilterStack:
    """Filter stack to reduce SQL query to minimal tokens."""

    def __init__(self, filters=None):
        """Initialize the filter stack.
        
        Parameters
        ----------
        filters: list
            List of filters to be applied to the SQL query.
        """
        self.filters = filters or []

        # Get all the member filter function in this class.
        if not self.filters:
            self._get_member_functions()

    def __call__(self, query):
        """Apply filters to the SQL query.
        
        Parameters
        ----------
        query: str
            SQL query to be processed
        
        Returns
        -------
        process_query: str
            Processed query
        """
        for filter in self.filters:
            query = filter(query)

        return query

    def add(self, filter):
        """Add a filter to the filter stack.
        
        Parameters
        ----------
        filter: function
            Filter to be added to the filter stack.
        """
        if not filter.__name__.startswith('filter'):
            raise ValueError('Filter must be a function.')

        self.filters.append(filter)

    def remove(self, filter):
        """Remove a filter from the filter stack.
        
        Parameters
        ----------
        filter: function
            Filter to be removed from the filter stack.
        """
        self.filters.remove(filter)

    def _get_member_functions(self):
        """Get all the member filter function in this class."""
        for name in dir(self):
            if name.startswith('filter') and isinstance(getattr(self, name), MethodType):
                self.add(getattr(self, name))


class QueryFilter(FilterStack):
    """Filter class to filter out tokens that are not part of the query."""

    def __init__(self):
        """Initialize the `QueryFilter` class."""
        super(QueryFilter, self).__init__()

    def filter_as_keyword(self, query):
        """Filter to remove all the `AS` tokens and tokens that succeed the token."""

        for token in query.tokens:
            if isinstance(token, Identifier) and token.value.lower() == 'as':
                idx = query.tokens.index(token)
                query.tokens = query.tokens[:idx] + query.tokens[idx + 2:]
        return query
