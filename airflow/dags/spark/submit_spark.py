from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.hooks.base_hook import BaseHook
from datetime import datetime, timedelta

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 1, 28),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email_on_retry': False,
}

# Define the DAG
dag = DAG(
    'spark_submit_example',
    default_args=default_args,
    description='Automate spark-submit using Airflow',
    schedule_interval='@daily',  # Can set to a cron schedule if needed
    catchup=False,
)

# Explicitly set the Spark connection configuration within the DAG
spark_conn_id = "spark_default"
spark_connection = BaseHook.get_connection(spark_conn_id)

# Define the SparkSubmitOperator
spark_submit = SparkSubmitOperator(
    task_id='submit_spark_job',
    application='/opt/airflow/dags/spark/utils/pyspark_kafka_consumer.py',  # Path to your Spark application
    name='submit-spark-job',
    conn_id=spark_conn_id,
    conf={
        'spark.executor.memory': '2G',
        'spark.executor.cores': '2',
        'spark.driver.memory': '2G',
        'spark.driver.cores': 2,
        'spark.submit.deployMode': 'client',  # Or 'cluster' depending on your cluster setup
    },
    packages='org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0',  # Add any necessary Spark packages
    executor_memory='2G',
    executor_cores=2,
    driver_memory='2G',
    dag=dag,
)

# Define task order (in this case, there's only one task)
spark_submit
