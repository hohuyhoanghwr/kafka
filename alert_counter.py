import logging
from quixstreams import Application
from quixstreams.dataframe.windows import Count
from datetime import timedelta

def main():
    logging.info("START alert counter...")
    app = Application(
        broker_address="localhost:9092",
        consumer_group="alert-counter",
        auto_offset_reset="latest",
    )

    input_topic = app.topic("alert", value_deserializer="json")
    output_topic = app.topic("alert-count", value_serializer="json")

    sdf = app.dataframe(input_topic)
    sdf = sdf.hopping_window(duration_ms=timedelta(seconds=5), step_ms=timedelta(seconds=1)).agg(alert_count=Count()).final()

    # Write the result to a new topic
    sdf.to_topic(output_topic)

    app.run(sdf)

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
