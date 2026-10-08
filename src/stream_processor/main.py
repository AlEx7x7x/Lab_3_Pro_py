import csv
import random
import tracemalloc
import time
from pathlib import Path
from itertools import islice

from pipeline import build_pipeline
from analytics import calculate_statistics
from filters import filter_low_stock

def generate_test_file(path: Path, count: int) -> None:
    categories = ("Electronics", "Clothing", "Home", "Toys")
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["product_id", "name", "category", "price", "quantity"])
        for index in range(1, count + 1):
            writer.writerow([
                index,
                f"Product {index}",
                random.choice(categories),
                round(random.uniform(10.0, 5000.0), 2),
                random.randint(0, 100),
            ])

def read_all_products_eager(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)

def measure_execution(function, *args):
    tracemalloc.start()
    start_time = time.time()
    
    result = function(*args)
    
    elapsed_time = time.time() - start_time
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return result, peak / 1024 / 1024, elapsed_time

def consume_lazy(path: Path):
    pipeline = build_pipeline(path)
    total_value = (product.price * product.quantity for product in pipeline)
    return sum(total_value)

def main() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    path = data_dir / "products_large.csv"
    
    print("Генерація тестового файлу товарів (100,000 записів)...")
    generate_test_file(path, 100_000)
    
    # 1. Pipeline basics
    pipeline = build_pipeline(path)
    low_stock = filter_low_stock(pipeline, threshold=5)
    print("\nПерші 3 товари з низьким запасом (< 5 шт):")
    for product in list(islice(low_stock, 3)):
        print(product.product_id, product.name, product.category, product.quantity, "шт")

    # 2. Statistics
    pipeline_for_stats = build_pipeline(path)
    stats = calculate_statistics(pipeline_for_stats)
    print(f"\nСтатистика (streaming processing):")
    print(f"Кількість: {stats['count']}")
    print(f"Загальна вартість залишків: {stats['total_value']:.2f}")
    print(f"Найдорожчий товар: {stats['most_expensive_product']} ({stats['most_expensive_price']})")

    # 3. Eager vs Lazy
    print("\n--- Порівняння Eager та Lazy варіантів ---")
    
    eager_result, eager_mem, eager_time = measure_execution(read_all_products_eager, path)
    print(f"Eager Evaluation: Читання {len(eager_result)} записів")
    print(f"Eager Time: {eager_time:.4f} секунд | Eager Peak Memory: {eager_mem:.2f} MB")
    
    lazy_result, lazy_mem, lazy_time = measure_execution(consume_lazy, path)
    print(f"\nLazy Evaluation: Загальна вартість {lazy_result:.2f}")
    print(f"Lazy Time: {lazy_time:.4f} секунд | Lazy Peak Memory: {lazy_mem:.2f} MB")

if __name__ == "__main__":
    main()