from operator import itemgetter


class EntityLinker:

    def __init__(self, extractor, comparator, providers):
        self.extractor = extractor
        self.comparator = comparator
        self.providers = providers

    async def lookup(self, obj: dict, context: str) -> list:
        providers = (p for p in self.providers if p.accepts(obj))
        for span in obj['spans']:
            query = span['normalized']  # TODO:
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
                    
