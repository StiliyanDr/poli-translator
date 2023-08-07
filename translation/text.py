from typing import Optional

from translation.language import Language


class Text:
    def __init__(self,
                 body: Optional[str] = None,
                 from_language: Optional[Language] = None,
                 to_language: Optional[Language] = None):
        self.body = body
        self.from_language = from_language
        self.to_language = to_language

    def __eq__(self, other):
        return (
            type(self) == type(other) and
            self.body == other.body and
            self.from_language is other.from_language and
            self.to_language is other.to_language
        )
