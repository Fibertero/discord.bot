from .discord_object import DiscordObject

class Member(DiscordObject):
    def __init__(self, id: int, display_name: str):
        super().__init__(id)
        self.display_name = display_name