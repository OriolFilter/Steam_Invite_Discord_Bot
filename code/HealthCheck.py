from aiohttp import web
from Classes import HealthCheckConf
from CustomBot import CustomBot


class HealthcheckHandler:
    __discord_bot: CustomBot
    __configuration: HealthCheckConf

    def __init__(self, configuration, discord_bot):
        self.__configuration: HealthCheckConf = configuration
        self.__discord_bot: CustomBot = discord_bot

    @property
    def is_bot_running(self) -> bool:
        return not self.__discord_bot.is_closed()

    async def handle_healthcheck(self, request):
        status_code = [503, 200][self.is_bot_running]
        data = {'status_code': status_code}
        return web.json_response(data, status=status_code)


def run(configuration: HealthCheckConf, discord_bot: CustomBot):
    app = web.Application()
    handler = HealthcheckHandler(configuration=configuration, discord_bot=discord_bot)
    app.add_routes([web.get('/', handler.handle_healthcheck)])
    web.run_app(app, port=configuration.port)
