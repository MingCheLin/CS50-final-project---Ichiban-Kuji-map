var markers = new Array();

// function to get shop info from server and add markers
function markerAdd() {
    markerRemove();
    let formdata = new FormData(document.querySelector('form'))
    fetch('/map',{method: 'POST', body: formdata})
    .then(response => response.json())
    .then(shops => maplayer(shops))
    .catch(error => alert("Unvalid kuji name"));
}
// function to add markers
function maplayer(shops) {
    for(i=0;i<shops.length;i++){
        var shop_info = '<h1>'+shops[i]["shop_name"]+'</h1><p>address : '+shops[i]["shop_address"]+ '</p><p>tel : '+shops[i]["shop_tel"]+'</p>';
        var marker = new L.marker([shops[i]['lon'], shops[i]['lat']]).bindPopup(shop_info);
        markers.push(marker);
        map.addLayer(markers[i]);
    }
}
// function to remove markers
function markerRemove(){
    for(i=0;i<markers.length;i++) {
        map.removeLayer(markers[i]);
    }
}


// add a button to show all shops except family mart
L.Control.allShop = L.Control.extend({
    onAdd: function(map) {
      var el = L.DomUtil.create('div', 'leaflet-control');
      el.innerHTML = '<button onclick="markerAddAll()" type="button" class="custom_button allshop_button leaflet-bar">All</button>';
      return el;
}})
L.control.allshop = function(opts) {
    return new L.Control.allShop(opts);
}
L.control.allshop({
    position: 'bottomright'
}).addTo(map);

function markerAddAll() {
    markerRemove();
    fetch('/allshop',{method: 'POST'})
    .then(response => response.json())
    .then(shops => maplayer(shops));
}