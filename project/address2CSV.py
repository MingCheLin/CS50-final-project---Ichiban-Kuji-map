import csv
import sqlite3

con = sqlite3.connect('./static/ichiban_kuji.db')
cursor = con.cursor()
cursor.execute('SELECT shop_id, shop_address FROM shops')


with open("address.csv", "w", newline="", encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'Address', 'Response_Address', 'Response_X', 'Response_Y'])
    for row in cursor:
        writer.writerow([row[0], row[1]])