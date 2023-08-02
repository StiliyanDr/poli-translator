from translation import Language


def test_creating_supported_language():
    assert Language.from_string("en") is Language.EN


def test_creating_unsupported_language_returns_other():
    assert Language.from_string("zz") is Language.OTHER
