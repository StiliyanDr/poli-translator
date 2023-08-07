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
