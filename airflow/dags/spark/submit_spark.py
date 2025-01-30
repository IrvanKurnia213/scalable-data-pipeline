from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 28),
}

dag = DAG(
    'spark_submit_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

spark_task = BashOperator(
    task_id='submit_spark_job',
    bash_command="""
    docker exec spark-master \
      /opt/spark/bin/spark-submit \
      --class org.apache.spark.examples.SparkPi \
      --master spark://spark-master:7077 \
      --deploy-mode client \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.postgresql:postgresql:42.6.0 \
      --executor-memory 2G \
      --executor-cores 2 \
      --driver-memory 2G \
      --conf spark.dynamicAllocation.enabled=false \
      --conf spark.shuffle.service.enabled=false \
      /opt/spark-apps/pyspark_kafka_consumer.py
    """,
    dag=dag,
)

spark_task
