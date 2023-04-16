import requests
from enum import IntEnum
from .types.emoji import Emoji
from .types.member import Member
from .types.user import User
from .types.textchannel import TextChannel
from .types.role import Role


class OptionType(IntEnum):
    """
    TODO:
    This code snippet defines several classes and an enumeration to create and manage options for commands in a Discord bot. The classes include OptionType, Option, and Choice, while the enumeration is OptionType.    
    OptionType is an enumeration subclassing IntEnum that defines various types of command options. The from_annotation class method takes an annotation as input and returns the corresponding OptionType value based on the type of the annotation.
    Note: The code also imports several types used in the OptionType enumeration, such as Emoji, Member, User, TextChannel, and Role. These types are not defined in the code snippet, so you can assume that they are defined elsewhere in the bot's codebase.
    """
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
    """
    TODO:
    Option class represents a command option. It has a name, description, type (from OptionType), whether it's required or not, and an optional list of choices. The __init__ method initializes the option instance with the given parameters. The to_dict method converts the Option object into a dictionary format, which can be used when interacting with the Discord API.
    """
    def __init__(self, name, description, type, required, choices=None):
        self.name = name
        self.description = description
        self.type = type
        self.required = required
        self.choices = choices if choices is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type.value,
            "required": self.required,
            "choices": [choice.to_dict() for choice in self.choices] if self.choices else None
        }
    

class Choice:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_dict(self):
        """
        TODO:
        Choice class represents a single choice within an option. It has a name and a value. The __init__ method initializes the choice instance with the given parameters. The to_dict method converts the Choice object into a dictionary format, which can also be used when interacting with the Discord API.
        """
        return {
            "name": self.name,
            "value": self.value
        }
