from enum import Enum
class Role(str, Enum):
    ADMIN = "ADMIN"
    SELLER = "SELLER"
    USER = "USER"