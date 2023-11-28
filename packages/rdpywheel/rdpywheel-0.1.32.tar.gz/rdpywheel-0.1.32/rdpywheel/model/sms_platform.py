from enum import Enum, unique


@unique
class SmsPlatform(Enum):
    SMS_ACTIVE = 1
    CN_VIRTUAL = 2
