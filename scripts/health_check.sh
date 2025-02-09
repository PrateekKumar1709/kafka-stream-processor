#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
KAFKA_HOST="localhost"
KAFKA_PORT="9092"
ZOOKEEPER_HOST="localhost"
ZOOKEEPER_PORT="22181"

echo "Running health checks..."

# Check if Kafka is accessible
check_kafka() {
    echo "Checking Kafka connection..."
    if nc -z ${KAFKA_HOST} ${KAFKA_PORT} 2>/dev/null; then
        echo -e "${GREEN}✓ Kafka is accessible${NC}"
        return 0
    else
        echo -e "${RED}✗ Cannot connect to Kafka${NC}"
        return 1
    fi
}

# Check if Zookeeper is accessible
check_zookeeper() {
    echo "Checking Zookeeper connection..."
    if nc -z ${ZOOKEEPER_HOST} ${ZOOKEEPER_PORT} 2>/dev/null; then
        echo -e "${GREEN}✓ Zookeeper is accessible${NC}"
        return 0
    else
        echo -e "${RED}✗ Cannot connect to Zookeeper${NC}"
        return 1
    fi
}

# Check if consumer is running
check_consumer() {
    echo "Checking consumer status..."
    if docker ps | grep -q kafka-consumer; then
        echo -e "${GREEN}✓ Consumer is running${NC}"
        return 0
    else
        echo -e "${RED}✗ Consumer is not running${NC}"
        return 1
    fi
}

# Run all checks
main() {
    local status=0
    
    check_kafka || status=1
    check_zookeeper || status=1
    check_consumer || status=1
    
    if [ $status -eq 0 ]; then
        echo -e "\n${GREEN}All health checks passed!${NC}"
    else
        echo -e "\n${RED}Some health checks failed!${NC}"
    fi
    
    return $status
}

main
