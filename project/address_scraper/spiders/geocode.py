import scrapy
import sqlite3

class GeocodeSpider(scrapy.Spider):
    name = 'geocode'
    allowed_domains = ['map.tgos.tw/TGOSCloud/Web/Map/TGOSViewer_Map']


    def start_requests(self):
        con = sqlite3.connect('./static/ichiban_kuji.db')
        cursor = con.cursor()
        addresses = cursor.execute("SELECT shop_id, shop_address FROM shops WHERE lat is NULL;").fetchall()
        start_urls = []
        for address in addresses:
            start_urls.append('https://map.tgos.tw/TGOSCloud/Web/Map/TGOSViewer_Map.aspx?addr='+ address[0])
        for add in start_urls:
            yield scrapy.Request(add,callback=self.parse)

    def parse(self, response):
        lon = response.xpath('//div[@id="LocateBox_FunctionWork_Coord_Work_WGS84"]/div/input[@id="LocateBox_FunctionWork_Coord_Work_WGS84_lng"]/@value').get(default='not')
        lat = response.xpath('//div[@id="LocateBox_FunctionWork_Coord_Work_WGS84"]/div/input[@id="LocateBox_FunctionWork_Coord_Work_WGS84_lat"]/@value').get(default='not')
        con = sqlite3.connect('./static/ichiban_kuji.db')
        cursor = con.cursor()
        shop_id = cursor.execute("SELECT shop_id FROM shops WHERE lat is NULL LIMIT 1;").fetchall()[0]
        data = (lat, lon, shop_id)
        cursor.execute("UPDATE shops SET lat=?, lon=? WHERE shop_id=?", data)
        con.commit()
        con.close()
