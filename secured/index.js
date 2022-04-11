const express = require("express");
const path = require("path");
const app = express();
const middlewares = require("./middlewares.js");
const port = 4000;

app.get('/token', (req, res) => {
    middlewares.getSearchToken(req, res, function (response) {
        res.send(JSON.stringify(response));
    })
})

app.get('/search/', (req, res) => {
    res.sendFile(path.join(__dirname, "/search.html"));
})

app.listen(port, () => {
    console.log(`Search token listening on http://localhost:${port}`)
})