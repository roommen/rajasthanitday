from kafka import KafkaConsumer
consumer = KafkaConsumer('faceid',bootstrap_servers =['172.26.42.131:9092'])
for msg in consumer:
    print msg.value
