from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType, TimestampType
import os

# 🛠 Конфигурация из переменных окружения
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:29092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "test_topic")  # Используем твой топик
POSTGRES_URL = os.getenv("POSTGRES_URL", "jdbc:postgresql://postgres_dwh:5432/dwh_db")
POSTGRES_TABLE = os.getenv("POSTGRES_TABLE", "stg.superstore_data_raw")
POSTGRES_USER = os.getenv("POSTGRES_USER", "dwh_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "dwh_pass")

# 🔥 Инициализация Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
    .getOrCreate()

# 📌 Определяем схему сообщений Kafka (под твой producer)
schema = StructType() \
    .add("Row ID", IntegerType()) \
    .add("Order ID", StringType()) \
    .add("Order Date", StringType()) \
    .add("Ship Date", StringType()) \
    .add("Ship Mode", StringType()) \
    .add("Customer ID", StringType()) \
    .add("Customer Name", StringType()) \
    .add("Segment", StringType()) \
    .add("Country", StringType()) \
    .add("City", StringType()) \
    .add("State", StringType()) \
    .add("Postal Code", StringType()) \
    .add("Region", StringType()) \
    .add("Product ID", StringType()) \
    .add("Category", StringType()) \
    .add("Sub-Category", StringType()) \
    .add("Product Name", StringType()) \
    .add("Sales", FloatType()) \
    .add("Quantity", IntegerType()) \
    .add("Discount", FloatType()) \
    .add("Profit", FloatType())

# 📡 Читаем поток из Kafka, включая Kafka timestamp
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(value AS STRING)", "timestamp AS kafka_timestamp") \
    .select(from_json(col("value"), schema).alias("data"), col("kafka_timestamp")) \
    .select("data.*", "kafka_timestamp")

# 🛢 Функция для пакетной записи в PostgreSQL
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", POSTGRES_URL) \
        .option("dbtable", POSTGRES_TABLE) \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()

# 🔄 Запускаем поток с foreachBatch
query = df.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_postgres) \
    .start()

query.awaitTermination()
