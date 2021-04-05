import json
import requests

'''
Pull data sources from the terra ecosystem, specifically
 - Prices
 - Exchange Rates
to extract insights such as
 - asset flow
 - relative and absolute changes (tied to the dollar)
 - best LP farming methods
'''


def main():
    get_anc_prices()


# get the luna vs. terra stablecoin exchange rates
def get_terra_prices():
    response = requests.get("https://lcd.terra.dev/oracle/denoms/exchange_rates")
    list_of_currencies = response.json()['result']
    return list_of_currencies


# request MIR assets prices, liquidity, volume, etc.
# explorer: https://graph.mirror.finance/graphql
def get_mirror_prices():
    response = requests.post(
        'https://graph.mirror.finance/graphql',
        json={
            'query': '''
                {
                  assets {
                    symbol
                    name
                    prices {
                      price
                      oraclePrice
                    }
                    statistic {
                      liquidity
                      volume
                      apr
                      apy
                    }
                  }
                  statistic {
                    network
                    assetMarketCap
                    totalValueLocked
                    collateralRatio
                    mirCirculatingSupply
                    mirTotalSupply
                    govAPR
                    govAPY
                    
                  }
                }
            ''',
        },
    )
    mir_prices = response.json()['data']
    return mir_prices


# get ANC prices, rates, LP rates, etc.
# docs: https://docs.anchorprotocol.com/developers-ethereum/ethanchor-api/getting-market-information
def get_anc_prices():
    '''
    Response format:
    stable_denom: denom of the stablecoin money market
    liquid_terra: liquidTerra is the currently available stablecoin pool size in money market
    exchange_rate: exchange rate between aTerra <> stablecoin (e.g. aUST <> UST)
    last_updated: Unix timestamp at which the last update to this response has been made
    current_apy: Yearly yield on anchor deposits
    borrowed_terra: Sum of all borrowed liabilities in this money market
    utilization_ratio: Ratio between borrowed deposit and total stablecoin deposit
    borrow_interest: Interest rate per block
    '''
    response = requests.get("https://eth-api.anchorprotocol.com/api/v1/stablecoin_info/uusd").json()
    response2 = requests.post(
        'https://mantle.anchorprotocol.com/',
        json={
            'query': '''
                {
                  AnchorBorrowerDistributionAPYs(Order: DESC Limit: 1) {
                    ANCPrice
                    ANCEmissionRate
                    DistributionAPY
                    Height
                    Timestamp
                    TotalLiabilities
                  }
                }
            ''',
        },
    ).json()

    result = {"first": response, "second": response2}

    return result

def get_terraswap_rates():
    # TODO https://docs.terraswap.io/docs/howto/query/
    pass


if __name__ == "__main__":
    main()
