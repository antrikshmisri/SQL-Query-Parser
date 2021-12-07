"""Module to provide functionalities around queries"""

from collections import deque

from sqlparser.exceptions import QueryParseError
from sqlparser.filters import QueryFilter
from sqlparser.tokens import __TOKEN_TYPES__ as token_type_dict
from sqlparser.tokens import Identifier, Keyword
from sqlparser.utils import get_token_class, merge_consequtive_keywords


class Query:
    """Class to represent a SQL query as atomic token objects."""

    def __init__(self, query=None, tokens=None):
        """Initialize the `Query` class.

        Parameters
        ----------
        query: str
            SQL query to be parsed.
        """
        self.query = query or ""
        self.tokens = tokens or list()

        if not self.tokens:
            # Deconstruct the query to get individual tokens.
            self._get_tokens_from_query()

        self.subquery = self.process_subqueries()  # Process subqueries.
        merge_consequtive_keywords(self)

    def __iter__(self):
        """Iterate over the tokens in the query."""
        return iter(self.tokens)

    def __getitem__(self, index):
        """Return the token at the given index."""
        return self.tokens[index]

    def __str__(self):
        """Return the query as a string."""
        return " ".join([str(token) for token in self.tokens])

    def _get_tokens_from_query(self):
        """Deconstruct the query to get individual tokens."""
        _string_tokens = self.query.split(" ")

        for string_token in _string_tokens:
            if string_token == "":
                continue
            token_class = get_token_class(string_token)
            self.tokens.append(token_class(string_token))

    def process_subqueries(self):
        """Return the subqueries of the query."""
        begin_token_values = ['SELECT', 'DELETE', 'UPDATE',
                              'INSERT', 'CREATE', 'DROP', 'ALTER', 'TRUNCATE']
        seperators = ['(', ')']
        subquery = None

        for idx, token in enumerate(self.tokens):
            current_token = token.value
            next_token = self.tokens[idx +
                                     1].value if idx < len(self.tokens) - 1 else None

            subquery_conditions = [current_token == seperators[0],
                                   next_token in begin_token_values, ]

            if all(subquery_conditions):
                subquery_start_idx, subquery_end_idx = self._get_subquery(idx)

                if subquery_end_idx == -1:
                    raise QueryParseError(
                        f"Unbalanced subquery at index {subquery_start_idx}"
                        f", {[token.value for token in self.tokens[subquery_start_idx:]]}")

                subquery = Query(
                    tokens=self.tokens[subquery_start_idx + 1:subquery_end_idx])

                for subquery_token in self.tokens[subquery_start_idx:subquery_end_idx + 1]:
                    self.tokens.remove(subquery_token)

                self.tokens.insert(subquery_start_idx, subquery)

        if not subquery:
            return self.tokens

    def _get_subquery(self, start_idx):
        """Get the index range of a subquery

        Parameters
        ----------
        start_idx: int
            Start index of the subquery

        Returns
        -------
        tuple
            Tuple containing the start and end index of the subquery.
        """
        token_deque = deque()

        for i in range(start_idx, len(self.tokens)):
            if self.tokens[i].value == ')':
                token_deque.popleft()

            elif self.tokens[i].value == '(':
                token_deque.append(self.tokens[i])

            if not token_deque:
                return start_idx, i

        return (start_idx, -1)


def create_query_dict(query):
    """Create a dictionary from a query.

    Paramters
    ---------
    query: Query
        Query that is to be converted

    Returns
    -------
    dict
    """
    query_dict = {}
    for token in query.tokens:
        if isinstance(token, Keyword):
            query_dict[token.value] = []

    query_filter = QueryFilter()
    query = query_filter(query)

    for token in query.tokens:
        if isinstance(token, Keyword):
            for token_pair in query.tokens[query.tokens.index(token) + 1:]:
                if isinstance(token_pair, Keyword):
                    break

                if isinstance(token_pair, Query):
                    token_pair = create_query_dict(token_pair)

                if isinstance(token_pair, Identifier):
                    separated_tokens = token_pair.value.split("(")
                    if separated_tokens[0] in token_type_dict["aggregate"]:
                        token_pair = {
                            separated_tokens[0]: separated_tokens[1][:-1]}

                query_dict[token.value].append(token_pair)

    return query_dict
