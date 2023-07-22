import scrapy
import sqlite3
import json

class IchibankujiSpider(scrapy.Spider):
    name = 'IchibanKuji'
    allowed_domains = ['www.banpresto.jp']
    country_id = '04'
    start_urls = ['https://www.banpresto.jp/shop/'+ country_id+ '.json']


    def parse(self, response):
        # Load data from json file
        data = json.loads(response.body)
        kuji_data = data["kuji_master"]
        shop_data = data["shop_information"]
        # shop_area = data["shop_area"]


        # Load kuji information and store as json file called kujis.json
        with open('./static/kujis.json', 'w', newline = '') as jsonfile:
            jsonfile.write(json.dumps(kuji_data))


        # Load kuji info as list
        kujis = []
        for kuji in kuji_data:
            kujis.append((kuji["kuji_master_id"], kuji["kuji_master_name"]))
        # connect to sql library
        con = sqlite3.connect('./ichiban_kuji.db')
        cursor = con.cursor()
        cursor.execute("DELETE FROM kujis;")
        cursor.executemany("INSERT INTO kujis (kuji_id, kuji_name) VALUES (?, ?);", kujis)


        # Load shop information into sql database called ichiban_kujis.db with table shop_kuji and shops
        shop_kuji = []
        shops = []
        newest_shop_id = cursor.execute("SELECT shop_id FROM shops ORDER BY shop_id DESC LIMIT 1;").fetchone()[0]
        for shop in shop_data:
            if shop["shop_id"] > newest_shop_id:
                shops.append((shop["shop_id"], shop["shop_name"], shop["shop_address"], shop["area_id"], shop["shop_tel"]))
            for kujiID in shop["kuji_master_id"]:
                shop_kuji.append((shop["shop_id"], kujiID))
        cursor.execute("DELETE FROM shop_kuji;")
        cursor.executemany("INSERT INTO shop_kuji (shop_id, kuji_id) VALUES (?, ?)", shop_kuji)
        cursor.executemany("INSERT INTO shops (shop_id, shop_name, shop_address, area_id, shop_tel) VALUES (?, ?, ?, ?, ?)", shops)
        cursor.execute("DELETE FROM shops WHERE shop_address is NULL;")


        # Load city name and id into sql database called ichiban_kujis.db with table city
        # citys = []
        # for city in shop_area:
        #     citys.append((city["area_id"], city["area_name"]))
        # cursor.executemany("INSERT INTO city (city_id, city_name) VALUES (?, ?)", citys)
        
        con.commit()
        con.close()
