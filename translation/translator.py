"""
Top level 'convenience' functions for the package.
"""
import googletrans as gt

from translation.language import Language


class Translator:
    def __init__(self, default_to_lang=None):
        self.__google_translator = gt.Translator()
        self.__default_to_lang = (default_to_lang
                                  if default_to_lang is not None
                                  else Language.EN)

    def __copy__(self):
        raise TypeError("Copying not supported!")

    def __deepcopy__(self, memodict={}):
        raise TypeError("Deep copying not supported!")

    def detect_language_of(self, text):
        return Language.from_string(
            self.__google_translator.detect(text).lang
        )

    def translate(self, text):
        if text.from_language is None:
            text.from_language = self.detect_language_of(text.body)

        if text.to_language is None:
            text.to_language = self.__default_to_lang

        if (text.from_language is Language.OTHER or
                text.to_language is Language.OTHER):
            raise ValueError(f"Can't translate: {text.body!r}")

        return self.__google_translator.translate(
            text.body,
            src=text.from_language.name.lower(),
            dest=text.to_language.name.lower()
        ).text

    def translate_many(self, texts):
        return [
            self.__try_to_translate(t)
            for t in texts
        ]

    def __try_to_translate(self, text):
        try:
            return self.translate(text)
        except ValueError as e:
            return e

    @property
    def default_to_language(self):
        return self.__default_to_lang
