# Use the official Airflow image as the base
FROM apache/airflow:latest

# Install required system dependencies
USER root
RUN apt-get update && apt-get install -y librdkafka-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y openjdk-17-jdk && rm -rf /var/lib/apt/lists/*

RUN java -version

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Switch to airflow user
USER airflow

# Copy the requirements.txt into the container
COPY requirements.txt /requirements.txt

# Install required Python libraries from the requirements.txt file
RUN pip install --no-cache-dir -r /requirements.txt