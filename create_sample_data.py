import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


def generate_sample_sales(num_rows: int = 200) -> pd.DataFrame:
    base_date = datetime(2024, 1, 1)

    customer_segments = ["Regular", "VIP", "Corporate"]
    countries_cities = [
        ("Nigeria", "Lagos"),
        ("Nigeria", "Abuja"),
        ("Italy", "Rome"),
        ("Italy", "Milan"),
        ("Germany", "Berlin"),
        ("France", "Paris"),
    ]

    products = [
        ("P001", "Wireless Mouse", "Electronics", "Accessories", 25.0),
        ("P002", "Mechanical Keyboard", "Electronics", "Accessories", 70.0),
        ("P003", "USB-C Cable", "Electronics", "Cables", 10.0),
        ("P004", "Laptop Stand", "Office", "Furniture", 40.0),
        ("P005", "Notebook", "Office", "Stationery", 5.0),
        ("P006", "Ballpoint Pen", "Office", "Stationery", 2.0),
        ("P007", "Gaming Headset", "Electronics", "Audio", 80.0),
        ("P008", "Office Chair", "Office", "Furniture", 150.0),
    ]

    payment_methods = ["Card", "Transfer", "Cash"]

    rows = []

    for i in range(1, num_rows + 1):
        order_id = f"O{i:04d}"

        order_date = base_date + timedelta(days=random.randint(0, 180))

        customer_id = f"C{random.randint(1, 50):03d}"
        customer_name = f"Customer {customer_id}"
        customer_email = f"{customer_id.lower()}@example.com"
        customer_segment = random.choice(customer_segments)

        product_id, product_name, product_category, product_subcategory, base_price = random.choice(products)

        quantity = random.randint(1, 5)
        discount = random.choice([0.0, 0.05, 0.1, 0.15])  

        unit_price = base_price

        country, city = random.choice(countries_cities)
        payment_method = random.choice(payment_methods)

        rows.append(
            {
                "order_id": order_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "customer_id": customer_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "customer_segment": customer_segment,
                "product_id": product_id,
                "product_name": product_name,
                "product_category": product_category,
                "product_subcategory": product_subcategory,
                "unit_price": unit_price,
                "quantity": quantity,
                "discount": discount,
                "payment_method": payment_method,
                "city": city,
                "country": country,
            }
        )

    df = pd.DataFrame(rows)
    return df


def save_to_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved sample data to: {path}")


def main():
    target_path = Path("data/raw/sales_raw.csv")
    df_sales = generate_sample_sales(num_rows=200)
    save_to_csv(df_sales, target_path)


if __name__ == "__main__":
    main()
