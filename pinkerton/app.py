from aiohttp import web

from pinkerton import views
from pinkerton.linker import EntityLinker
from pinkerton.similarity import LDASimilarity
from pinkerton.extractor import EntityExtractor
from pinkerton.providers import WikipediaProvider, YandexMapsProvider


app = web.Application()

'''
Entity linking setup
'''
app.linker = EntityLinker(
    extractor=EntityExtractor(
        api_base_url='https://natasha.b-labs.pro/api/',
    ),
    comparator=LDASimilarity(),
    providers=[
        WikipediaProvider(),
        YandexMapsProvider(),
    ],
)


'''
Routes setup
'''

app.router.add_get('/version', views.version)
app.router.add_post('/annotate', views.annotate)
