#! /usr/local/bin/python3

import asyncio
from queue import Queue
from time import time
from collections import Counter
import os
import json

import aiohttp

CALLS_PER_SECOND = os.getenv('CALLS_PER_SECOND', default=10)

FILENAME = os.getenv('FILENAME', default=0)

BASE_URL = 'https://api.dbpedia-spotlight.org/en'
ENDPOINT_URL = f'{BASE_URL}/annotate'

write_queue = Queue()

stats = Counter()

class SimpleLimiter:
    """
    The reasoning for this is that even though the requests are scheduled sequentially,
    they're executed asynchronously and the rate may exceed what is considered good-natured API usage.
    It is only sufficient for a single scheduler use-case.
    """

    def __init__(self, calls_per_second: float):
        self.next = 0
        self.delay = (1 / int(calls_per_second)) if int(calls_per_second) else None
        
    async def __aenter__(self):
        if not self.delay:
            return
        t = time()
        if t < self.next:
            await asyncio.sleep(self.next - t)
        self.next = time() + self.delay

    async def __aexit__(self, *_):
        pass

def to_file():
    with open("retryed.json", "a", encoding='utf8') as f:
        f.write("{\n")
        while True:
            data = write_queue.get()
            if data is None:
                break
            f.write(f"\"{data[0]}\": {json.dumps(data[1], ensure_ascii=False)},\n")
            stats['written'] += 1
        f.write("}")


def texts():
    with open('retry.json', 'r', encoding='utf8') as f:
        for item in json.load(f):
            url = item['URL']
            text = item['alt_text']
            if(text):
                text = text.replace('|',"")
            stats['texts_read'] += 1
            yield url, text


async def printer():
    while True:
        msg = '\t'.join(f"{key}:\t{value}" for key, value in stats.items())
        print(f"\r{msg}", end='')
        await asyncio.sleep(1)



async def main():
    print(str(FILENAME))
    print(str(CALLS_PER_SECOND))
    
    limiter = SimpleLimiter(CALLS_PER_SECOND)
    client = aiohttp.ClientSession()

    _to_file = asyncio.create_task(asyncio.to_thread(to_file))
    _printer = asyncio.create_task(printer())
    
    async def _fetch(url, text):
        stats['requests'] += 1
        for _ in range(5):
            response = await client.get(ENDPOINT_URL,
                                        params={"text": text,  # more configuration?
                                                'confidence': 0.5
                                                },
                                        headers={'Accept': 'application/json'}
                                        )
            if response.status == 200:
                write_queue.put((url, await response.json()))
                break
        else:
            print("\nFAILED:", url)
            stats['failed'] += 1
        stats['requests'] -= 1

    coros = []
    for url, text in texts():
        async with limiter:
            coros.append(asyncio.create_task(_fetch(url, text)))

    print("\nall done")
    await asyncio.gather(coros)
    print("\ngathered")
    write_queue.put(None)
    print("\npoisoned")
    await _to_file
    print("\nwriter done")
    _printer.cancel()
    print("\nprinter canceled")
    await client.close()


asyncio.run(main())
