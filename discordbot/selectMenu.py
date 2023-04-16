class SelectMenuBuilder:
	@staticmethod
	def create_select_menu(custom_id, options, placeholder=None):
		select_menu = {
			"type": 1,
			"components": [
				{
					"type": 3,
					"custom_id": custom_id,
					"options": options,
					"placeholder": placeholder or "Selecione uma opção",
				}
			],
		}
		return select_menu