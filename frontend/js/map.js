function init() {
    map = new OpenLayers.Map("basicMap");
    var mapnik         = new OpenLayers.Layer.OSM();
    var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
    var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
    var position       = new OpenLayers.LonLat(13.41,52.52).transform( fromProjection, toProjection);
    var zoom           = 10;
    var markers = new OpenLayers.Layer.Markers( "Markers" );
    var lonlats = [];
    map.addLayer(markers);
    map.addLayer(mapnik);

    var vector_layer = new OpenLayers.Layer.Vector();
    map.addLayer(vector_layer);

    OpenLayers.Control.Click = OpenLayers.Class(OpenLayers.Control, {
        defaultHandlerOptions: {
            'single': true,
            'double': false,
            'pixelTolerance': 0,
            'stopSingle': false,
            'stopDouble': false
        },

        initialize: function(options) {
            this.handlerOptions = OpenLayers.Util.extend(
                {}, this.defaultHandlerOptions
            );
            OpenLayers.Control.prototype.initialize.apply(
                this, arguments
            );
            this.handler = new OpenLayers.Handler.Click(
                this, {
                    'click': this.trigger
                }, this.handlerOptions
            );
        },

        trigger: function(e) {
            var lonlat = map.getLonLatFromPixel(e.xy);
            lonlats.push(lonlat);
            markers.addMarker(new OpenLayers.Marker(lonlat));
        }

    });
    var click = new OpenLayers.Control.Click();
    map.addControl(click);
    click.activate();

    map.setCenter(position, zoom );

    function converted_lonlats(){
        var lonlats_t = lonlats.map(function (lonlat) {
            var l = new OpenLayers.LonLat(lonlat.lon, lonlat.lat);
            return l.transform(new OpenLayers.Projection("EPSG:900913"), new OpenLayers.Projection("EPSG:4326"));
        });
        return lonlats_t;
    }

    function getArea(){
        if (lonlats.length==0){
            alert("No markers");
            throw 'No markers';

        }
        var lonlats_t=converted_lonlats();

        longitudes = lonlats_t.map(function(lonlat){

            return lonlat.lon;
        });
        latitudes = lonlats_t.map(function(lonlat){
            return lonlat.lat;
        });
        return {
            "min_longitude": Math.min.apply(Math, longitudes)-0.0001,
            "min_latitude": Math.min.apply(Math, latitudes)-0.0001,
            "max_longitude": Math.max.apply(Math, longitudes)+0.0001,
            "max_latitude": Math.max.apply(Math, latitudes)+0.0001
        }
    }

    function createPolygon(route){
        var points = [];
        var proj1 = new OpenLayers.Projection("EPSG:4326");
        var proj2 = new OpenLayers.Projection("EPSG:900913");
        var siteStyle = {
            fill: false,

        };
        for (var i = 0; i < route.length; i++){
            var point = new OpenLayers.Geometry.Point(route[i][1], route[i][0]);
            point.transform(proj1, proj2);
            points.push(point);
            console.log(point);
        }
        var linearRing = new OpenLayers.Geometry.LinearRing(points);
        var geometry = new OpenLayers.Geometry.Polygon([linearRing]);
        var polygonFeature = new OpenLayers.Feature.Vector(geometry, null, siteStyle);
        vector_layer.addFeatures([polygonFeature]);
    }

    $("#find_routes").click(function(e) {
        e.preventDefault();
        var lonlats_t=converted_lonlats();
        var target_points = lonlats_t.map(function(lonlat){
            return {
                'latitude': lonlat.lat,
                'longitude': lonlat.lon
            }
        })

        var data = {
            "vehicles_number": $("#courier_num").val(),
            "target_points": target_points
        };

        $.ajax({
            url: 'http://localhost:5000/routes',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json;',
            dataType: 'json',
            async: true,
            success: function(msg) {
                console.log(msg);
                for (var i=0; i<msg.routes.length; i++){
                    createPolygon(msg.routes[i]);
                }

            }
        });

    });


}



