from collections import Counter
from collections.abc import Iterable
from models import ProductRecord

def calculate_statistics(products: Iterable[ProductRecord]) -> dict:
    count = 0
    total_value = 0.0
    most_expensive = None
    categories = Counter()
    
    for product in products:
        count += 1
        total_value += (product.price * product.quantity)
        categories[product.category] += 1
        
        if most_expensive is None or product.price > most_expensive.price:
            most_expensive = product
            
    return {
        "count": count,
        "total_value": total_value,
        "most_expensive_product": most_expensive.name if most_expensive else None,
        "most_expensive_price": most_expensive.price if most_expensive else 0.0,
        "categories": dict(categories),
    }