import asyncio, aiohttp

loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)

async def getResponse(url, **kwargs):
    async with session.get(url, **kwargs) as response:
        return await response.json()

def formatUrl(endpoint):
    return 'https://api.scryfall.com{}'.format(endpoint)

card = loop.run_until_complete(getResponse(url=formatUrl('/cards/named?'), params={'fuzzy':'black lotus'}))

print(card)

session.close()
loop.close()
