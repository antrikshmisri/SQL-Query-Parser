"""Module to represent SQL tokens as classes"""
import abc
from re import compile as regex_compile
from re import error
from re import match as regex_match

__TOKEN_TYPES__ = {
    'keyword': ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'LIKE', 'IN', 'GROUP BY'],
    'operator': ['=', '<', '>', '<=', '>=', '!=', '+', '-', '*', '/', '%'],
    'separator': ['(', ')', ',', ';'],
    'identifier': ['[a-zA-Z_][a-zA-Z0-9_]*'],
    'number': ['[0-9]+'],
    'string': ['\'[^\']*\''],
    'whitespace': ['[ \t\n\r]+'],
    'aggregate': ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX'],
}


class Token(abc.ABC):
    """Umbrella class for all token classes"""

    def __init__(self, value, validate=True, valid_token_dict=None):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        self._value = str()
        self._properties = dict()

        self.validate = validate
        self.token_dict = valid_token_dict or __TOKEN_TYPES__

        self.value = value

        if self.value is None:
            raise ValueError("Value cannot be None")

        if self.validate:
            self._validate_value()

    def _validate_value(self):
        """Validate a value against token types."""
        for token_item in self.token_dict.items():
            token_type = token_item[0]
            token_values = token_item[1]

            if len(token_values) == 1:
                try:
                    regex_compile(token_values[0])
                    is_valid_pattern = True
                except error:
                    is_valid_pattern = False

                if is_valid_pattern:
                    if regex_match(token_values[0], self.value):
                        self._properties[token_type] = True
                    else:
                        self._properties[token_type] = False
            else:
                if self.value in token_values:
                    self._properties[token_type] = True
                else:
                    self._properties[token_type] = False

        if not any(list(self._properties.values())):
            raise ValueError(f"Value {self.value} is not a valid token")
        elif 'identifier' in self._properties:
            if self._properties['identifier'] and sum(int(value) for value in self._properties.values()) > 1:
                self._properties['identifier'] = False

    @abc.abstractmethod
    def __str__(self):
        """Return the string representation of the token"""
        _msg = "This method must be implemented by the child class."
        raise NotImplementedError(_msg)

    @property
    def value(self):
        """Return the value of the token"""
        return self._value

    @value.setter
    def value(self, value):
        """Set the value of the token"""
        self._value = value
        if self.validate:
            self._validate_value()

    @property
    def properties(self):
        """Return all the properties of the token in `dict` format"""
        return self._properties


class Keyword(Token):
    """Class to represent SQL keywords"""

    def __init__(self, value, validate=True, 
                 valid_token_dict={'keyword': __TOKEN_TYPES__['keyword']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""Keyword({self.value})"""


class Operator(Token):
    """Class to represent SQL operators"""

    def __init__(self, value, validate=True,
                 valid_token_dict={'operator': __TOKEN_TYPES__['operator']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""Operator({self.value})"""


class Separator(Token):
    """Class to represent SQL separators"""

    def __init__(self, value, validate=True,
                 valid_token_dict={'separator': __TOKEN_TYPES__['separator']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""Separator({self.value})"""


class Identifier(Token):
    """Class to represent SQL identifiers"""

    def __init__(self, value, validate=True,
                 valid_token_dict={'identifier': __TOKEN_TYPES__['identifier']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""Identifier({self.value})"""


class Number(Token):
    """Class to represent SQL numbers"""

    def __init__(self, value, validate=True,
                 valid_token_dict={'number': __TOKEN_TYPES__['number']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""Number({self.value})"""


class String(Token):
    """Class to represent SQL strings"""

    def __init__(self, value, validate=True,
                 valid_token_dict={'string': __TOKEN_TYPES__['string']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""String({self.value})"""


class Whitespace(Token):
    """Class to represent SQL whitespaces"""

    def __init__(self, value, validate=True,
                 valid_token_dict={'whitespace': __TOKEN_TYPES__['whitespace']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""Whitespace({repr(self.value)})"""


class Aggregate(Token):
    """Class to represent SQL aggregates"""

    def __init__(self, value, validate=True,
                 valid_token_dict={'aggregate': __TOKEN_TYPES__['aggregate']}):
        """Initialize the class.
        
        Parameters
        ----------
        value: str
            The value of token
        validate: bool
            Whether to validate the value against token types
        valid_token_dict: dict
            A dictionary of valid token types and their values
        """
        super().__init__(value, validate, valid_token_dict)

    def __str__(self):
        """Return the string representation of the token"""
        return f"""Aggregate({self.value})"""
