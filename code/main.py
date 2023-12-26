import asyncio

from CustomBot import CustomBot, middleware

from HealthCheck import HealthcheckHandler


async def main():
    """
    Inits Discord Bot

    Inits HealthcheckHandler, passes as arguments configuration and the discord bot.

    Starts Web server and Discord Server
    """
    bot = CustomBot()
    handler = HealthcheckHandler(configuration=middleware.Configuration.healtcheck, discord_bot=bot)

    await handler.start_web()
    await bot.run()
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())
