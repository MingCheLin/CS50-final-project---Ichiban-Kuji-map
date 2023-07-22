import os
import time
from flask import Flask, flash, redirect, render_template, request, jsonify
import sqlite3
import json


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# make sure no cache and web update after immediate
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

## reserve to add more service
@app.route("/")
def index():
    return render_template("map.html")

## main map app
@app.route("/map", methods=["GET", "POST"])
def map():
    if request.method == "POST":
        ## use SQLite database
        con = sqlite3.connect('./ichiban_kuji.db')
        cur = con.cursor()
        ## receive POST from searchbar
        kuji_name = request.form.get("search")
        kuji_id = cur.execute("SELECT kuji_id FROM kujis WHERE kuji_name like ?", ('%'+ kuji_name +'%',))       # search certain kuji in DB
        ## try to get kuji id if the kuji exist
        try:
            kuji_id = kuji_id.fetchall()[0]
        except:
            return render_template("map.html")
        ## search the shops'id that sell certain kuji
        shop_ids = cur.execute("SELECT shop_id FROM shop_kuji WHERE kuji_id = ?", kuji_id)
        shop_ids = shop_ids.fetchall()
        ## fill shops info
        shops = []
        for shop_id in shop_ids:
            shops.append(cur.execute("SELECT shop_name, shop_address, shop_tel, lat, lon FROM shops WHERE shop_id = ?", shop_id).fetchone())
        shop_json=[]
        for shop in shops:
            shop_json.append({"shop_name":shop[0], "shop_address":shop[1], "shop_tel":shop[2], "lat":shop[3], "lon":shop[4]})
        ## close DB
        con.close()
        return jsonify(shop_json)
    return render_template("map.html")

# add all shops
@app.route("/allshop", methods=["GET", "POST"])
def allshop():
    con = sqlite3.connect('./static/ichiban_kuji.db')
    cur = con.cursor()
    shops = cur.execute("SELECT shop_name, shop_address, shop_tel, lat, lon FROM shops WHERE shop_name NOT LIKE '%全家%'")
    shop_json=[]
    for shop in shops:
        shop_json.append({"shop_name":shop[0], "shop_address":shop[1], "shop_tel":shop[2], "lat":shop[3], "lon":shop[4]})
    con.close()
    return jsonify(shop_json)

if __name__ == '__main__':
    app.run('0.0.0.0')