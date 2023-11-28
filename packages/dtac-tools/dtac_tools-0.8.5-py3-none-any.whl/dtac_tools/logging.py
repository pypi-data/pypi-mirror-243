from enum import Enum

class LoggingLevel(Enum):
    LevelDebug = 0
    LevelInfo = 1
    LevelWarning = 2
    LevelError = 3
    LevelFatal = 4

class LogMessage:
    def __init__(self, level, message, fields):
        self.level = level
        self.message = message
        self.fields = fields