import asyncio
import json

import aiohttp
import requests


def parse_inv2(*args):  # TODO enable proxy
    resp = []
    for steam_id in args:
        url = 'http://steamcommunity.com/inventory/%s/730/2?l=english&count=5000' % steam_id
        resp.append(requests.get(url).json())

    return resp


def parse_inv(*args):
    loop = asyncio.get_event_loop()
    tasks = [get_inv(steam_id) for steam_id in args]

    future = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(future)

    return future.result()


async def get_inv(target_id):
    async with aiohttp.ClientSession() as session:
        url = 'http://steamcommunity.com/inventory/%s/730/2?l=english&count=5000' % target_id

        async with session.get(url) as resp:
            text = await resp.text()
            return json.loads(text)


if __name__ == '__main__':
    r = parse_inv(*['76561198244303924' for i in range(10)])
    print(type(r))
    for i in r:
        print(i)
