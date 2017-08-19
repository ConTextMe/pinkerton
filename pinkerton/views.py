from aiohttp import web

from pinkerton.settings import (
    PROJECT_VERSION,
    MAX_ENTITIES_PER_OBJECT,
)
from pinkerton.utils import serialize_object


async def version(request):
    return web.json_response(data={
        'version': PROJECT_VERSION,
    })


async def annotate(request):
    form = await request.post()
    entities = [
        (serialize_object(obj), entities[:MAX_ENTITIES_PER_OBJECT])
        async for (obj, entities) in request.app.linker.process(form['text'])
    ]
    return web.json_response(data=entities)
