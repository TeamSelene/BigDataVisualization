const URL = "localhost";
const PORT = 28017;
const DB = "selene";
const COLLECTION = "images";

function getQuery(limit) {
    queryString = $.param({
        limit: 12
    })
    // console.log(queryString);
    uriQuery = `http://${URL}:${PORT}/${DB}/${COLLECTION}/?${queryString}`;

    let xmlRequest = $.ajax(uriQuery);

    return $.ajax(uriQuery, { dataType: "json" });
}
