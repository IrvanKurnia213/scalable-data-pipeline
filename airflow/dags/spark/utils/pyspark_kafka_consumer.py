from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StringType, StructType, StructField
import psycopg2
from pyspark.sql import DataFrame

# Initialize Spark Session with Kafka support
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/spark-checkpoints") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4") \
    .config("spark.jars.packages", "org.postgresql:postgresql:42.6.0") \
    .getOrCreate()

# Define Kafka broker and topic
KAFKA_BROKER = "kafka:29092"  # Use container name as the hostname
KAFKA_TOPIC = "raw-data"

# Define the schema of Kafka messages
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("movie_id", StringType(), True),
    StructField("rating", StringType(), True),
    StructField("timestamp", StringType(), True)
])

# Read from Kafka topic as streaming DataFrame
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka value (bytes) to string and apply schema
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")  # Extract fields

# Define function to write each batch to PostgreSQL
def write_to_postgres(batch_df: DataFrame, batch_id: int):
    # JDBC connection properties
    jdbc_url = "jdbc:postgresql://analytics-postgres:5432/analytics"
    connection_properties = {
        "user": "analytics",
        "password": "analytics",
        "driver": "org.postgresql.Driver"
    }
    
    # Write the DataFrame to PostgreSQL (using append mode)
    batch_df.write \
        .jdbc(url=jdbc_url, table="ratings", mode="append", properties=connection_properties)

# Write the stream to PostgreSQL using foreachBatch
query = parsed_df.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start()

query.awaitTermination()
