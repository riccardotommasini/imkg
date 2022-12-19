import asyncio
import os

from google.protobuf.json_format import MessageToDict
from google.cloud import vision
import aiohttp
import pymongo

MONGO_URI = os.getenv('MONGO_URI')
SCRAPER_API_KEY = os.getenv('SCRAPER_API_KEY')
PROXY = proxy = f'http://scraperapi:{SCRAPER_API_KEY}@proxy-server.scraperapi.com:8001'
if not (MONGO_URI and SCRAPER_API_KEY):
    raise RuntimeError("Missing environment variables")

DEFAULT_MAX = 1000  # no limit seems to be enforced, however the return count for each feature is <= limit
features = [  # perhaps set in some configuration?
    vision.Feature(type_=type_, max_results=max_) for type_, max_ in [
        # (1, DEFAULT_MAX),   # face detection
        # (2, DEFAULT_MAX),   # landmark detection
        # (3, DEFAULT_MAX),   # logo detection
        (4, DEFAULT_MAX),  # label detection
        (5, DEFAULT_MAX),  # text detection
        # (6, DEFAULT_MAX),   # safe search detection
        # (7, DEFAULT_MAX),   # image properties
        # (9, DEFAULT_MAX),   # crop hints
        (10, DEFAULT_MAX),  # web detection
        # (11, DEFAULT_MAX),  # document text detection
        # (12, DEFAULT_MAX),  # product search
        (19, DEFAULT_MAX)  # object localization
    ]
]

mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_collection = mongo_client['persistent']['KnowYourMeme']
vision_client = vision.ImageAnnotatorClient()


def annotate_batch(batch):
    batch_request = vision.BatchAnnotateImagesRequest(requests=[
        vision.AnnotateImageRequest(image=vision.Image(content=data[1]), features=features)
        for data in batch
    ])
    batch_response = vision_client.batch_annotate_images(batch_request)
    for _id, annotation in zip((i[0] for i in batch), batch_response.responses):
        mongo_collection.update_one({"_id": _id}, {"$set": {'template_annotation': MessageToDict(annotation._pb)}})


async def batch_maker(image_queue):
    batch = []
    batch_size = 0
    last = None
    while True:
        _id, image = await image_queue.get()
        if len(batch) == 16 or batch_size + len(image) * 1.4 > 1e7 or not image:
            last = asyncio.to_thread(annotate_batch(batch))
            batch = []
        if not image:
            break
        batch.append((_id, image))
    if last:
        await last


async def main():
    semaphore = asyncio.Semaphore(10)  # scraperapi concurrency limit
    image_queue = asyncio.Queue()
    _batch_maker = asyncio.create_task(batch_maker(image_queue))
    client = aiohttp.ClientSession()

    async def _fetch(_id, img_url):
        resp = await client.get(img_url, proxy=PROXY)
        semaphore.release()
        if resp.status == 200:
            await image_queue.put((_id, await resp.read()))

    last = None
    for entry in mongo_collection.find({'template_annotation': {'$exists': False}}, {'template_image_url': 1}):
        _id = entry['_id']
        img_url = entry['template_image_url']
        await semaphore.acquire()
        last = asyncio.create_task(_fetch(_id, img_url))

    if last:
        await last
    await image_queue.put((None, None))
    await image_queue.join()
    await _batch_maker
    await client.close()


asyncio.run(main())
