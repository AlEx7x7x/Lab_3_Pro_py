from collections.abc import Iterable, Iterator
from models import ProductRecord

def validate_products(rows: Iterable[dict[str, str]]) -> Iterator[ProductRecord]:
    for row in rows:
        try:
            product_id = int(row["product_id"])
            name = row["name"].strip()
            category = row["category"].strip()
            price = float(row["price"])
            quantity = int(row["quantity"])
        except (ValueError, TypeError, KeyError):
            continue
            
        if not name or not category or price < 0 or quantity < 0:
            continue
            
        yield ProductRecord(
            product_id=product_id, 
            name=name, 
            category=category, 
            price=price, 
            quantity=quantity
        )

def filter_by_category(products: Iterable[ProductRecord], category: str) -> Iterator[ProductRecord]:
    for product in products:
        if product.category.lower() == category.lower():
            yield product

def filter_low_stock(products: Iterable[ProductRecord], threshold: int) -> Iterator[ProductRecord]:
    for product in products:
        if product.quantity < threshold:
            yield product