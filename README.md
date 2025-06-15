# Real-Time IoT Sensor Stream Processing with Apache Kafka

This project implements a real-time stream processing system for simulated IoT temperature sensor data using **Apache Kafka**, **Quix Streams**, and **Streamlit**.

It is based on the exercise specification in `kafka_Roland.md`, extended with advanced features such as:
- Windowed aggregation for **alert counts** and **average temperature**
- A responsive **Streamlit dashboard** for live monitoring

---

## 🔧 System Architecture

The system is composed of 5 main components:

1. **Producer** (`producer.py`)  
   Simulates temperature readings from a device every second and sends them to Kafka (`sensor` topic).

2. **Consumer (Alert Filter)** (`consumer.py`)  
   Reads messages from `sensor`, transforms them, filters for high temperatures (Kelvin > 303), and writes alerts to the `alert` topic.

3. **Alert Counter** (`alert_counter.py`)  
   Consumes from `alert`, performs a hopping window aggregation (5s), and writes count results to the `alert-count` topic.

4. **Average Temperature Tracker** (`avg_temp.py`)  
   Consumes from `sensor`, computes the average temperature in a hopping window (10s), and sends it to the `avg-temp` topic.

5. **Real-Time Dashboard** (`dashboard.py`)  
   Streamlit app that visualizes:
   - Latest temperature per device
   - Average temperature (10s window)
   - Alert count (5s window)
   - A rolling chart of last 100 seconds

---

## 🚀 How to Run

### 1. Set up Kafka (Docker)
```bash
docker compose up -d


### 2. Set up Kafka (Docker)
```bash
docker compose up -d

### 3. Start Consumers
In seperate terminals
```bash
python consumer.py          # Transforms + filters alerts
python alert_counter.py     # Windowed alert count
python avg_temp.py          # Windowed average temperature

### 4. Start Dashboard
```bash
streamlit run dashboard.py

## See screenshot files for the snapshot of the dashboard