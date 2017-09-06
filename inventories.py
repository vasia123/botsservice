import asyncio
import json

import aiohttp
import requests


#test
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
        proxies = {}
        async with session.get(url) as resp:
            text = await resp.text()
            page = json.loads(text)

            if page is None:
                return {'data': {
                    '440': {'message': 'HTTP error 404'},
                    '570': {'message': 'HTTP error 404'},
                    '730': {'message': 'HTTP error 404'},
                }}

            descriptions = {}
            for block in page['descriptions']:
                key = '%s_%s' % (block['classid'], block['instanceid'])

                descriptions[key] = {}

                descriptions[key]['icon_url'] = block['icon_url']
                descriptions[key]['market_name'] = block['market_name']
                descriptions[key]['name'] = block['name']
                descriptions[key]['tradable'] = block['tradable']
                if block.get('icon_url_large') is not None:
                    descriptions[key]['icon_url_large'] = block['icon_url_large']

                tags = {}
                for tag_category in block['tags']:
                    tags[tag_category['category']] = tag_category['localized_tag_name']

                descriptions[key]['type'] = tags['Type']
                descriptions[key]['quality'] = tags['Quality']
                descriptions[key]['rarity'] = tags['Rarity']
                if tags.get('Exterior') is not None:
                    descriptions[key]['exterior'] = tags['Exterior']

            items = {}
            for block in page['assets']:
                descriptions_key = '%s_%s' % (block['classid'], block['instanceid'])
                items_key = '%s_%s_%s' % (block['classid'], block['instanceid'], block['assetid'])

                items[items_key] = {
                    'classid': block['classid'],
                    'instanceid': block['instanceid'],
                    'assetid': block['assetid'],
                    'contextid': block['contextid'],
                    'amount': block['amount'],
                    'icon_url': descriptions[key]['icon_url'],
                    'market_name': descriptions[key]['market_name'],
                    'name': descriptions[key]['name'],
                    'tradable': descriptions[key]['tradable'],
                    'type': descriptions[key]['type'],
                    'quality': descriptions[key]['quality'],
                    'rarity': descriptions[key]['rarity'],
                }

                if descriptions[descriptions_key].get('icon_url_large') is not None:
                    items[items_key]['icon_url_large'] = descriptions[descriptions_key]['icon_url_large']
                if descriptions[descriptions_key].get('exterior') is not None:
                    items[items_key]['exterior'] = descriptions[descriptions_key]['exterior']

            return {'data': {
                '440': [],
                '570': [],
                '730': list(items.values())
            }}


if __name__ == '__main__':
    print(parse_inv('76561198244303924'))
    # r = parse_inv(*['76561198244303924' for i in range(10)])
    # print(type(r))
    # for i in r:
    #     print(i)
