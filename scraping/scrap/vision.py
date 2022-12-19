import asyncio
import json
import os
import threading
from queue import Queue
import time

from google.protobuf.json_format import MessageToDict
from google.cloud import vision
import aiohttp

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY')
PROXY = proxy = f'http://scraperapi:{SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001'
if not SCRAPER_API_KEY:
    raise RuntimeError("Missing environment variables")

DEFAULT_MAX = 1000  # no limit seems to be enforced, however the return count for each feature is <= limit
features = [  # perhaps set in some configuration?
    vision.Feature(type_=type_, max_results=max_) for type_, max_ in [
        # (1, DEFAULT_MAX),   # face detection
        # (2, DEFAULT_MAX),   # landmark detection
        # (3, DEFAULT_MAX),   # logo detection
        (4, DEFAULT_MAX),  # label detection
        # (5, DEFAULT_MAX),  # text detection
        (6, DEFAULT_MAX),   # safe search detection
        # (7, DEFAULT_MAX),   # image properties
        # (9, DEFAULT_MAX),   # crop hints
        (10, DEFAULT_MAX),  # web detection
        # (11, DEFAULT_MAX),  # document text detection
        # (12, DEFAULT_MAX),  # product search
        # (19, DEFAULT_MAX)  # object localization
    ]
]

write_queue = Queue()

vision_client = vision.ImageAnnotatorClient()

stats = {'writes': 0, 'images_read': 0, 'batch_requests_sent': 0, 'batch_requests_done': 0, 'images_queued': 0, 'fetches_live': 0, 'current_batch': 0,
         'skipped': 0, 'failing': 0}

def to_file():
    with open("kym_vision5.json", 'a', encoding='utf8') as f:
        f.write("{\n")
        while True:
            data = write_queue.get()
            if data is None:
                break
            f.write(f"\"{data[0]}\": {json.dumps(data[1], ensure_ascii=False)},\n")
            stats['writes'] += 1
        f.write("}")

def images():
    with open('kym_vision3.json', encoding='utf8') as f:
        keys = json.load(f).keys()
    with open('KYM.json', encoding='utf8') as f:
        kym = json.load(f)
        print("kym length:",len(kym))
        print("vision length:", len(keys))
        for entry in kym:
            if entry['url'] in keys:
                stats['skipped'] += 1
                continue
            yield entry['url'], entry['template_image_url']
            stats['images_read'] += 1


def annotate_batch(batch):
    batch_request = vision.BatchAnnotateImagesRequest(requests=[
        vision.AnnotateImageRequest(image=vision.Image(content=data[1]), features=features)
        for data in batch
    ])
    stats['batch_requests_sent'] += 1
    batch_response = vision_client.batch_annotate_images(batch_request)
    for _id, annotation in zip((i[0] for i in batch), batch_response.responses):
        write_queue.put((_id, MessageToDict(annotation._pb)))
    stats['batch_requests_done'] += 1

async def batch_maker(image_queue):
    batch = []
    batch_size = 0
    coros = []
    while True:
        _id, image = await image_queue.get()
        if len(batch) == 16 or batch_size + len(image) * 1.4 > 1e7 or not image:
            coros.append(asyncio.create_task(asyncio.to_thread(annotate_batch, batch)))
            stats['current_batch'] = 0
            batch = []
        if (_id, image) == (None, None):
            break
        if image:
            stats['current_batch'] += 1
            batch.append((_id, image))
    await asyncio.gather(coros)

async def printer():
    while True:
        msg = '\t'.join(f"{key}:\t{value}" for key, value in stats.items())
        print(f"\r{msg}", end='')
        await asyncio.sleep(1)

async def main():
    semaphore = asyncio.Semaphore(10)  # scraperapi concurrency limit
    image_queue = asyncio.Queue()
    _batch_maker = asyncio.create_task(batch_maker(image_queue))
    _to_file = asyncio.create_task(asyncio.to_thread(to_file))
    _printer = asyncio.create_task(printer())

    client = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

    async def _fetch(_id, img_url):
        failing = False
        try:
            for _ in range(5):
                stats['fetches_live'] += 1
                resp = await client.get(img_url, proxy=PROXY)
                stats['fetches_live'] -= 1
                if resp.status == 200:
                    await image_queue.put((_id, await resp.read()))
                    stats['images_queued'] += 1
                    if failing:
                        stats['failing'] -= 1
                    break
                elif resp.status == 403:
                    if failing:
                        stats['failing'] -= 1
                    break
                else:
                    failing = True
                    print(resp)
                    stats['failing'] += 1
            else:
                print("FAILED:", img_url)
                stats['failing'] -= 1
        except:
            pass
        semaphore.release()

    coros = []
    for _id, img_url in images():
        await semaphore.acquire()
        coros.append(asyncio.create_task(_fetch(_id, img_url)))
    print("all queued")
    await asyncio.gather(coros)
    print("gathered")
    await image_queue.put((None, None))
    print("poisoned")
    await image_queue.join()
    print("dead")
    await _batch_maker
    print("batches done")
    write_queue.put(None)
    print("poisoned")
    await _to_file
    print("dead")
    _printer.cancel()
    print("printind gone")
    await client.close()
    print("client closed")


asyncio.run(main())
