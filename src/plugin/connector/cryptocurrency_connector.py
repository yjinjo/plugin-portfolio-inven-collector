import logging
from typing import Dict, List

from pycoingecko import CoinGeckoAPI
from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger(__name__)


class CryptoConnector(BaseConnector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = CoinGeckoAPI()

    def list_cryptocurrencies(self) -> List[Dict]:
        try:
            coins = self.client.get_coins_markets(
                vs_currency="krw", order="market_cap_desc", per_page=5, page=1
            )

            filtered_coins = list()
            for coin in coins:
                filtered_coins.append(
                    {
                        "name": coin["name"],
                        "current_price": coin["current_price"],
                        "market_cap_rank": coin["market_cap_rank"],
                        "price_change_percentage_24h": coin[
                            "price_change_percentage_24h"
                        ],
                        "high_24h": coin["high_24h"],
                        "low_24h": coin["low_24h"],
                        "last_updated": coin["last_updated"],
                    }
                )
            return filtered_coins
        except Exception as e:
            _LOGGER.error(f"Error fetching cryptocurrency data: {e}")
            return []
