
from sqlparser.tokens import Aggregate, Identifier, Keyword, Operator

__TOKEN_PRECEDENCE__ = {
    Keyword: {'valid': [Aggregate, Identifier, Operator, Keyword],
              'invalid': ['WHERE', 'AND', 'OR', 'NOT', 'LIKE', 'IN', 'INSERT', 'UPDATE', 'DELETE']},

    Aggregate: {'valid': [Keyword, Aggregate, Identifier, Operator],
                'invalid': ['INSERT', 'UPDATE', 'DELETE']},

    Identifier: {'valid': [Keyword, Aggregate, Identifier, Operator],
                 'invalid': []},

    Operator: {'valid': [Keyword, Aggregate, Identifier, Operator],
               'invalid': ['SELECT', 'INSERT', 'UPDATE', 'DELETE']},

}
