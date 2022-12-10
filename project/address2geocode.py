import sqlite3
import csv

con = sqlite3.connect('./static/ichiban_kuji.db')
cursor = con.cursor()
with open('./static/Address_Finish.csv', 'r', newline = '') as csvfile:
    rows = csv.reader(csvfile)
    header = next(rows)
    for row in rows:
        id = '0'+row[0]
        lat = row[3]
        lon = row[4]
        # print(id+' '+lat+' '+lon)

        cursor.execute("UPDATE shops SET lat = ?, lon = ? WHERE shop_id = ?;", (lat, lon, id))
    con.commit()
    con.close()