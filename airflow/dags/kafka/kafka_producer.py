from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess
import logging

def run_kafka_producer():
    try:
        result = subprocess.run(
            ["python", "/opt/airflow/dags/kafka/utils/producer.py"],
            check=True, capture_output=True, text=True
        )
        logging.info(result.stdout)  # Log successful output
    except subprocess.CalledProcessError as e:
        logging.error(f"Kafka producer script failed: {e.stderr}")
        raise  # Ensure Airflow properly marks it as failed

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 0,  # Disable automatic retries
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 28),
}

# Initialize the DAG
dag = DAG(
    'kafka_producer_dag',
    default_args=default_args,
    description='DAG to trigger Kafka producer script',
    schedule_interval='@hourly',
    max_active_runs=1,  # Prevents multiple overlapping runs
    catchup=False  # Prevents unwanted backfills
)

# Define the task
run_producer_task = PythonOperator(
    task_id='run_kafka_producer',
    python_callable=run_kafka_producer,
    dag=dag,
)

# Set task dependencies (if needed)
run_producer_task
