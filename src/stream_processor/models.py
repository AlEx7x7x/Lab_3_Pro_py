from typing import NamedTuple

class ProductRecord(NamedTuple):
    product_id: int
    name: str
    category: str
    price: float
    quantity: int