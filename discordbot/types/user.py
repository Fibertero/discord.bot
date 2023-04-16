from .discord_object import DiscordObject

class User(DiscordObject):
    def __init__(self, id: int, username: str, discriminator: str):
        super().__init__(id)
        self.username = username
        self.discriminator = discriminator

    @property
    def mention(self):
        return f"<@{self.id}>"