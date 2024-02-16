# 📊 Data Pipeline Project with Airflow, Kafka, Spark, and Cassandra

This project implements an automated data engineering workflow that collects, processes, and stores randomly generated user data. It uses Apache Airflow for orchestration, Apache Kafka for data stream handling, Apache Spark for data processing, and Cassandra for persistent storage.

## 🚀 Quick Start

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the repository**

   git clone [https://github.com/your-username/your-repository.git] (https://github.com/pablogzalez/Realtime-Data-Streaming/tree/master)
   [cd your-repository (Realtime-Data-Streaming)

2. **Start the services**

  Use Docker Compose to build and start the necessary services (Airflow, Kafka, Spark, Cassandra).

  docker-compose up -d

3. **Execution**
- ***Apache Airflow:*** Access the Airflow UI at http://localhost:8080 and trigger the user_automation DAG.
- ***Verify execution:*** Check the logs in Airflow to ensure data is being processed and stored correctly.

📋 Architecture
This project follows a data flow architecture involving the following components:

- ***Apache Airflow:*** Orchestrates the workflow of data collection, processing, and storage.
- ***Apache Kafka:*** Acts as a messaging system to handle real-time data.
- ***Apache Spark:*** Processes the real-time data read from Kafka.
- ***Cassandra:*** Stores the processed data for future queries and analysis.

🛠 Technologies Used
- Apache Airflow
- Apache Kafka
- Apache Spark
- Cassandra
- Docker
