class Embed:
	def __init__(
		self,
		title=None,
		description=None,
		color=None,
		url=None,
		timestamp=None,
		fields=None,
		author=None,
		footer=None,
		thumbnail=None,
		image=None,
	):
		self.title = title
		self.description = description
		self.color = color
		self.url = url
		self.timestamp = timestamp
		self.fields = fields or []
		self.author = author
		self.footer = footer
		self.thumbnail = thumbnail
		self.image = image

	def add_field(self, name, value, inline=False):
		self.fields.append({"name": name, "value": value, "inline": inline})

	def set_author(self, name, url=None, icon_url=None):
		self.author = {"name": name, "url": url, "icon_url": icon_url}

	def set_footer(self, text, icon_url=None):
		self.footer = {"text": text, "icon_url": icon_url}

	def set_thumbnail(self, url):
		self.thumbnail = {"url": url}

	def set_image(self, url):
		self.image = {"url": url}

	def to_dict(self):
		embed_dict = {}
		if self.title:
			embed_dict["title"] = self.title
		if self.description:
			embed_dict["description"] = self.description
		if self.color:
			embed_dict["color"] = self.color
		if self.url:
			embed_dict["url"] = self.url
		if self.timestamp:
			embed_dict["timestamp"] = self.timestamp.isoformat()
		if self.fields:
			embed_dict["fields"] = self.fields
		if self.author:
			embed_dict["author"] = self.author
		if self.footer:
			embed_dict["footer"] = self.footer
		if self.thumbnail:
			embed_dict["thumbnail"] = self.thumbnail
		if self.image:
			embed_dict["image"] = self.image
		return embed_dict