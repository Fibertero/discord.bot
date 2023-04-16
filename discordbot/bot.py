import asyncio, aiohttp, json, inspect, websockets
from inspect import signature, Parameter
from .http_client import HTTPClient
from .context import Context
from .embed import Embed
from .commands import Command
from .options import OptionType, Option

class ClientApp:
	def __init__(self, token, client_id):
		"""
		TODO:
		This code represents the second part of the ClientApp class, containing additional methods to handle various tasks related to Discord interactions. Some of the tasks include sending interaction responses, creating and managing slash commands, sending messages, and syncing commands with a guild (server). Additionally, it includes methods for handling global commands and guild audit logs.
		The code also contains methods for retrieving help information, deferring responses, and managing guild emojis. These methods allow the bot to perform operations such as listing, creating, modifying, and deleting guild emojis.
		In summary, this part of the ClientApp class adds essential functionalities to interact with the Discord API, enabling the bot to perform various tasks and respond to user interactions.
		"""
		self.token = token
		#self.session = aiohttp.ClientSession()
		self.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(self.loop)
		self.session = aiohttp.ClientSession(loop=self.loop)

		self.client_id = client_id
		self.commands = {}
		self.command_descriptions = {}
		self.event_handlers = {}
		self.http = HTTPClient(token, self.session)  # Adicione essa linha
		self.on_button_click = None  # Adicione este atributo
		self.on_select_menu = None
		self.on_ready = None
	
	async def __aenter__(self):
		""""
		TODO: Implement asynchronous context management for entering the bot's context. This will allow for the bot to be used in 'with' statements to properly initialize and clean up resources.
		"""
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		"""
		TODO: Implement asynchronous context management for entering the bot's context. This will allow for the bot to be used in 'with' statements to properly initialize and clean up resources.
		"""
		await self.close()

	"""async def start(self):
		try:
			await self.http.start()
			await self.connect()  # Adicione essa linha
		except KeyboardInterrupt:
			print("Bot shutdown!")
		finally:
			await self.on_shutdown()"""

	async def start(self):
		gateway_url = await self.get_gateway()
		async with websockets.connect(f"{gateway_url}?v=10&encoding=json") as websocket:
			await self.identify(websocket)
			await self.receive_data(websocket)

	async def close(self):
		await self.http.close()

	async def on_shutdown(self):
		await self.http.close()
		await self.session.close()  # Adicione essa linha

	async def connect(self):
		url = 'wss://gateway.discord.gg/?v=10&encoding=json'
		async with self.session.ws_connect(url) as ws:
			while True:
				data = await ws.receive_json()
				if data['op'] == 10:
					heartbeat_interval = data['d']['heartbeat_interval'] / 1000
					asyncio.create_task(self.heartbeat(ws, heartbeat_interval))
					await self.identify(ws)
				elif data['op'] == 0:
					await self.handle_event(data)
				elif data['op'] == 11:
					pass
					#print("Heartbeat ACK")
	
	def run(self):
		task = self.loop.create_task(self.connect())
		try:
			self.loop.run_until_complete(task)
		finally:
			self.loop.run_until_complete(self.loop.shutdown_asyncgens())
			self.loop.close()
			
	async def heartbeat(self, ws, interval):
		while True:
			await asyncio.sleep(interval)
			await ws.send_json({"op": 1, "d": None})

	async def identify(self, ws):
		payload = {
			"op": 2,
			"d": {
				"token": self.token,
				"intents": 513,  # Mude os intents conforme necessário
				"properties": {
					"$os": "linux",
					"$browser": "discord.bot",
					"$device": "discord.bot"
				}
			}
		}
		await ws.send_json(payload)
		data = await ws.receive_json()

		if data['t'] == 'READY':
			try:
				await self.handle_event(data)
			except Exception as e:
				print(f"An error occurred while receiving data: {e}")
	
	async def receive_data(self, websocket):
		async for message in websocket:
			data = json.loads(message)
			try:
				await self.handle_event(data)
			except Exception as e:
				print(f"An error occurred while receiving data: {e}")

	async def get_gateway(self):
		url = "https://discord.com/api/v10/gateway/bot"
		headers = {"Authorization": f"Bot {self.token}"}

		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers=headers) as response:
				gateway_data = await response.json()

		return gateway_data["url"]
	
	"""async def receive_data(self, ws):
		while True:
			try:
				data = await ws.receive_json()
				await self.handle_event(data)
			except Exception as e:
				print(f"An error occurred while receiving data: {e}")"""

	async def handle_event(self, data):
		"""
		MESSAGE_CREATE
		CHANNEL_CREATE
		GUILD_ROLE_DELETE
		INTERACTION_CREATE
		GUILD_ROLE_CREATE
		GUILD_ROLE_UPDATE
		GUILD_UPDATE
		"""

		if data['t'] == 'READY':
			if 'READY' in self.event_handlers:
				self.on_ready = self.event_handlers['READY']
			if self.on_ready:
				await self.on_ready(self)

		elif data['t'] == 'MESSAGE_CREATE':
			await self.handle_message(data['d'])
		elif data['t'] == 'INTERACTION_CREATE':
			await self.handle_interaction(data['d'])

	async def handle_message(self, message_data):
		content = message_data['content']

		if content.startswith('!'):  # Altere o prefixo do comando conforme necessário
			command_name = content[1:].split()[0]
			await self.execute_command(command_name, message_data)

	async def handle_interaction(self, interaction_data):
		handler = self.event_handlers

		if 'type' not in interaction_data: return
		if interaction_data['type'] == 2:  # 2 representa comandos de barra
			command_name = interaction_data['data']['name']
			await self.execute_slash_command(command_name, interaction_data)
		elif interaction_data['type'] == 3:  # 3 representa interações de componente
			#Eventos registrados com decoradores

			handler_on_button_click = handler.get("button_click")
			if handler_on_button_click:
				ctx = self.create_context(interaction_data)
				await self.on_button_click(ctx, interaction_data)
			
			handle_on_select_menu = handler.get("select_menu")
			if handle_on_select_menu:
				ctx = self.create_context(interaction_data)
				await self.on_button_click(ctx, interaction_data)

			#Eventos registrados manualmente
			if self.on_button_click and interaction_data['data']['component_type'] == 2:  # Verifique se o manipulador está definido
				ctx = self.create_context(interaction_data)
				await self.on_button_click(ctx, interaction_data)
			if self.on_select_menu  and interaction_data['data']['component_type'] == 3:  # Verifique se o manipulador está definido
				ctx = self.create_context(interaction_data)
				await self.on_select_menu(ctx, interaction_data)

	def event(self, event_name):
		def decorator(func):
			self.event_handlers[event_name] = func
			return func
		return decorator

	def get_command_type_hints(self, func):
		sig = inspect.signature(func)
		type_hints = {}
		for name, param in sig.parameters.items():
			if param.annotation != inspect.Parameter.empty:
				type_hints[name] = param.annotation
		return type_hints
	
	def add_command(self, command):
		self.commands[command.name] = command
	
	def get_command(self, command_name):
		return self.commands.get(command_name)
	
	def slash_command(self, name: str, description: str):
		def decorator(func):
			options = []
			for param in signature(func).parameters.values():
				if param.name != "ctx":
					options.append(Option(
						name=param.name,
						description=f"Enter a {param.annotation.__name__}",
						type=OptionType.from_annotation(param.annotation),
						required=param.default == Parameter.empty
					))
			command = Command(name, description, func, options=options)
			self.add_command(command)
			return func

		return decorator

	def command(self, name=None, description=None):
		def decorator(func):
			_name = name or func.__name__
			_description = description or "Sem descrição."

			self.commands[_name] = {
				"func": func,
				"name": _name,
				"description": _description,
			}
			return func

		return decorator

	# Dentro da classe MyBot em mybot.py
	# Dentro da classe MyBot em mybot.py
	async def on_command(self, interaction):
		command_name = interaction["data"]["name"]
		command_function = self.commands.get(command_name)

		if command_function:
			ctx = Context(self, interaction)
			await command_function(ctx)
		else:
			response_data = {
				"type": 4,
				"data": {
					"content": f"Comando desconhecido: {command_name}",
				}
			}
			await self.http.send_interaction_response(interaction["id"], interaction["token"], response_data)

	async def send_response(self, interaction_data, response, ephemeral=False):
		# Assuming you have the token and API_ENDPOINT defined earlier in your code
		interaction_id = interaction_data["id"]
		interaction_token = interaction_data["token"]

		url = f"https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback"
		
		json_payload = {
			"type": 4,  # This is the type for a message response
			"data": {
                "content": response,
                "flags": 64 if ephemeral else 6,
            },
		}

		headers = {
			"Authorization": f"Bot {self.token}",
			"Content-Type": "application/json"
		}

		async with aiohttp.ClientSession() as session:
			async with session.post(url, json=json_payload, headers=headers) as response:
				if response.status != 200:
					print(f"Failed to send response. Status code: {response.status}")
				if response.status != 204:
					print(f"Failed to send response. Status code: {response.status}")
					response_text = await response.text()
					print(f"Response content: {response_text}")
				await response.json()
	
	async def edit_response(self, interaction_data, json_payload, file=False):
		interaction_token = interaction_data["token"]

		url = f"https://discord.com/api/v10/webhooks/{self.client_id }/{interaction_token}/messages/@original"
		headers = {
			"Authorization": f"Bot {self.token}",
			"Content-Type": "application/json"
		}

		if file:
			# Se um arquivo for fornecido, use multipart para enviar o arquivo junto com o payload JSON
			form_data = aiohttp.FormData()
			form_data.add_field("payload_json", json.dumps(json_payload), content_type="application/json")
			form_data.add_field("file", file, filename=file.name, content_type="application/octet-stream")

			async with aiohttp.ClientSession() as session:
				async with session.patch(url, json=json_payload, headers=headers) as response:
					await response.json()
		else:
			async with aiohttp.ClientSession() as session:
				async with session.patch(url, json=json_payload, headers=headers) as response:
					await response.json()

	async def execute_command(self, command_name, message_data):
		command = self.commands.get(command_name)
		if command:
			ctx = self.create_context(message_data)
			await command.func(ctx)

	async def execute_slash_command(self, command_name, interaction_data):
		command = self.get_command(command_name)
		
		if command is not None:
			ctx = self.create_context(interaction_data)
			response = await command.func(ctx)
			
			if not ctx.deferred:  # Check if defer() has been called
				await self.send_response(interaction_data, response)
		else:
			print(f"Command '{command_name}' not found")
		if command is None:
			# Log a warning message or send an error response to the user
			print(f"Command '{command_name}' not found")
			return
	
	async def send_interaction_response(
		self,
		interaction_id,
		interaction_token,
		content=None,
		ephemeral=False,
		embed=None,
		components=None,
		):
		url = f"https://discord.com/api/interactions/{interaction_id}/{interaction_token}/callback"
		response_data = {
			"type": 4,
			"data": {
				"content": content or "",
				"flags": 64 if ephemeral else 0,
			},
		}

		if embed:
			response_data["data"]["embeds"] = [embed.to_dict()]

		if components:
			response_data["data"]["components"] = components

		await self.http.send_interaction_response(interaction_id, interaction_token, response_data)


	async def create_slash_command(self, guild_id, command_name, description, options=None):
		url = f"https://discord.com/api/applications/{self.client_id}/guilds/{str(guild_id)}/commands"
		command_data = {
			"name": command_name,
			"description": description,
			"options": options or []
		}
		async with self.session.post(url, headers={"Authorization": f"Bot {self.token}"}, json=command_data) as resp:
			if resp.status != 200 and resp.status != 201:
				print(f"Erro ao criar comando de barra: {resp.status} {await resp.text()}")
	
	def create_context(self, message_data):
		return Context(self, message_data)

	async def send_message(self, channel_id, content=None, embed=None, components=None, ephemeral=None):
		"""
		TODO: Implement a method to send messages from the bot to users on the platform or API.

		"""
		data = {}

		if ephemeral:
			data['ephemeral'] = ephemeral
		if content:
			data['content'] = content
		if embed:
			data['embeds'] = [embed]
		if components:
			data['components'] = components

		if not data:
			print('No information provided to send the message!')
			return
	
		async with self.session.post(f'https://discord.com/api/channels/{channel_id}/messages', headers={'Authorization': f'Bot {self.token}'}, json=data) as resp:
			if resp.status != 200 and resp.status != 201:
				print(f'Falha ao enviar mensagem: {resp.status} {await resp.text()}')

	async def sync_with_guild(self, guild_id):
		existing_commands = await self.get_guild_commands(str(guild_id))
		existing_commands_dict = {cmd['name']: cmd for cmd in existing_commands}
		for command_name, command in self.commands.items():
			if command_name in existing_commands_dict:
				existing_command = existing_commands_dict[command_name]
				await self.update_guild_command(str(guild_id), existing_command['id'], command)
			else:
				await self.create_guild_command(str(guild_id), command)

		for existing_command in existing_commands:
			if existing_command['name'] not in self.commands:
				await self.delete_guild_command(str(guild_id), existing_command['id'])

	async def get_guild_commands(self, guild_id):
		url = f"https://discord.com/api/applications/{self.client_id}/guilds/{str(guild_id)}/commands"
		async with self.session.get(url, headers={"Authorization": f"Bot {self.token}"}) as resp:
			if resp.status == 200:
				return await resp.json()
			else:
				print(f"Erro ao obter comandos da guilda: {resp.status} {await resp.text()}")
				return []

	async def create_guild_command(self, guild_id, command):
		url = f"https://discord.com/api/applications/{self.client_id}/guilds/{str(guild_id)}/commands"
		command_data = {
			"name": command.name,
			"description": command.description,
			"options": command.options or []
		}
		async with self.session.post(url, headers={"Authorization": f"Bot {self.token}"}, json=command_data) as resp:
			if resp.status != 200 and resp.status != 201:
				print(f"Erro ao criar comando de barra: {resp.status} {await resp.text()}")

	async def update_guild_command(self, guild_id, command_id, command):
		url = f"https://discord.com/api/applications/{self.client_id}/guilds/{str(guild_id)}/commands/{command_id}"
		command_data = {
			"name": command.name,
			"description": command.description,
			"options": command.options or []
		}
		async with self.session.patch(url, headers={"Authorization": f"Bot {self.token}"}, json=command_data) as resp:
			if resp.status != 200:
				print(f"Erro ao atualizar comando de barra: {resp.status} {await resp.text()}")

	async def delete_guild_command(self, guild_id, command_id):
		url = f"https://discord.com/api/applications/{self.client_id}/guilds/{str(guild_id)}/commands/{command_id}"
		async with self.session.delete(url, headers={"Authorization": f"Bot {self.token}"}) as resp:
			if resp.status != 200:
				print(f"Erro ao excluir comando de barra: {resp.status} {await resp.text()}")

	# Dentro da classe MyBot em mybot.py
	async def register_guild_commands(self, guild_id):
		for command_name, command_description in self.command_descriptions.items():
			command_data = {"name": command_name, "description": command_description}
			await self.create_guild_command(guild_id, command_data)

	async def get_global_commands(self):
		url = f"https://discord.com/api/applications/{self.client_id}/commands"
		async with self.session.get(url, headers={"Authorization": f"Bot {self.token}"}) as resp:
			if resp.status == 200:
				return await resp.json()
			else:
				print(f"Erro ao obter comandos globais: {resp.status} {await resp.text()}")
				return []

	async def create_global_command(self, command):
		url = f"https://discord.com/api/applications/{self.client_id}/commands"
		command_data = {
			"name": command.name,
			"description": command.description,
			"options": command.options or []
		}
		async with self.session.post(url, headers={"Authorization": f"Bot {self.token}"}, json=command_data) as resp:
			if resp.status != 200 and resp.status != 201:
				print(f"Erro ao criar comando global: {resp.status} {await resp.text()}")

	async def update_global_command(self, command_id, command):
		url = f"https://discord.com/api/applications/{self.client_id}/commands/{command_id}"
		command_data = {
			"name": command.name,
			"description": command.description,
			"options": command.options or []
		}
		async with self.session.patch(url, headers={"Authorization": f"Bot {self.token}"}, json=command_data) as resp:
			if resp.status != 200:
				print(f"Erro ao atualizar comando global: {resp.status} {await resp.text()}")

	async def delete_global_command(self, command_id):
		url = f"https://discord.com/api/applications/{self.client_id}/commands/{command_id}"
		async with self.session.delete(url, headers={"Authorization": f"Bot {self.token}"}) as resp:
			if resp.status != 200:
				print(f"Erro ao excluir comando global: {resp.status} {await resp.text()}")

	async def sync_global_commands(self):
		existing_commands = await self.get_global_commands()
		existing_commands_dict = {cmd['name']: cmd for cmd in existing_commands}

		for command_name, command in self.commands.items():
			if command_name in existing_commands_dict:
				existing_command = existing_commands_dict[command_name]
				await self.update_global_command(existing_command['id'], command)
			else:
				await self.create_global_command(command)

		for existing_command in existing_commands:
			if existing_command['name'] not in self.commands:
				await self.delete_global_command(existing_command['id'])

	async def get_guild_audit_logs(self, guild_id, limit=50, before=None, after=None, user_id=None, action_type=None):
		params = {"limit": limit}
		if before:
			params["before"] = before
		if after:
			params["after"] = after
		if user_id:
			params["user_id"] = user_id
		if action_type:
			params["action_type"] = action_type

		url = f"https://discord.com/api/guilds/{guild_id}/audit-logs"
		headers = {"Authorization": f"Bot {self.token}"}
		async with self.session.get(url, headers=headers, params=params) as resp:
			if resp.status == 200:
				return await resp.json()
			else:
				print(f"Error getting guild audit logs: {resp.status} {await resp.text()}")
				return None
			
	def get_help(self):
		"""
		TODO: Provide help information to users, including a list of available commands and their usage instructions.
		"""
		help_text = "Here's a list of available commands:\n\n"

		# Get all methods in the Bot class
		methods = inspect.getmembers(self, predicate=inspect.ismethod)

		for method_name, method in methods:
			# Exclude special methods (e.g., __init__)
			if not method_name.startswith("__"):
				command_description = method.__doc__.strip() if method.__doc__ else "No description available."
				help_text += f"{method_name}: {command_description}\n"

		return help_text

	async def defer(self, interaction_data, ephemeral=True):
		interaction_id = interaction_data["id"]
		interaction_token = interaction_data["token"]

		defer_data = {
			"type": 5,  # ACK with source
			"data": {
				"flags": 64 if ephemeral else 0,
			},
		}

		url = f"https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback"
		async with aiohttp.ClientSession() as session:
			async with session.post(url, json=defer_data) as resp:
				if resp.status != 204:
					print(f"Failed to defer the response. Status code: {resp.status}")
	

	async def list_guild_emojis(self, guild_id):
		url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis"
		headers = {"Authorization": f"Bot {self.token}"}
		
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers=headers) as response:
				return await response.json()

	async def get_guild_emoji(self, guild_id, emoji_id):
		url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis/{emoji_id}"
		headers = {"Authorization": f"Bot {self.token}"}
		
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers=headers) as response:
				return await response.json()

	async def create_guild_emoji(self, guild_id, name, image_data, roles):
		url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis"
		headers = {"Authorization": f"Bot {self.token}"}
		json_payload = {
			"name": name,
			"image": image_data,
			"roles": roles
		}
		
		async with aiohttp.ClientSession() as session:
			async with session.post(url, headers=headers, json=json_payload) as response:
				return await response.json()

	async def modify_guild_emoji(self, guild_id, emoji_id, name=None, roles=None):
		url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis/{emoji_id}"
		headers = {"Authorization": f"Bot {self.token}"}
		json_payload = {}

		if name:
			json_payload["name"] = name
		if roles:
			json_payload["roles"] = roles
		
		async with aiohttp.ClientSession() as session:
			async with session.patch(url, headers=headers, json=json_payload) as response:
				return await response.json()

	async def delete_guild_emoji(self, guild_id, emoji_id):
		url = f"https://discord.com/api/v10/guilds/{guild_id}/emojis/{emoji_id}"
		headers = {"Authorization": f"Bot {self.token}"}
		
		async with aiohttp.ClientSession() as session:
			async with session.delete(url, headers=headers) as response:
				return response.status == 204
