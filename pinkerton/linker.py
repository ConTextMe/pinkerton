from operator import itemgetter

from pinkerton.base import EntityType


class EntityLinker:

    '''
    Entity linker is a layer between objects extractor and data providers
    '''

    def __init__(self, extractor, comparator, providers):
        self.extractor = extractor
        self.comparator = comparator
        self.providers = providers

    def get_queryset(self, obj: dict) -> set:
        '''
        Returns list of strings, that can be used in search with data providers
        '''
        type = obj['type']
        fields = obj['fields']

        # default queryset is normalized forms of all entity spans
        queryset = set(
            span['normalized'] for span in obj['spans']
        )

        if type == EntityType.Person:
            # add person-specific search queries to queryset
            # mostly because a lot of wiki articles have titles
            # in different form (like, Lastname_Firstname and Firstname_Lastname)
            firstname, lastname = (
                fields.get('firstname', None),
                fields.get('lastname', None),
            )
            if firstname and lastname:
                queryset |= {
                    ' '.join((firstname, lastname)),
                    ' '.join((lastname, firstname))
                }

        return queryset

    async def lookup(self, obj: dict, context: str) -> list:
        '''
        Returns all search results from data providers as generator
        '''
        providers = (p for p in self.providers if p.accepts(obj))
        for query in self.get_queryset(obj):
            for provider in providers:
                entities = await provider.search(query=query)
                for match in self.comparator.score(entities, context=context):
                    yield match

    async def process(self, text: str) -> list:
        objects, spans = await self.extractor.extract(text)
        for obj in objects:
            yield obj, sorted(
                [
                    match async for match in self.lookup(obj, context=text)
                ],
                key=itemgetter(1),
                reverse=True,
            )
