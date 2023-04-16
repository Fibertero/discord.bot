import os
from discordbot.bot import ClientApp

TOKEN = os.environ.get('DISCORD_BOSONS_TESTS')
CLIENT_ID = 1025801029566070824
GUILD_ID = 898335285719470080

bot = ClientApp(TOKEN, CLIENT_ID)

@bot.event('READY')
async def on_ready(bot):
    print("Bot online!")
    await bot.sync_with_guild(GUILD_ID)

@bot.slash_command(name="hello", description="Send hello!")
async def hello(ctx, name:str):
    await ctx.defer(ephemeral=False)
    await ctx.send(content=f"Hello, {name}!")

if __name__ == "__main__":
    bot.run()