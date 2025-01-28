# Use the official Airflow image as the base
FROM apache/airflow:latest

RUN mkdir -p /opt/airflow/logs && chown -R airflow:airflow /opt/airflow/logs

# Switch to airflow User
USER airflow

# Install requirements
RUN pip install apache-airflow-providers-docker \
  && pip install apache-airflow-providers-http \
  && pip install confluent-kafka

# Switch back to root user
USER root