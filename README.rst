discord.bot
==========

.. image:: https://discord.com/api/guilds/336642139381301249/embed.png
   :target: https://discord.gg/r3sSKJJ
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/discord.py.svg
   :target: https://pypi.python.org/pypi/discord.py
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/discord.py.svg
   :target: https://pypi.python.org/pypi/discord.py
   :alt: PyPI supported Python versions

This is a Python-based API wrapper for Discord that is modern, user-friendly, packed with features, and designed to be async-ready. It provides a comprehensive and intuitive way to interact with Discord's API and build applications such as bots, integrations, and other tools.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.

Installing
----------

**Python 3.9 or higher is required**

To install the library you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install git+https://github.com/BosonsHiggs/discord.bot

    # Windows
    py -3 -m pip install git+https://github.com/BosonsHiggs/discord.bot


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/BosonsHiggs/discord.bot
    $ cd discord.bot


Quick Example
--------------

.. code:: py

    import asyncio
    from discord.bot import MeuBot

    TOKEN = 'BOT TOKEN HERE'
    GUILD_ID = guild_id_here
    aplication_id = aplication_id

    async def hello_func(ctx):
        await ctx.send(content="Mensagem com botão:")

    async def main():
        async with MeuBot(TOKEN, aplication_id) as bot:
            hello_command = Command("hello", hello_func, "Respond with 'Hello, world!'")
            bot.add_command(hello_command)
            
            await bot.sync_with_guild(GUILD_ID)  # Sincroniza comandos de barra com o servidor

            await bot.connect()

    if __name__ == "__main__":
        asyncio.run(main())


You can find more examples in the examples directory.

Links
------

- `No links!`_