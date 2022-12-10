// set map object
let options = {minZoom: 8, zoomControl: false};
try{
    map = L.map('map', options).locate({setView: true});
}
catch(e){
    map = L.map('map', options).setView([121.5173399, 25.0475613], 13);
}

// load openstreetmap from http://www.openstreetmap.org
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// add locate user location button
function locate_user(){
    map.locate({setView: true})
}
L.Control.Locate_button = L.Control.extend({
    onAdd: function(map) {
      var el = L.DomUtil.create('div', 'leaflet-control');
      el.innerHTML = '<button onclick="locate_user()" type="button" class="custom_button locate_button leaflet-bar"></button>';
      return el;
}})
L.control.locate_button = function(opts) {
    return new L.Control.Locate_button(opts);
}
L.control.locate_button({
    position: 'bottomright'
}).addTo(map);

