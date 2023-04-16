import os
from discordbot.bot import ClientApp

TOKEN = os.environ.get('DISCORD_BOSONS_TESTS')
CLIENT_ID = client_id
GUILD_ID = GUILD_ID

bot = ClientApp(TOKEN, CLIENT_ID)

@bot.event('READY')
async def on_ready(bot):
    print("Bot online!")
    #register the commands on a server
    await bot.sync_with_guild(GUILD_ID)
    #sync global commands
	#await bot.sync_global_commands()

@bot.slash_command(name="hello", description="Send hello!")
async def hello(ctx):
    await ctx.defer(ephemeral=False)
    await ctx.send(content="Hello!")

if __name__ == "__main__":
    bot.run()
