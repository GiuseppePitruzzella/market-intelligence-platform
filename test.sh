#!/bin/bash

echo "Starting Docker services in the background..."
docker compose up -d

# Wait 60 seconds to give Logstash time to perform the first polling
echo "Waiting 60 seconds for Logstash to collect the first data..."
sleep 60

echo "Starting the Kafka consumer to display messages..."
python kafka/kafka_consumer.py

echo "Shutting down Docker services..."
docker compose down