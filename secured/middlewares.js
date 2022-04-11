// ./middlewares.js

"use strict"
const request = require("request");

module.exports = {
  getSearchToken: (req, res, next) => {

    const postData = {
      userIds: [
        {
          "provider": "Provider Name",
          "name": "user@email.com",
          "type": "User"
        }
      ],
      searchHub: "Your Search Hub",
      filter: "If you want to enforce a filter"
    };

    request(
      "https://platform.cloud.coveo.com/rest/search/v2/token",
      {
        auth: { bearer: "your-search-token-request-api-key" },
        json: true,
        method: "POST",
        body: postData
      },
      (error, response, body) => {
        if (error) {
          console.log("err", error)
          next(error);
        } else if (response.statusCode != 200) {
          console.log(JSON.stringify(res, null, 2))
          next(JSON.stringify(res, null, 2));
        } else {
          req.token = body.token;
          next(body.token);
        }
      }
    );
  }
}