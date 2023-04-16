class MessageComponentInteraction:
    def __init__(self, interaction_data):
        self.interaction_data = interaction_data
        self.type = interaction_data["type"]
        self.channel_id = interaction_data["channel_id"]
        self.message_id = interaction_data["message"]["id"]
        self.custom_id = interaction_data["data"]["custom_id"]
        self.component_type = interaction_data["data"]["component_type"]
        self.user_id = interaction_data["member"]["user"]["id"]
        self.guild_id = interaction_data["guild_id"]
        self.application_id = interaction_data["application_id"]
        self.token = interaction_data["token"]
        self.id = interaction_data["id"]

    def get_value(self):
        if self.component_type == 3:  # Select Menu
            values = self.interaction_data["data"]["values"]
            return values[0] if values else None
        return None
