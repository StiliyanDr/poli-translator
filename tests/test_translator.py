import copy

import pytest

import translation as tr


class TestConstructor:
    def test_default_to_language_defaults_to_english(self):
        translator = tr.Translator()

        assert translator.default_to_language is tr.Language.EN

    def test_default_to_language_can_be_set(self):
        translator = tr.Translator(tr.Language.DE)

        assert translator.default_to_language is tr.Language.DE


class TestCopying:
    def test_shallow_copy_raises_error(self, translator):
        with pytest.raises(TypeError):
            copy.copy(translator)

    def test_deep_copy_raises_error(self, translator):
        with pytest.raises(TypeError):
            copy.deepcopy(translator)


class TestLanguageDetection:
    def test_detection_of_supported_language_returns_it(
        self,
        translator,
        english_text
    ):
        lang = translator.detect_language_of(english_text)

        assert lang is tr.Language.EN

    def test_detection_of_unsupported_language_returns_other(
        self,
        translator,
        unsupported_language_text
    ):
        lang = translator.detect_language_of(unsupported_language_text)

        assert lang is tr.Language.OTHER


class TestTranslateOne:
    def test_defaults_are_from_detected_and_to_from_ctor(
        self,
        german_text,
        french_text
    ):
        translator = tr.Translator(default_to_lang=tr.Language.DE)

        translated = translator.translate(french_text)

        assert translated == german_text

    def test_exception_is_raised_for_unsupported_from_language(
        self,
        translator,
        unsupported_language_text
    ):
        with pytest.raises(ValueError):
            translator.translate(unsupported_language_text)

    def test_with_selected_languages(
        self,
        translator,
        french_text,
        german_text
    ):
        translated = translator.translate(
            french_text,
            from_lang=tr.Language.FR,
            to_lang=tr.Language.DE
        )

        assert translated == german_text
