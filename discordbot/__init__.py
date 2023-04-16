"""
Discord API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Discord API.
:copyright: (c) 2023-present Aril Ogai
:license: MIT, see LICENSE for more details.
"""

__title__ = 'discord'
__author__ = 'Aril Ogai'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023-present Aril Ogai'
__version__ = '1.0.0a'

import logging
from typing import NamedTuple, Literal

from .types.emoji import Emoji
from .types.member import Member
from .types.user import User
from .types.textchannel import TextChannel
from .types.role import Role
