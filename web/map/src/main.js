$(window).on("load", () => {
    getQuery(100)
        .done(data => {
            console.log(data.rows);
            plotPoints(geoJSONLayer, data.rows);
        })
        .fail((_, status) => console.error(status));
});

function plotPoints(geoJSONLayer, data) {
    // Grab the points of every element.
    let geoDataPoints = data.map(elem =>
        elem.pts.map(point =>
            ({
                type: point.loc.type,
                coordinates: point.loc.coordinates,
                ref1: binArray2FloatArray(point.ref1.$binary),
                ref2: binArray2FloatArray(point.ref2.$binary)
            })
        ))
        .reduce((a, b) => a.concat(b), [])
    geoJSONLayer.addData(geoDataPoints);
}

function binArray2FloatArray(string) {
    let byteArray = base64js.toByteArray(string);
    return new Float32Array(byteArray.buffer);
}
