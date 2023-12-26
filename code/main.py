import asyncio

from CustomBot import CustomBot, middleware

import HealthCheck
from aiohttp import web


async def run(bot: CustomBot, handler: HealthCheck.HealthcheckHandler):
    """
    Starts the Hatcheck API server and passes the Web runner for async to do its thingies, passes the packed app.

    Starts the Discord Bot service/process
    """

    await HealthCheck.start_web(handler=handler)
    await bot.run()
    await asyncio.Event().wait()


def start():
    """
    Inits Discord Bot
    Inits HealthcheckHandler (aka the class that will handle HTTP requests for the Discord "API" web server)

    Inits the Web Server and configures it to use the handler, afterward packs the app.
    """
    bot = CustomBot()
    handler = HealthCheck.HealthcheckHandler(configuration=middleware.Configuration.healtcheck, discord_bot=bot)

    asyncio.run(run(bot=bot, handler=handler))


if __name__ == '__main__':
    start()
