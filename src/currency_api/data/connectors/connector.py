import requests

from typing import List

from currency_api.data.types import Currency, CurrencyRates
from currency_api.utils.metrics import cache_and_log


class CurrencyExchangeConnector:
    """
        Base api class to outline connector functionality.
    """

    def __init__(self, api_url: str, data_source: str):
        self._api_url = api_url
        self._data_source = data_source

    def _format_api_url(self, base_currency: Currency, currencies: List[Currency], fallback: bool = False) -> str:
        """ Format api url for request. """
        return NotImplementedError()
    
    def _format_data(self, data: dict, base_currency: Currency, currencies: List[Currency]) -> CurrencyRates:
        """ Format the response to currency rates. """
        raise NotImplementedError()
    
    def parse_currency(self, currency: Currency) -> Currency:
        """ Validates and parses a currency for expected format. """
        if not isinstance(currency, Currency):
            raise ValueError(f'Provided Currency is not of type ({type(Currency)})')
        currency = currency.strip()
        if len(currency) <= 0 or len(currency) >= 16:
            raise ValueError(f'Provided Currency {currency} is not valid with character length: {len(currency)}')
        return currency

    def parse_currencies(self, currencies: List[Currency]) -> List[Currency]:
        """ Parse currencies before get requests. This removes duplicate currencies and sorts them for consistant cache lookup. """
        return sorted(set([self.parse_currency(currency) for currency in currencies]))
    
    @cache_and_log
    def get(self, uri: str) -> dict:
        """ 
            Make get api call using requests module and return the json response. 
            Main function that allows for easy extension for future exchange connectors.
            Uses the cache and log function to log the metrics and cache uri json results.
            If overriden, the class must call this for logging and caching.
        """
        response = requests.get(uri)
        if response.ok:
            return response.json()
        response.raise_for_status()

    def get_rates(self, base_currency: Currency, currencies: List[Currency]) -> CurrencyRates:
        """ Return the provided currency rates for the base currency. """
        base_currency = self.parse_currency(base_currency)
        currencies = self.parse_currencies(currencies)
        try:
            json = self.get(self._format_api_url(base_currency, currencies))
        except:
            # Try once more with a fallback.
            json = self.get(self._format_api_url(base_currency, currencies, fallback=True))
        return self._format_data(json, base_currency, currencies)