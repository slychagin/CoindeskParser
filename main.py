import os
import csv
import time
from typing import List
from dotenv import load_dotenv

import aiohttp
import asyncio
from aiohttp import ContentTypeError, ClientConnectorError
from aiohttp.web_exceptions import HTTPException

load_dotenv()

HOST: str = os.environ.get('HOST')
URL: str = os.environ.get('URL')
QUERY: str = os.environ.get('QUERY')
HEADERS: dict = {
    'User-Agent': os.environ.get('USERAGENT'),
    'Accept': os.environ.get('ACCEPT')
}
FILE: str = os.environ.get('FILE')


async def get_total_number() -> int:
    """
    Makes a request for the first page of the search results
    and pulls the total number of results.
    Every page has 'metadata' with 'total'=results number.
    """
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        try:
            async with session.get(URL + QUERY) as response:
                json_data = await response.json()
                number_per_page = len(json_data['items'])
                total_number = int(json_data['metadata']['total']) // number_per_page + 1
                return total_number
        except ContentTypeError:
            print('Check your URL!\nIt must be:\n'
                  'https://www.coi.com/pf/api/v3/content/fetch/search?query='
                  '{"search_query":"bitcoin","sort":0,"page":0,"filter_url":""}')
        except ClientConnectorError as e:
            print('Connection Error', str(e))
        except HTTPException as e:
            print(f'{e.status_code}\n{e.reason}\n{e.text}')


async def get_urls(pages_num: int) -> List[str]:
    """
    Create urls for all pages with news
    """
    urls_list = []
    for page_num in range(pages_num):
        query = QUERY.replace('"page":0', f'"page":{page_num}')
        url = URL + query
        urls_list.append(url)
    return urls_list


def save_data_to_csv(items: List, path: str) -> None:
    """
    Save all news to csv file. Save file in the current directory
    :param items: list of news that get in main async function
    :param path: file where to save the data
    :return: None
    """
    try:
        with open(path, 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['News Number', 'Title', 'Link', 'Date'])
            for number, item in enumerate(items):
                writer.writerow([number + 1, item['title'], HOST + item['link'], item['pubdate']])
    except PermissionError as e:
        print(f'{str(e)}\nThe data was not saved to a file.\n'
              f'Maybe the file is open or something else.')


async def user_input() -> int:
    """
    Asks the user how many pages to parse
    """
    pages_total = await get_total_number()

    while True:
        number = input(f'Enter the number of pages from 1 to {pages_total} to be parsed'
                       f' and press Enter:\n')
        try:
            correct_value = int(number)
            if 1 <= correct_value <= pages_total:
                return correct_value
            else:
                continue
        except ValueError:
            try:
                float(number)
                print("Input is an float number.")
            except ValueError:
                print("This is not a number. Please enter a valid number!")


async def main() -> None:
    """
     Asynchronously iterates through the list of links,
     fetches data by the items key and save it to csv file
    """
    data = []
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        try:
            pages_number = await user_input()
            urls = await get_urls(pages_number)
            print('Loading...')

            for i, url in enumerate(urls):
                async with session.get(url) as response:
                    news_data = await response.json()
                    data.extend(list(map(lambda x: x, news_data['items'])))

                    # This line can be added for a beautiful display in the console,
                    # but then the speed drops almost twice.
                    # print(f'Parse page {i + 1} from {len(urls)}')

        except ClientConnectorError as e:
            print('Connection Error', str(e))
        except HTTPException as e:
            print(f'{e.status_code}\n{e.reason}\n{e.text}')

    print(f'\nLoad {len(data)} news')

    # Save parsed data to csv file
    save_data_to_csv(data, FILE)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        start_time = time.perf_counter()
        loop.run_until_complete(main())
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Parse time: {total_time:.1f} seconds')
    except KeyboardInterrupt:
        pass
