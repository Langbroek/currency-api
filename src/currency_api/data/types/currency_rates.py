from typing import TypedDict, Dict



CurrencyRates = TypedDict('CurrencyRates', {'datasource': str, 'base': str, 'rates': Dict[str, float]})