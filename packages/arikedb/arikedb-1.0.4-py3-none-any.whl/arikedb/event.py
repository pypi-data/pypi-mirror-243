from enum import Enum


class Event(Enum):
    ON_SET = "set"
    ON_CHANGE = "change"
    ON_RISE = "rise"
    ON_FALL = "fall"
