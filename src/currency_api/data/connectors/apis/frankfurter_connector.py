from typing import List

from currency_api.data.types import Currency, CurrencyRates
from currency_api.data.connectors import CurrencyExchangeConnector


class FrankfurterConnector(CurrencyExchangeConnector):

    def __init__(self, api_url: str = 'https://api.frankfurter.dev/v1/latest', data_source: str = 'Frankfurter Currency API'):
        super().__init__(api_url, data_source)
    
    def parse_currency(self, currency):
        return super().parse_currency(currency).upper()  # Frankfurter uses upper cases.
    
    def _format_api_url(self, base_currency: Currency, currencies: List[Currency], fallback = False) -> str:
        """ Format the api url for frank furter. """
        if fallback:
            raise ValueError('Frankfurter does not have a fallback api url.')
        uri = f'{self._api_url}?BASE={base_currency}'
        if len(currencies) == 0:
            return uri
        return uri + f'&symbols={",".join(currencies)}'    
    
    def _format_data(self, json: dict, base_currency: Currency, currencies: List[Currency]) -> CurrencyRates:
        """ Format the Frankfurter response into currency rates dictionary. """
        lookup = json.get('rates', {})
        return {
            'datasource': self._data_source,
            'base': base_currency,
            'rates': {currency: lookup[currency] for currency in currencies if currency in lookup}  # Filter
        }
    
    def __str__(self):
        return 'Frankfurter'