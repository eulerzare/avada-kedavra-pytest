from threading import Thread

from kafka import KafkaProducer, KafkaConsumer, TopicPartition


def con():
    consumer = KafkaConsumer("sampleTopic", bootstrap_servers=["localhost:9092"])
    consumer.subscribe(['sampleTopic'])
    for msg in consumer:
        print(msg)


w = Thread(target=con, daemon=True)
w.start()

producer = KafkaProducer(bootstrap_servers=["localhost:9092"])

future = producer.send("sampleTopic", b"hello world", key=b"key1")

result = future.get()

print(result)

producer.flush()
