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

    def translate(self,
                  text,
                  *,
                  from_lang=None,
                  to_lang=None):
        if from_lang is None:
            from_lang = self.detect_language_of(text)

        if to_lang is None:
            to_lang = self.__default_to_lang

        if from_lang is Language.OTHER or to_lang is Language.OTHER:
            raise ValueError(f"Can't translate: {text!r}")

        return self.__google_translator.translate(
            text,
            src=from_lang.name.lower(),
            dest=to_lang.name.lower()
        ).text

    @property
    def default_to_language(self):
        return self.__default_to_lang
