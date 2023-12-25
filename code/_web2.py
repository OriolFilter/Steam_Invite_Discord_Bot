# Proof of concept
from aiohttp import web
from datetime import datetime
from Classes import HealthCheckConf


class Handler:
    t: object

    def __init__(self, t):
        self.t = t

    async def handle_healthcheck(self, request):
        return web.Response(text=f"x={self.t.x}",status=503)

    async def handle_greeting(self, request):
        name = request.match_info.get('name', "Anonymous")
        txt = "Hello, {}".format(name)
        response = 404
        print(f'response={response}')
        # return web.Response(status='503')
        return web.Response(status=int(response))
        # return web.Response(text=txt,status=503)


def run(t):
    # def run(healthcheck_config:HealthCheckConf,discord_bot:CustomBot):
    app = web.Application()
    handler = Handler(t=t)
    app.add_routes([web.get('/', handler.handle_healthcheck)])
    web.run_app(app)
