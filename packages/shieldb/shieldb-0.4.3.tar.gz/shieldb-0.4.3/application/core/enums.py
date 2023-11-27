from enum import Enum


class Actions(Enum):
    DELETE = "delete"
    MASK = "mask"
    PLACE_TO_MASK = "all"
    CONFIRM = "y"
    SHUFFLE_METHOD = "shuffle"
    REGEX_METHOD = "regex"
    REVERSE_METHOD = "reverse"
    RANDOM_METHOD = "random_char"
    MIDDLE_MASK_CHAR_METHOD = "middle"
    MIDDLE_RANDOM_CHARACTER_METHOD = "random_character"
    START_METHOD = "start"
    NLTK_METHOD = "nltk"
    END_METHOD = "end"
    MASK_CHAR = '*'
