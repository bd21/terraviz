import json

import urllib3


# get top 100 coin market caps
def lambda_handler(event, context):
    http = urllib3.PoolManager()

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        "Accept": "*/*",
        "X-CMC_PRO_API_KEY": "478d0b1f-c75c-44f4-8d32-3f10c63dfd79",
        "Access-Control-Allow-Origin": "*"
    }

    r = http.request('GET', url, headers=headers)

    response = json.loads(r.data)

    result = {}
    result['entries'] = []
    for entry in response['data']:
        result['entries'].append({
            "id": entry['id'],
            "name": entry['name'],
            "symbol": entry['symbol'],
            "rank": entry['cmc_rank'],
            "max_supply": entry['max_supply'],
            "circulating_supply": entry['circulating_supply'],
            "total_supply": entry['total_supply'],
            "quote": entry['quote']
        })

    return {
        'statusCode': 200,
        "isBase64Encoded": False,
        'body': result,
        "headers": {
            "content-type": "application/json"
        }
    }

if __name__ == "__main__":
    lambda_handler(None, None)
