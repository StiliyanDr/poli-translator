import enum


@enum.unique
class Language(enum.Enum):
    BG = enum.auto()
    EN = enum.auto()
    DE = enum.auto()
    FR = enum.auto()
    ES = enum.auto()
    OTHER = enum.auto()

    @classmethod
    def from_string(cls, s):
        return getattr(cls, s.upper(), cls.OTHER)
