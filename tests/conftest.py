import pytest

import translation as tr


@pytest.fixture
def translator():
    return tr.Translator()


@pytest.fixture
def english_text():
    return "hello young sir"


@pytest.fixture
def unsupported_language_text():
    return "witaj młody panie"


@pytest.fixture
def german_text():
    return "Hallo junger Herr"


@pytest.fixture
def french_text():
    return "bonjour jeune monsieur"
