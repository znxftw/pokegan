import logging
import os.path
import re
import shutil

import requests
import scrapy
from scrapy.http import TextResponse

base_file_path = os.path.dirname(__file__) + '\\..\\..\\images\\'


def process_image(path):
    prepend = "https://archives.bulbagarden.net/media/upload/thumb/"
    append = ".png"

    enlarged = path.replace("70px", "200px")
    full_url = prepend + enlarged + append

    image_name = re.search('200px-(.*).png', full_url, re.IGNORECASE).group(1)
    full_path = base_file_path + image_name + '.png'

    if os.path.exists(full_path):
        logging.info(f"Skipping download for {image_name}...")
        return

    response = requests.get(full_url, stream=True)
    with open(full_path, "wb") as f:
        shutil.copyfileobj(response.raw, f)
        logging.info(f"Completed download for {image_name}...")


class PokemonSpider(scrapy.Spider):
    name = "pokemon"

    start_urls = [
        'https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number'
    ]

    def parse(self, response: TextResponse, **kwargs):
        result = response.xpath('//img/@src').re(r'//archives.bulbagarden.net/media/upload/thumb/(.*).png')

        os.makedirs(base_file_path, exist_ok=True)

        image_urls = []
        for path in result:
            prepend = "https://archives.bulbagarden.net/media/upload/thumb/"
            append = ".png"

            enlarged = path.replace("70px", "200px")
            full_url = prepend + enlarged + append
            image_urls.append(full_url)

        image_item = ImageItem()
        image_item['file_urls'] = image_urls
        yield image_item


class ImageItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
