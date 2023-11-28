from enum import Enum

class APILimitStatus(Enum):
    BELOW_SOFT_LIMIT = -1
    BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT = 0
    GREATER_THAN_HARD_LIMIT = 1
