#!/bin/bash

echo "Setting up Market Intelligence Platform..."

# Create necessary directories
mkdir -p logs data/sample config/logstash/pipeline config/logstash/patterns
mkdir -p config/elasticsearch/mappings config/grafana/dashboards config/grafana/datasources
mkdir -p src/data-ingestion/news-scrapers src/data-ingestion/social-media-collectors
mkdir -p src/data-processing/spark-jobs src/api/fastapi-backend src/frontend/react-dashboard

# Copy environment variables
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please configure your API keys."
fi

# Make scripts executable
chmod +x scripts/*.sh

# Build Docker images
echo "Building Docker images..."
docker-compose build

# Create Kafka topics
echo "Creating Kafka topics..."
docker-compose up -d kafka zookeeper
sleep 30
docker-compose exec kafka kafka-topics --create --topic market-news --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
docker-compose exec kafka kafka-topics --create --topic social-sentiment --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
docker-compose exec kafka kafka-topics --create --topic market-data --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
docker-compose exec kafka kafka-topics --create --topic processed-insights --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

echo "Setup completed! Run 'docker-compose up -d' to start all services."