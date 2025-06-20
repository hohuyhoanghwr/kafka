from datetime import datetime
from quixstreams import Application
import streamlit as st
from collections import deque

temperature_buffer = deque(maxlen=100)
timestamp_buffer = deque(maxlen=100)

st.title("Real-Time IoT Dashboard")

@st.cache_resource
def kafka_connection():
    return Application(
        broker_address="localhost:9092",
        consumer_group="dashboard",
        auto_offset_reset="latest",
    )

app = kafka_connection()
sensor_topic = app.topic("sensor")
alert_topic = app.topic("alert")

alert_count_topic = app.topic("alert-count") #Visualizing alerts count over last 5 seconds
avg_temp_topic = app.topic("avg-temp") #Visualizing average temperature over last 10 seconds


col1, col2, col3 = st.columns(3)
with col1:
    st_metric_temp = st.empty()
with col2:
    st_metric_avg_temp = st.empty()
with col3:
    st_metric_alert_count = st.empty()

# st_metric_temp = st.empty() # Placeholder for temperature metric
st_chart = st.empty() # Placeholder for temperature chart
# st_metric_alert_count = st.empty()
# st_metric_avg_temp = st.empty()

with app.get_consumer() as consumer:
    consumer.subscribe([sensor_topic.name, alert_topic.name, alert_count_topic.name,avg_temp_topic.name])
    previous_temp = 0
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is not None and msg.topic() == sensor_topic.name:
            sensor_msg = sensor_topic.deserialize(msg)
            temperature = sensor_msg.value.get('temperature')
            device_id = sensor_msg.value.get('device_id')
            timestamp = datetime.fromisoformat(sensor_msg.value.get('timestamp'))
            diff = temperature - previous_temp
            previous_temp = temperature
            timestamp_str = timestamp.strftime("%H:%M:%S")
            st_metric_temp.metric(label=device_id, value=f"{temperature:.2f} °C", delta=f"{diff:.2f} °C")
            
            timestamp_buffer.append(timestamp_str)
            temperature_buffer.append(temperature)
            st_chart.line_chart(
                data={
                    "time": list(timestamp_buffer),
                    "temperature °C": list(temperature_buffer)
                },
                x="time",
                y="temperature °C",
                use_container_width=True,
            )
            
        elif msg is not None and msg.topic() == alert_count_topic.name:
            alert_count_msg = alert_count_topic.deserialize(msg)
            alert_count = alert_count_msg.value.get('alert_count', 0)
            st_metric_alert_count.metric(label="Alert Count last 5 seconds", value=alert_count)

        elif msg is not None and msg.topic() == avg_temp_topic.name:
            avg_temp_msg = avg_temp_topic.deserialize(msg)
            avg_temp = avg_temp_msg.value.get('avg_temp', 0)
            st_metric_avg_temp.metric(label="Avg. Temp. last 10 seconds", value=f"{avg_temp:.2f} °C")