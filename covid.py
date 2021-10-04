import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def weather_request():
    async with aiohttp.ClientSession() as session:
        url = "https://стопкоронавирус.рф/information/"
        async with session.get(url, ssl=False) as response:
            response = await response.text() if response.status == 200 else f'Cannot connect to host: {url}'
            root = BeautifulSoup(response, 'html.parser')
            stats = root.select_one('cv-stats-virus')
            spread = root.select_one('cv-spread-overview')

            daily = json.loads(stats[':stats-data'])
            data = json.loads(spread[':spread-data'])

            regions = {}
            for row in data:
                regions[row['title']] = row['sick_incr']

            day = daily["sickChange"]
            total = daily["sick"]
            reg = regions["Краснодарский край"]  # Enter yours region name here

            covid = f'Прирост за день:\n{day}\nОбщее число заражений:\n{total}\nВ Краснодарском крае:\n{reg}'

            print(covid)
            return covid

loop = asyncio.get_event_loop()
loop.run_until_complete(weather_request())
