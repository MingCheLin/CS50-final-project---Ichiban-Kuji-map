# Ichiban Kuji map
#### Video Demo:  <https://youtu.be/vDUFQqH6NuQ>
#### Description:
My project including 2 part.
Respectively scrap part and map part.

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

## Map
To make the map I use leaflet as map API and openstreetmap as basic map data.
I use flask to build my web.
And when the web is loaded.
Server will send a json file that contain kuji info.
If user search the kuji name the search bar will provide sugestion with the data in this json file.
After user click enter or the sugesstion.
I would sent a request to server and server will send the shop info back.
With the shop info leaflet API can make marker on the map.

