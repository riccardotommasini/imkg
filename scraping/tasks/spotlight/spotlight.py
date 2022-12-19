import asyncio
from time import time
import os

import aiohttp
import pymongo

MONGO_URI = os.getenv('MONGO_URI')
CALLS_PER_SECOND = os.getenv('CALLS_PER_SECOND', default=2)
if not MONGO_URI:
    raise RuntimeError("Missing environment variable")

BASE_URL = 'https://api.dbpedia-spotlight.org/en'
ENDPOINT_URL = f'{BASE_URL}/annotate'

mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_collection = mongo_client['persistent']['KnowYourMeme']


class SimpleLimiter:
    """
    The reasoning for this is that even though the requests are scheduled sequentially,
    they're executed asynchronously and the rate may exceed what is considered good-natured API usage.
    It is only sufficient for a single scheduler use-case.
    """

    def __init__(self, calls_per_second: float):
        self.delay = (1 / calls_per_second) if calls_per_second else None
        self.next = 0

    async def __aenter__(self):
        if not self.delay:
            return
        t = time()
        if t < self.next:
            await asyncio.sleep(self.next - t)
        self.next = time() + self.delay

    async def __aexit__(self, *_):
        pass



async def main():
    limiter = SimpleLimiter(CALLS_PER_SECOND)
    client = aiohttp.ClientSession()

    async def _fetch(_id, text):
        response = await client.get(ENDPOINT_URL,
                                    params={"text": text,  # more configuration?
                                            },
                                    headers={'Accept': 'application/json'}
                                    )
        data = await response.json()
        mongo_collection.update_one(_id, {"$set": {"spotlight": data, "last_update_text_entities": int(time())}})

    last = None
    for entry in mongo_collection.find(
            {"$expr": {"$gt": ["$last_update_text_entities", "$last_update_source"]}},
            {'content.about': 1}
    ):
        _id = entry['_id']
        text = entry['contet']['about']['text']
        if 'subsections' in entry['content']['about']:
            subsections = entry['content']['about']['subsections']
            for subsection in subsections:
                text.extend(subsections[subsection]['text'])
        text = " ".join(text)

        with limiter:
            last = asyncio.create_task(_fetch(_id, text))

    await last  # wait for the last one to finish before exiting
    await client.close()


asyncio.run(main())
