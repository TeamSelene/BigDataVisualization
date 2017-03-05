$(window).on("load", () => {
    getQuery()
        .done(data => console.log(data.rows))
        .fail((_, status) => console.error(status));
});
