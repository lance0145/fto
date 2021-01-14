
mapboxgl.accessToken = 'pk.eyJ1IjoibG9uZ2xhdGZpbmRlciIsImEiOiJjazhnY2RjMnYwMDV3M2hucnk3N3llY3l6In0.J_r7BM6chjYo2_SqHA2x_g';
var coordinates = document.getElementById('coordinates');
var map = new mapboxgl.Map({
	container: 'map',
	style: 'mapbox://styles/mapbox/streets-v11',
	center: [122.56589980392613, 10.695733431914903],
	zoom: 14
});

var geocoder = new MapboxGeocoder({
	accessToken: mapboxgl.accessToken,
	mapboxgl: mapboxgl
});

map.on('click', function(results) {
	$("input[name='x_longitude_latitude']").val(results.lngLat.lng+', '+results.lngLat.lat);
})
map.addControl(geocoder);
geocoder.on('results', function(results) {
})
