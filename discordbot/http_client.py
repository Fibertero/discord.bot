import json
import aiohttp
from aiohttp.helpers import current_task

API_BASE_URL = "https://discord.com/api/v10"


class HTTPClient:
	"""
	TODO:
	This code defines an HTTPClient class to manage HTTP requests to the Discord API. The class is initialized with a bot token and an aiohttp session. It provides several methods to interact with the Discord API, such as getting guilds, sending interaction responses, and managing guild commands.
	The request method is the core method for handling HTTP requests. It sets the necessary headers, converts JSON data to a string, and constructs the full URL for the API endpoint. The method then sends the request using the aiohttp session and handles the response accordingly. If the response status code is 204 (No Content), it returns None. Otherwise, it returns the JSON response data.
	The other methods in the HTTPClient class are specific to different Discord API endpoints and use the request method to send their respective requests.
	"""
	def __init__(self, token, session):
		self.token = token
		self.session = session
	
	async def close(self):
		"""
		TODO:
		Closes the aiohttp session.
		"""
		await self.session.close()

	async def start(self):
		"""
		TODO:
		Creates a new aiohttp session.
		"""
		self.session = aiohttp.ClientSession()

	async def get_guilds(self):
		"""
		TODO:
		Retrieves the guilds the bot is in.
		"""
		url = f"https://discord.com/api/users/@me/guilds"
		headers = {"Authorization": f"Bot {self.token}"}
		async with self.session.get(url, headers=headers) as resp:
			if resp.status == 200:
				return await resp.json()
			else:
				print(f"Erro ao obter guildas: {resp.status} {await resp.text()}")
				return []

	async def request(self, method, path, **kwargs):
		"""
		TODO:
		A generic request method that sends an HTTP request with the given method and path, as well as any additional kwargs. The headers are set to include the bot's authorization token and a content type of "application/json".
		"""
		headers = kwargs.get("headers", {})
		headers["Authorization"] = f"Bot {self.token}"
		headers["Content-Type"] = "application/json"
		kwargs["headers"] = headers

		if "json" in kwargs:
			kwargs["data"] = json.dumps(kwargs["json"])
			del kwargs["json"]

		url = API_BASE_URL + path
		async with self.session.request(method, url, **kwargs) as response:
			if response.status >= 300:
				raise Exception(f"Erro ao fazer requisição: {response.status} {await response.text()}")
			if response.status == 204:
				return None
			return await response.json()

	async def send_interaction_response(self, interaction_id, interaction_token, response_data):
		"""
		TODO:
		Sends an interaction response using the interaction ID and token, along with the response data.
		"""
		path = f"/interactions/{interaction_id}/{interaction_token}/callback"
		return await self.request("POST", path, json=response_data)

	async def create_guild_command(self, guild_id, command_data):
		"""
		TODO:
		Creates a new guild command using the guild ID and the command data.
		"""
		path = f"/applications/{self.token}/guilds/{guild_id}/commands"
		return await self.request("POST", path, json=command_data)

	async def get_guild_commands(self, guild_id):
		"""
		TODO:
		Retrieves all the commands for a given guild.
		"""
		path = f"/applications/{self.token}/guilds/{guild_id}/commands"
		return await self.request("GET", path)

	async def delete_guild_command(self, guild_id, command_id):
		"""
		TODO:
		Deletes a command in a guild using the guild ID and command ID.
		"""
		path = f"/applications/{self.token}/guilds/{guild_id}/commands/{command_id}"
		return await self.request("DELETE", path)
