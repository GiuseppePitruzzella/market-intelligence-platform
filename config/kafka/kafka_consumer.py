from kafka import KafkaConsumer
import json

# Configura il consumer per connettersi a Kafka
consumer = KafkaConsumer(
    'financial_data_stream', # Nome del topic
    bootstrap_servers='localhost:9092', # Endpoint di Kafka esposto da Docker
    auto_offset_reset='earliest', # Inizia a leggere dall'inizio del topic
    group_id='test-consumer-group', # ID del gruppo di consumer
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # Deserializza il JSON
)

print("▶️  In ascolto sul topic 'financial_data_stream'...")
for message in consumer:
    print("\n--- Nuovo Messaggio Ricevuto ---")
    print(f"Topic: {message.topic}")
    print(f"Dati: {json.dumps(message.value, indent=2)}")
    print("--------------------------------")