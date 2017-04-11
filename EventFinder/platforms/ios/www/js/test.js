var zoom = 10;

function setCenter() {
    Mapbox.setCenter({
    'lat': 50.2222,
    'lng': 5.2344,
    'animated': true // default false
    });
}

function getCenter() {
    Mapbox.getCenter(function (c) {
    alert(JSON.stringify(c))
    });
}

function getZoomLevel() {
    Mapbox.getZoomLevel(function (zl) {
    alert(zl)
    });
}

function zoomIn() {
    Mapbox.setZoomLevel({
    'level': ++zoom,
    'animated': true // default false
    });
}

function zoomOut() {
    Mapbox.setZoomLevel({
    'level': --zoom,
    'animated': true // default false
    });
}

function showMap() {
    Mapbox.show({
        style: 'emerald',
        margins: {
            'left': 0,
            'right': 0,
            'top': 0,
            'bottom': 80
        },
        center: {
            lat: 52.3702160,
            lng: 4.8951680
        },
        zoomLevel: zoom, // 0 (the entire world) to 20, default 10
        showUserLocation: true, // default false
        hideAttribution: true, // default false
        hideLogo: true, // default false
        hideCompass: false, // default false
        disableRotation: false, // default false
        disableScroll: false, // default false
        disableZoom: false, // default false
        disablePitch: false, // default false
        markers: [
            {
            'lat': 52.3732160,
            'lng': 4.8941680,
            'title': 'Nice location',
            'subtitle': 'Really really nice location',
            'image': 'www/img/markers/hi.jpg' // TODO support this on a rainy day
            }
        ]
        },
        function (result) {
        console.log(JSON.stringify(result));
        // let's add a callback for these markers - invoked when the callout is tapped (Android) or the (i) icon in the marker callout (iOS)
        Mapbox.addMarkerCallback(function (selectedMarker) {
            alert("Marker selected: " + JSON.stringify(selectedMarker));
        });
        },
        function (error) {
        alert(error);
        }
    )
}

function hideMap() {
    Mapbox.hide({},
        function (result) {
        console.log(JSON.stringify(result));
        },
        function (error) {
        alert(error);
        }
    )
}

function addGeoJSON() {
    Mapbox.addGeoJSON({
    'url': 'https://gist.githubusercontent.com/tmcw/10307131/raw/21c0a20312a2833afeee3b46028c3ed0e9756d4c/map.geojson'
    });
}

function addPolygon() {
    Mapbox.addPolygon({
    points: [
        {
        'lat': 52.3832160,
        'lng': 4.8991680
        },
        {
        'lat': 52.3632160,
        'lng': 4.9011680
        },
        {
        'lat': 52.3932160,
        'lng': 4.8911680
        }
    ]
    });
}

function addMarkers() {
    Mapbox.addMarkers([
        {
            'lat': 52.3602160,
            'lng': 4.8891680,
            'title': 'One-line title here', // no popup unless set
            'subtitle': 'This text can span multiple lines on Android only. On iOS it\'s one line max.',
            'image': 'www/img/markers/hi.jpg' // TODO support this on a rainy day
        },
        {
            'lat': 52.3702160,
            'lng': 4.8911680,
            'title': 'Nu subtitle for this one' // iOS: no popup unless set, Android: an empty popup -- so please add something
        }
        ],
        function (result) {
        console.log(JSON.stringify(result));
        },
        function (error) {
        alert(error)
        }
    )
}
