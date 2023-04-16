import asyncio, aiohttp, json
from urllib import parse, request

class Context:
	def __init__(self, bot, message_data):
		self.bot = bot
		self.channel_id = message_data["channel_id"]
		self.user_id = message_data["member"]["user"]["id"]
		self.id = message_data["id"]
		self.bot = bot
		self.message_data = message_data
		self.deferred = False

	async def defer(self, ephemeral=True):
		await self.bot.defer(self.message_data, ephemeral)
		self.deferred = True
	
	async def send(self, content=None, **kwargs):
		content = kwargs.get("content") if content is None else content
		embed = kwargs.get("embed")
		components = kwargs.get("components")
		ephemeral = kwargs.get("ephemeral")
		file = kwargs.get("file")
		tts = kwargs.get("tts")

		url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages"
		headers = {"Authorization": f"Bot {self.bot.token}"}

		if embed:
			embed = embed.to_dict()

		json_payload = {
			"content": content,
			"embed": embed,
			"components": components,
			"flags": 64 if ephemeral else 0,
			"tts": tts,
		}

		if self.deferred:
			await self.bot.edit_response(self.message_data, json_payload, file=file)
		else:
			if file:
				# Se um arquivo for fornecido, use multipart para enviar o arquivo junto com o payload JSON
				form_data = aiohttp.FormData()
				form_data.add_field("payload_json", json.dumps(json_payload), content_type="application/json")
				form_data.add_field("file", file, filename=file.name, content_type="application/octet-stream")

				async with aiohttp.ClientSession() as session:
					async with session.post(url, headers=headers, data=form_data) as response:
						await response.json()
			else:
				async with aiohttp.ClientSession() as session:
					async with session.post(url, headers=headers, json=json_payload) as response:
						await response.json()


	async def edit(self, message_id, content=None, **kwargs):
		embed = kwargs.get("embed")
		components = kwargs.get("components")
		file = kwargs.get("file")
		tts = kwargs.get("tts")

		if embed:
			embed = embed.to_dict()

		json_payload = {
			"content": content,
			"embed": embed,
			"components": components,
			"tts": tts,
		}

		url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages/{message_id}"
		headers = {"Authorization": f"Bot {self.bot.token}", "Content-Type": "application/json"}

		async with aiohttp.ClientSession() as session:
			async with session.patch(url, headers=headers, json=json_payload) as response:
				await response.json()

	async def delete(self, message_id):
		url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages/{message_id}"
		headers = {"Authorization": f"Bot {self.bot.token}"}

		async with aiohttp.ClientSession() as session:
			async with session.delete(url, headers=headers) as response:
				if response.status != 204:
					print(f"Failed to delete message. Status code: {response.status}")

	async def add_reaction(self, message_id, emoji):
		# Encode the emoji to URL format
		encoded_emoji = parse.quote(emoji, safe='')
		url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
		headers = {"Authorization": f"Bot {self.bot.token}"}

		async with aiohttp.ClientSession() as session:
			async with session.put(url, headers=headers) as response:
				if response.status != 204:
					print(f"Failed to add reaction. Status code: {response.status}")