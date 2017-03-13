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
    let geoDataPoints = data.map(elem => elem.loc);
    console.log(geoDataPoints);
    geoJSONLayer.addData(geoDataPoints);
}
