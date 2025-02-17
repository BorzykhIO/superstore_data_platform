
# Data Platform for Supermarket

## Overview
This project is a prototype of a data platform designed to process and analyze sales data from a supermarket chain. The platform integrates real-time data streaming, batch processing, and data warehousing, leveraging modern data engineering tools.

![Альтернативный текст](https://raw.githubusercontent.com/BorzykhIO/superstore_data_platform/main/img/Superstore_Data_Platform.png)


## Architecture Components

### 1. Kafka Producer (Data Generator)
- Generates synthetic sales data.
- Publishes the data to a Kafka topic.

### 2. Spark Streaming (Kafka Consumer)
- Consumes messages from the Kafka topic in real-time.
- Transforms and loads the data into the staging layer of the data warehouse (PostgreSQL).

### 3. Data Warehouse (PostgreSQL)
- **Staging Layer:** Stores raw data ingested from Kafka.
- **Core Layer:** Transforms raw data into structured dimensions (dimensions and facts).
- **DM Layer (Data Marts):** Aggregates data for analytics and reporting.
  
**DBT Models:** Handle data transformations within the DWH, ensuring clean and structured data for reporting.

### 4. Apache Airflow (Workflow Orchestration)
- Manages data pipeline execution.
- Schedules and runs DBT models for data transformations.

## Technology Stack
- **Kafka**: Message broker for real-time data streaming.
- **Apache Spark (Structured Streaming)**: Processes and transforms streaming data.
- **PostgreSQL**: Data warehouse storage.
- **DBT (Data Build Tool)**: Transforms raw data into structured tables.
- **Apache Airflow**: Orchestrates workflows and schedules DBT models.
- **Jupyter Notebook**: Can be used to do exploratory data analysis and make prototypes of ML models.

## Data Flow
1. **Kafka Producer** generates synthetic sales transactions.
2. **Spark Streaming** consumes and processes messages, then loads them into the **staging layer** in PostgreSQL.
3. **DBT models** transform raw data into dimensions and facts in the **core layer**.
4. DBT further processes **core layer** data into analytics-ready **data marts (DM layer)**, utilizing all DBT features: **Jinja Templates**, **Indepodent incremental data update**.
5. **Airflow** orchestrates the execution of DBT models to maintain data consistency.

## Setup Instructions
### Prerequisites
- Docker & Docker Compose (optional but recommended)
- Kafka & Zookeeper
- Apache Spark
- PostgreSQL
- DBT
- Apache Airflow

### Running the Project
1. Start Kafka and Zookeeper.
2. Run the Kafka Producer to generate data.
3. Start Spark Streaming to consume Kafka messages and write to PostgreSQL.
4. Execute DBT transformations using Airflow.
5. Query the Data Marts for analytics.

## Future Enhancements
- Implement monitoring and logging with Prometheus/Grafana.
- Add schema evolution handling in Kafka.
- Optimize DBT models for performance.
- Add a BI tool such as Apache Superset.
- Introduce batch processing alongside streaming.

---

This README provides a high-level structure; you can refine it based on specific configurations and customizations in your project.

