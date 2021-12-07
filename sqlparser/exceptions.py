
class InvalidQueryError(Exception):
    def __init__(self, message):
        self.message = f"Invalid Query. {message}"

    def __str__(self):
        return self.message


class QueryParseError(Exception):
    def __init__(self, message):
        self.message = f"Couldn't parse query. {message}"

    def __str__(self):
        return self.message
