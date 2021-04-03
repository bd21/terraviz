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
    get_mirror_prices()


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


def get_anc_prices():
    pass


def get_terraswap_rates():
    # TODO https://docs.terraswap.io/docs/howto/query/
    pass


if __name__ == "__main__":
    main()
