import os
from discordbot.bot import ClientApp

TOKEN = os.environ.get('DISCORD_BOSONS_TESTS')
CLIENT_ID = CLIENT_ID
GUILD_ID = GUILD_ID

bot = ClientApp(TOKEN, CLIENT_ID)

@bot.event('READY')
async def on_ready(bot):
    print("Bot online!")
    await bot.sync_with_guild(GUILD_ID)

@bot.slash_command(name="hello", description="Send hello!")
async def hello(ctx, name:str):
    await ctx.defer(ephemeral=False)
    await ctx.send(content=f"Hello to Discord.bot!")

if __name__ == "__main__":
    bot.run()
