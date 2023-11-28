from enum import Enum


class Flag(str, Enum):
    RENAME = "REPLACE"
    RENAME_NOREPLACE = "NO_REPLACE"
    RENAME_EXCHANGE = "EXCHANGE"
