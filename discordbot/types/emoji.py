from .discord_object import DiscordObject

class Emoji(DiscordObject):
    def __init__(self, id: int, name: str):
        super().__init__(id)
        self.name = name