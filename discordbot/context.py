import asyncio, aiohttp, json
from urllib import parse, request
from .custom_json_encoder import CustomJSONEncoder

class Context:
	def __init__(self, bot, message_data):
		"""
		TODO:
		The code uses the Discord API to perform the actions, and it makes the requests with the aiohttp library to ensure that the requests are asynchronous and non-blocking. This is important for a Discord bot to ensure that it can handle multiple commands concurrently without causing delays.
		In each method, the appropriate API endpoint is constructed using the base URL (https://discord.com/api/v10/) and the required parameters (like channel ID, message ID, etc.). The headers for the requests include the bot's authorization token. The responses from the Discord API are then handled accordingly.
		In the send and edit methods, if a file is included in the request, the code uses the aiohttp.FormData class to create a multipart request payload that includes both the JSON data and the file.
		The add_reaction method encodes the emoji to a URL-safe format using the urllib.parse.quote function before making the request.
		"""
		self.bot = bot
		self.channel_id = message_data["channel_id"]
		self.user_id = message_data["member"]["user"]["id"]
		self.id = message_data["id"]
		self.bot = bot
		self.message_data = message_data
		self.deferred = False

	async def defer(self, ephemeral=True):
		"""
		TODO:
		Marks the interaction as deferred, which allows the bot to take more time to process the command without causing a timeout.
		"""
		await self.bot.defer(self.message_data, ephemeral)
		self.deferred = True
	
	async def send(self, content=None, **kwargs):
		"""
		TODO:
		Sends a message to the specified channel with optional parameters like content, embed, components, ephemeral, file, and text-to-speech (TTS).
		"""
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
				# Modifique esta linha para usar o CustomJSONEncoder
				form_data.add_field("payload_json", json.dumps(json_payload, cls=CustomJSONEncoder), content_type="application/json")
				form_data.add_field("file", file, filename=file.name, content_type="application/octet-stream")

				async with aiohttp.ClientSession() as session:
					async with session.post(url, headers=headers, data=form_data) as response:
						await response.json()
			else:

				async with aiohttp.ClientSession() as session:
					async with session.post(url, headers=headers, json=json_payload) as response:
						await response.json()


	async def edit(self, message_id, content=None, **kwargs):
		"""
		TODO:
		Edits an existing message with the given message ID and new content, embed, components, file, and TTS.
		"""
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
		"""
		TODO:
		Deletes a message with the given message ID.
		"""
		url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages/{message_id}"
		headers = {"Authorization": f"Bot {self.bot.token}"}

		json_payload = json.dumps(json_payload, cls=CustomJSONEncoder)
		async with aiohttp.ClientSession() as session:
			async with session.post(url, headers=headers, data=json_payload) as response:
				await response.json()

	async def add_reaction(self, message_id, emoji):
		"""
		TODO:
		Adds a reaction (emoji) to a message with the given message ID.
		"""
		# Encode the emoji to URL format
		encoded_emoji = parse.quote(emoji, safe='')
		url = f"https://discord.com/api/v10/channels/{self.channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me"
		headers = {"Authorization": f"Bot {self.bot.token}"}

		async with aiohttp.ClientSession() as session:
			async with session.put(url, headers=headers) as response:
				if response.status != 204:
					print(f"Failed to add reaction. Status code: {response.status}")