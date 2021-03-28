
const url = "https://rkhmmz6x6j.execute-api.us-west-2.amazonaws.com/prod/coinmarketcap_top_100"

fetch(url,
    {
        method: "GET",
        mode: "no-cors",
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials" : true
        },
    })
  .then((response) => console.log(response.json()))
  .then((data) => console.log(data))