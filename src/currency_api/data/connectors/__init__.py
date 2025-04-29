from typing import List

from .connector import CurrencyExchangeConnector
from .apis import FrankfurterConnector, FreeCurrencyExchangeRatesConnector

# Single threaded connectors.
exchange_connectors: List[CurrencyExchangeConnector] = [
    FrankfurterConnector(),
    FreeCurrencyExchangeRatesConnector()
]