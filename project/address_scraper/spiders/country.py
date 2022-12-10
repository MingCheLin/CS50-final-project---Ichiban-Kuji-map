import scrapy
import sqlite3
import json

class CountrySpider(scrapy.Spider):
    name = 'country'
    allowed_domains = ['www.banpresto.jp']
    start_urls = ['https://www.banpresto.jp/shop/country.json']

    def parse(self, response):

        data = json.loads(response.body)
        data = data['country']
        countries = []
        for country in data:
            countries.append((country['country_id'], country['country_name']))
        # for i in countries:
        #     print(i)

        connection = sqlite3.connect('countryID.db')
        cursor = connection.cursor()
        cursor.executemany("INSERT INTO country (id, name) VALUES (?, ?)", countries)
        # cursor.execute("SELECT id FROM country")
        connection.commit()
        connection.close()
