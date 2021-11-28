import numpy.testing as npt

from sqlparser.tokens import Token


def test_token(capsys):
    class LazyToken(Token):
        def __init__(self, *args, **kwargs):
            kwargs["validate"] = False
            super(LazyToken, self).__init__(*args, **kwargs)

        def __str__(self):
            return 'lazy'

    print(LazyToken("LAZY"))
    captured = capsys.readouterr()
    npt.assert_equal(captured.out, "lazy\n")

    class InvalidToken(Token):
        def __init__(self, *args, **kwargs):
            kwargs["validate"] = False
            super(LazyToken, self).__init__(*args, **kwargs)

    with npt.assert_raises(TypeError):
        InvalidToken("INVALID")

    class ValidToken(Token):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __str__(self):
            return self.value

    valid_token = ValidToken("SELECT")
    npt.assert_equal(str(valid_token), "SELECT")
    npt.assert_equal(valid_token.value, "SELECT")
    npt.assert_equal(valid_token.properties['keyword'], True)

    for key in valid_token.properties.keys():
        if key != 'keyword':
            npt.assert_equal(valid_token.properties[key], False)

    valid_token.value = "+"
    npt.assert_equal(valid_token.value, "+")
    npt.assert_equal(valid_token.properties['operator'], True)

    with npt.assert_raises(ValueError):
        valid_token.value = "["
