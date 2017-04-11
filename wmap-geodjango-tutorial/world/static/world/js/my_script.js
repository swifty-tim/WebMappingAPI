/**
 * Created by mark on 15/02/17.
 */

function map_init(map, options) {
    var geom = JSON.parse($("#geom").html());

    geom = L.geoJson(geom);
    geom.addTo(map);

    var bbox = JSON.parse($("#bbox").html());
    // bbox = L.geoJson(bbox);

    // flip lat/lon
    var coord1 = [bbox.coordinates[0][1][1], bbox.coordinates[0][1][0]];
    var coord2 = [bbox.coordinates[0][3][1], bbox.coordinates[0][3][0]];
    // var bbox_array = [bbox.coordinates[0][1], bbox.coordinates[0][3]];

    map.fitBounds([coord1, coord2]);
}
