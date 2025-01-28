from confluent_kafka import Producer
import json
import random
import time

# Configuration for Kafka Producer
conf = {
    'bootstrap.servers': 'kafka:9092',  # Kafka broker address
    'client.id': 'python-producer'
}

# Create Producer instance
producer = Producer(conf)

# Function to generate random data
def generate_data():
    user_id = random.randint(1, 100)
    movie_id = random.randint(1, 50)
    rating = round(random.uniform(1, 5), 1)
    timestamp = int(time.time())
    
    # Create a JSON object as raw data
    raw_data = {
        "userId": user_id,
        "movieId": movie_id,
        "rating": rating,
        "timestamp": timestamp
    }
    return raw_data

# Function to send data to Kafka
def send_data():
    while True:
        data = generate_data()  # Simulate raw data generation
        # Produce message to the Kafka topic 'raw-data'
        producer.produce('raw-data', key=str(data['userId']), value=json.dumps(data))
        print(f"Sent: {data}")
        producer.flush()  # Ensure the message is sent
        time.sleep(1)  # Simulate a 1-second delay between messages

if __name__ == "__main__":
    try:
        send_data()
    except KeyboardInterrupt:
        print("Producer stopped.")
