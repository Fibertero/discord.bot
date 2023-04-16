import requests
from enum import IntEnum
from .types.emoji import Emoji
from .types.member import Member
from .types.user import User
from .types.textchannel import TextChannel
from .types.role import Role


class OptionType(IntEnum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    MEMBER = 11
    EMOJI = 12
    ROLE_OR_USER = 13

    @classmethod
    def from_annotation(cls, annotation):
        if annotation == int:
            return cls.INTEGER
        elif annotation == str:
            return cls.STRING
        elif annotation == bool:
            return cls.BOOLEAN
        elif annotation == Member:
            return cls.MEMBER
        elif annotation == User:
            return cls.USER
        elif annotation == TextChannel:
            return cls.CHANNEL
        elif annotation == Role:
            return cls.ROLE
        elif annotation == Emoji:
            return cls.EMOJI
        else:
            raise ValueError(f"Unsupported annotation type: {annotation}")


class Option:
    def __init__(self, name, description, type, required):
        self.name = name
        self.description = description
        self.type = type
        self.required = required

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "required": self.required,
        }