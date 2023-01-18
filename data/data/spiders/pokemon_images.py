import multiprocessing
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

    response = requests.get(full_url, stream=True)
    image_name = re.search('200px-(.*).png', full_url, re.IGNORECASE).group(1)

    with open(base_file_path + image_name + '.png', "wb") as f:
        shutil.copyfileobj(response.raw, f)


class PokemonSpider(scrapy.Spider):
    name = "pokemon"

    def start_requests(self):
        urls = [
            'https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs):
        result = response.xpath('//img/@src').re(r'//archives.bulbagarden.net/media/upload/thumb/(.*).png')

        os.makedirs(base_file_path, exist_ok=True)

        with multiprocessing.Pool() as pool:
            pool.map(process_image, result)
