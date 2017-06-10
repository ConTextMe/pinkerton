from aiohttp import ClientSession
from pinkerton.settings import DATA_PROVIDER_CLIENT_HEADERS


class BaseDataProvider:

    ALLOWED_ENTITY_TYPES = []

    @property
    def session(self):
        return ClientSession(headers=DATA_PROVIDER_CLIENT_HEADERS)

    async def search(self, query: str) -> list:
        '''
        Query method takes an entity (in most cases: string) and returns list
        of matches from external knowlegde database, like Wikipedia.org
        '''
        raise NotImplementedError

    def accepts(self, entity: object) -> bool:
        '''
        Returns true if data provider can return information about given entity
        '''
        entity_type = (
            getattr(entity, 'type', None) or entity.get('type', None)
        )
        return entity_type in self.ALLOWED_ENTITY_TYPES
