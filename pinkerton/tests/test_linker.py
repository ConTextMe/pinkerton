import pytest

from pinkerton.linker import EntityLinker
from pinkerton.extractor import EntityExtractor
from pinkerton.similarity import LDASimilarity
from pinkerton.providers import WikipediaProvider 


@pytest.fixture
def history_text():
    return '''
    Иван Васильевич, царь всея руси, по историческим данным, был тираном
    '''


@pytest.fixture
def linker():
    return EntityLinker(
        extractor=EntityExtractor(
            api_base_url='https://natasha.b-labs.pro/api/'
        ),
        comparator=LDASimilarity(),
        providers=[
            WikipediaProvider(),
        ],
    )


@pytest.mark.asyncio
async def test_link_person(linker, history_text):
    async for obj, entities in linker.process(history_text):
        assert obj['fields']['firstname'] == 'Иван'
        assert obj['fields']['middlename'] == 'Василиевич'

        entity, score = entities[0]

        assert entity['title'] == 'Иван Грозный'
        assert entity['source'] == 'https://ru.wikipedia.org/wiki/%D0%98%D0%B2%D0%B0%D0%BD_%D0%93%D1%80%D0%BE%D0%B7%D0%BD%D1%8B%D0%B9'
