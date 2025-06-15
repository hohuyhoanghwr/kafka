import logging
from quixstreams import Application
from quixstreams.dataframe.windows import Mean
from datetime import timedelta

def main():
    logging.info("START alert counter...")
    app = Application(
        broker_address="localhost:9092",
        consumer_group="avg-temp",
        auto_offset_reset="latest",
    )

    input_topic = app.topic("sensor", value_deserializer="json")
    output_topic = app.topic("avg-temp", value_serializer="json")

    sdf = app.dataframe(input_topic)
    sdf = sdf.hopping_window(duration_ms=timedelta(seconds=10), step_ms=timedelta(seconds=1)).agg(avg_temp=Mean("temperature")).final()

    sdf.print()
    # Write the result to a new topic
    sdf.to_topic(output_topic)

    app.run(sdf)

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
