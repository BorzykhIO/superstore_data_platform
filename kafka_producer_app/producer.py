from confluent_kafka import Producer
from faker import Faker
import random
import pandas as pd
from time import sleep
from random import uniform
import json
import os


BOOTSTRAP_SERVERS = os.getenv("KAFKA_BROKER", "kafka:29092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "test_topic")


faker = Faker()


file_path = "superstore_data.csv"
df = pd.read_csv(file_path, encoding="ISO-8859-1")
unique_products = df[['Product Name', 'Category', 'Sub-Category']].drop_duplicates()
unique_geo = df[['Country', 'City', 'State', 'Postal Code', 'Region']].drop_duplicates()

product_list = unique_products.to_records(index=False).tolist()
geo_list = unique_geo.to_records(index=False).tolist()


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    # else:
    #     print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def generate_synthetic_row():
    row_id = random.randint(1, 9999)
    order_date = faker.date_between(start_date="-1y", end_date="today")
    ship_date = order_date + pd.Timedelta(days=random.randint(1, 7))
    ship_mode = random.choice(["Standard Class", "Second Class", "First Class", "Same Day"])

    customer_id = f"{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}-{random.randint(10000, 99999)}"
    customer_name = faker.name()
    segment = random.choice(["Consumer", "Corporate", "Home Office"])


    product_name, category, sub_category = random.choice(product_list)
    country, city, state, postal_code, region = random.choice(geo_list)

    product_id = f"{category[:3].upper()}-{faker.random_uppercase_letter()}{faker.random_uppercase_letter()}-{random.randint(10000000, 99999999)}"
    order_id = f'US-{order_date}-{product_id}-{customer_id}-{row_id}'
    sales = round(random.uniform(5.0, 500.0), 2)
    quantity = random.randint(1, 10)
    discount = round(random.uniform(0.0, 0.5), 2)
    profit = round(sales * (1 - discount) - random.uniform(5.0, 50.0), 2)

    return {
        "Row ID": row_id,
        "Order ID": order_id,
        "Order Date": str(order_date),
        "Ship Date": str(ship_date),
        "Ship Mode": ship_mode,
        "Customer ID": customer_id,
        "Customer Name": customer_name,
        "Segment": segment,
        "Country": country,
        "City": city,
        "State": state,
        "Postal Code": postal_code,
        "Region": region,
        "Product ID": product_id,
        "Category": category,
        "Sub-Category": sub_category,
        "Product Name": product_name,
        "Sales": sales,
        "Quantity": quantity,
        "Discount": discount,
        "Profit": profit
    }

# Kafka Producer
producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

def produce_synthetic_data(topic, num_messages=4000):
    for _ in range(num_messages):
        sleep(uniform(0.2, 1)) 
        synthetic_row = generate_synthetic_row()
        producer.produce(topic, value=json.dumps(synthetic_row), callback=delivery_report)
    producer.flush()

if __name__ == '__main__':
    print(f"Producing messages to Kafka topic: {TOPIC_NAME}")
    produce_synthetic_data(TOPIC_NAME, num_messages=1000)
