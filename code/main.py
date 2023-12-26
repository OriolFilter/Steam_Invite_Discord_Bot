import asyncio

from CustomBot import CustomBot, middleware

import HealthCheck
from aiohttp import web


async def run(bot: CustomBot, runner: web.AppRunner):
    """
    Starts the Hatcheck API server and passes the Web runner for async to do its thingies, passes the packed app.

    Starts the Discord Bot service/process
    """

    await HealthCheck.start_web(runner=runner, config=middleware.Configuration.healtcheck)
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

    app = web.Application()
    app.add_routes([web.get('/', handler.handle_healthcheck)])
    runner = web.AppRunner(app)

    asyncio.run(run(bot=bot, runner=runner))


if __name__ == '__main__':
    start()
