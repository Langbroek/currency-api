from typing import List

from currency_api.data.connectors import CurrencyExchangeConnector
from currency_api.data.types import Currency, CurrencyRates


class FreeCurrencyExchangeRatesConnector(CurrencyExchangeConnector):

    def __init__(self, api_url: str = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies', data_source: str = 'Free Currency Exchange Rates API', 
                 fallback_url: str = 'https://latest.currency-api.pages.dev/v1/currencies'):
        super().__init__(api_url, data_source)
        self._fallback_url = fallback_url

    def parse_currency(self, currency):
        return super().parse_currency(currency).lower()  # Free currency uses lower cases.

    def _format_api_url(self, base_currency: Currency, currencies: List[Currency], fallback = False):
        """ Format api url for free currency. """
        base_url = self._fallback_url if fallback else self._api_url

        return base_url + f'/{base_currency}.min.json'
    
    def _format_data(self, json: dict, base_currency: Currency, currencies: List[Currency]) -> CurrencyRates:
        """ Format response to the currency rates for the free currency api. """
        lookup = json.get(base_currency, {})
        return {
            'datasource': self._data_source,
            'base': base_currency,
            'rates': {
                currency.upper(): lookup[currency] for currency in currencies if currency in lookup  # Filter only to expected currencies and upper case
            }
        }
    
    def __str__(self):
        return 'FreeCurrencyRates'