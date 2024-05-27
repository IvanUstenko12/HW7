import asyncio 
import aiohttp
import aiofiles
from lxml import html
import requests
from bs4 import BeautifulSoup

links_0 = ['https://regex101.com/',
    'https://docs.python.org/3/this-url-will-404.html',
    'https://www.nytimes.com/guides/',
    'https://www.mediamatters.org/',
    'https://1.1.1.1/',
    'https://www.politico.com/tipsheets/morning-money',
    'https://www.bloomberg.com/markets/economics',
    'https://www.ietf.org/rfc/rfc2616.txt']
urls = []

async def get_code(session, url):
    async with session.get(url) as response:  
        if response.status == 200:
            return await response.text() 

async def find_links(code):
    soup = BeautifulSoup(code, 'html.parser') 
    links = []
    for a in soup.find_all('a', href = True):
        if 'http' in a.get('href'):
            links.append(a.get('href') + '\n')

    return links

async def get_links(session, link):
    code = await get_code(session, link)
    links = await find_links(code)
    for i in links:
        urls.append(i)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in links_0:
            task = asyncio.create_task(get_links(session, link))
            tasks.append(task)
        await asyncio.gather(*tasks)

async def write_urls(file_name, urls):
    async with aiofiles.open(file_name, 'w') as f:
        await f.writelines(urls)


asyncio.run(main())
asyncio.run(write_urls('urls.txt', urls))



