import random
import asyncio

try:
	import discord
	from discord.ext import commands
except ImportError:
	print("Unable to load General cog. Check your discord.py installation.")

BOTNAMES = ["Agnes", "Alfred", "Archy", "Barty", "Benjamin", "Bertram",
	"Bruni", "Buster", "Edith", "Ester", "Flo", "Francis", "Francisco", "Gil",
	"Gob", "Gus", "Hank", "Harold", "Harriet", "Henry", "Jacques", "Jorge",
	"Juan", "Kitty", "Lionel", "Louie", "Lucille", "Lupe", "Mabel", "Maeby",
	"Marco", "Marta", "Maurice", "Maynard", "Mildred", "Monty", "Mordecai",
	"Morty", "Pablo", "Seymour", "Stan", "Tobias", "Vivian", "Walter", "Wilbur"]

class General:
	"""General features, including automatic name changing and welcome messages"""

	def __init__(self, bot):
		self.bot = bot

	async def set_nick(self, newnick):
		for server in self.bot.servers:
			await self.bot.change_nickname(server.me, "%s Bot" % newnick)

	def choose_nick(self):
		current_nick = list(self.bot.servers)[0].me.nick # Since the nickname should be the same for all servers, it shouldn't matter that self.bot.servers isn't always in the same order
		newnick = random.choice(BOTNAMES)
		while newnick == current_nick:
			newnick = random.choice(BOTNAMES) # Keep rerolling until we get a different name
		return newnick

	# Change nickname every 10 minutes
	async def change_nick(self):
		await self.bot.wait_until_ready()
		while not self.bot.is_closed:
			serverlist = list(self.bot.servers)
			if len(serverlist) > 0:
				await self.set_nick(self.choose_nick())
			await asyncio.sleep(self.bot.settings["changenick_interval"])

	async def on_server_join(self, server):
		await self.set_nick(self.choose_nick())

	def welcome_channel(self, server):
		return self.bot.server_settings_list[server.id]["welcome_channel"]

	def welcome_messages(self, server):
		return self.bot.server_settings_list[server.id]["welcome_messages"]

	def set_welcome_channel(self, server, channel):
		self.bot.server_settings_list[server.id]["welcome_channel"] = channel.id
		self.bot.save_server_settings()

	def set_welcome_messages(self, server, option):
		self.bot.server_settings_list[server.id]["welcome_messages"] = option
		self.bot.save_server_settings()

	async def say_welcome_channel(self, server, msg):
		welcome_channel = self.bot.server_settings_list[server.id]["welcome_channel"]
		if welcome_channel:
			try:
				await self.bot.send_message(self.bot.get_channel(welcome_channel), msg)
			except (discord.Forbidden, discord.NotFound, discord.InvalidArgument):
				await self.bot.send_message(server.default_channel, msg)
		else:
			await self.bot.send_message(server.default_channel, msg)

	async def on_member_join(self, member):
		serv = member.server
		if self.bot.server_settings_list[serv.id]["welcome_messages"]:
			await self.say_welcome_channel(serv, "%s has joined the server. Welcome!" % member.mention)

	@commands.command(pass_context = True, no_pm = True)
	async def welcomechannel(self, ctx, argument = None):
		"""Sets the channel for posting welcome messages.

		When used without an argument, uses the current channel. Otherwise, accepts a channel mention, a channel name, or a channel ID."""
		server = ctx.message.server # As no_pm is true here, I am assuming server cannot be None
		if not argument:
			chsetting = self.bot.get_channel(self.welcome_channel(server))
			channel = server.default_channel if chsetting is None else chsetting
			await self.bot.say("%s is currently the designated channel for welcome messages." % channel.mention)
		else:
			author = ctx.message.author
			if self.bot.is_owner(author) or self.bot.is_admin(author):
				for ch in server.channels:
					if ch.mention == argument or ch.name == argument or ch.id == argument:
						if ch.type == discord.ChannelType.text:
							self.set_welcome_channel(server, ch)
							await self.bot.say("%s is now the designated channel for welcome messages." % ch.mention)
							return
						else:
							await self.bot.say("That channel cannot be used for such purposes.")
							return
				await self.bot.say("Alas, I know of no such channel.")
			else:
				await self.bot.say("You have not the authority to issue such a command.")

	@commands.command(pass_context = True, no_pm = True)
	async def welcome(self, ctx, argument = None):
		"""Turns the welcome messages on or off.

		When used without an argument, shows current setting. Use "off", "no", or "false" to turn welcome messages off. Anything else turns it on."""
		server = ctx.message.server
		if not argument:
			wmstate = "enabled" if self.welcome_messages(server) else "disabled"
			await self.bot.say("Welcome messages are currently %s." % wmstate)
		else:
			author = ctx.message.author
			if self.bot.is_owner(author) or self.bot.is_admin(author):
				if argument == "off" or argument == "no" or argument == "false":
					self.set_welcome_messages(server, False)
					await self.bot.say("Welcome messages are now disabled.")
				else:
					self.set_welcome_messages(server, True)
					await self.bot.say("Welcome messages are now enabled.")
			else:
				await self.bot.say("You have not the authority to issue such a command.")

	@commands.command()
	async def changename(self):
		"""Chooses a random new nickname for the bot."""
		await self.bot.say("Too long have I endured this moniker. It is time to begin anew.")
		await self.set_nick(self.choose_nick())

	@commands.command()
	async def join(self):
		"""Displays a link where server owners can add this bot."""
		await self.bot.say("Another server? I am but a simple servant. %s" % self.bot.joinurl)

def setup(bot):
	general = General(bot)
	bot.add_cog(general)
	bot.loop.create_task(general.change_nick())
