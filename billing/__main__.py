import asyncio

from aiohttp import web

from billing.config import settings

__all__ = [
    'app'
]

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)




loop = asyncio.get_event_loop()

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])
print('Starting application... \nLog level {}'.format(settings.LOGGING_LEVEL))

web.run_app(app, host='0.0.0.0', port=8000)