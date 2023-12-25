# from http.server import BaseHTTPRequestHandler, HTTPServer
# from CustomBot import CustomBot
# from Classes import HealthCheckConf
#
#
#
# class MyServer(BaseHTTPRequestHandler):
#     __discord_bot: CustomBot
#     __configuration: HealthCheckConf
#
#     # def __init__(self, *args, **kwargs):
#     # def __init__(self, configuration: HealthCheckConf, discord_bot: CustomBot, *args, **kwargs):/
#     #     super(BaseHTTPRequestHandler, self).__init__(*args, **kwargs)
#         # self.configuration = configuration
#         # self.__discord_bot = discord_bot
#
#     @property
#     def is_bot_running(self) -> bool:
#         return not True
#         # return not self.__discord_bot.is_closed()
#
#     def do_GET(self):
#         status_code = [503, 200][self.is_bot_running]
#         message = ["Service Unavailable", "OK"][self.is_bot_running]
#
#
#         self.send_response(status_code)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(bytes("<html><head><title>Healthcheck</title></head>", "utf-8"))
#         self.wfile.write(bytes("<body>", "utf-8"))
#         self.wfile.write(bytes(f"<p>{status_code}: {message}</p>", "utf-8"))
#         self.wfile.write(bytes("</body></html>", "utf-8"))
#
#     async def _start(self):
#         hostName = "localhost"
#         serverPort = 8080
#         webServer = HTTPServer((hostName, serverPort), self)
#         print("Server started http://%s:%s" % (hostName, serverPort))
#         webServer.serve_forever()
#
#     async def start(self):
#         await self._start()
