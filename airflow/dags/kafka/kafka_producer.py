from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_kafka_producer():
    subprocess.run(["python", "/opt/airflow/dags/kafka/utils/producer.py"], check=True)

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2025, 1, 28),
}

# Initialize the DAG
dag = DAG(
    'kafka_producer_dag',
    default_args=default_args,
    description='DAG to trigger Kafka producer script',
    schedule_interval='@hourly',  # Adjust schedule as needed
)

# Define the task
run_producer_task = PythonOperator(
    task_id='run_kafka_producer',
    python_callable=run_kafka_producer,
    dag=dag,
)

# Set task dependencies (if needed)
run_producer_task
