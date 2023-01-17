import scrapy
from scrapy.http import TextResponse


class PokemonSpider(scrapy.Spider):
    name = "pokemon"

    def start_requests(self):
        urls = [
            'https://bulbapedia.bulbagarden.net/wiki/List_of_Pokémon_by_National_Pokédex_number'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: TextResponse, **kwargs):
        print(response.body)