# Ichiban Kuji map
#### Video Demo:  <https://youtu.be/vDUFQqH6NuQ>
#### Description:
My project including 3 part.
Respectively scrap part, map part and server part.

## Scrap
I use scrapy to scrap info from Banpresto official website.
There are two kind of info.
One is shop info.
In this it provide the shop name, address, telephone number and the kuji ID that the shop sell.
And the second is kuji info.
There are only kuji name and the ID of it.

Most difficut part is that I have to transfer the address into geolcode so that I can make the marker on map.
With google map API it would be easy, however, it takes money.
So I decide to use TGOS service, Taiwan goverment geospatial service.
That's why in this map it only show the shops which in Taiwan.
If there are method to transfer all address on the world into geocode it would be easy to make the map complete.
And all the info is stored as db file.

I also write a scrapy to send request to TGOS to transfer address and scrap info from Banpresto web to update info automatically.
However it's not useful now because Banpresto didn't update it's web frequently.

### Spider - country
In this spider it scrap the country info.
It is not useful now because I only make the map in Taiwan now.
But if one day the geocode problem is solved.
This spider may be useful.
### Spider -IchibanKuji
I use this spider to scrap kuji and shop info from Banpresto official website.
I can update the info.
And store kuji info into json file and store shop info into db file.
### Spider - geocode
This spider is used to transfer address to geocode aotomatically.

## Map
To make the map I use leaflet as map API and openstreetmap as basic map data.
I use flask to build my web.
And when the web is loaded.
Server will send a json file that contain kuji info.
If user search the kuji name the search bar will provide sugestion with the data in this json file.
After user click enter or the sugesstion.
I would sent a request to server and server will send the shop info back.
With the shop info leaflet API can make marker on the map.

### layout.html
This is just template that will be used in map.html.
It import leaflet and openstreetmap.
And also bootstrap to further use.
### map.html
In this html it just declare a div to use leaflet API and import the scripts that described below.
### map.js
In this js file I declare how to initialize the web.
If user allow the web to get location info it will locate to the user's current location.
Else it will set map center at Taipei.
And in this js it also make the locate button.
### searchbar.js
It build the search bar that provide sugesstion with kuji.json file.
Both enter and clicking the sugesstion sending POST request to server.
And server will send the most relevant shop infos back.
### marker.js
The shop markers are made in this js file.
After getting the shop infos, they will be used with Leaflet API to make markers of shops on map.
Each marker will provide Necseeary shop info.
And the All shops button also declare in this js file.
This button can show the all shops on the map no matter which kuji it sell.


## Server
### app.py
The server is just get the POST request and use sqlite3 to search the kuji that fit the kuji name.
Use kuji ID to find the shops that sell it.
And send the propriate shop infos back.
And the conmunicate communication agreement is json.
### address2CSV and address2geocode
These two python file will transfer address to CSV file to submit to TGOS platform.
After get the result, it will be update into IchibanKuji.db file.
