from dataclasses import dataclass, field, fields
from collections import deque


@dataclass
class Asset:
    price: float
    expected_annual_return: float
    ttl_yield: float
    dividend_period: int = 4
