# kafka-stream-processor
Real-time data processing pipeline using Apache Kafka and Docker
# Kafka Stream Processor
A real-time stream processing application that analyzes user login events using Apache Kafka, with metrics monitoring through Prometheus and Grafana.

## Project Overview
This project implements a streaming data pipeline that:
1. Processes user login events in real-time
2. Performs risk assessment and analysis
3. Provides metrics monitoring and visualization
4. Supports geographic and temporal analysis
5. Includes comprehensive testing and monitoring

## Architecture
### Components
1. Kafka Broker: Message broker for handling streaming data
2. Zookeeper: Coordination service for Kafka
3. Python Producer: Generates simulated login events
4. Python Consumer: Processes and analyzes login events
5. Kafdrop: Web UI for monitoring Kafka topics
6. Prometheus: Metrics collection and storage
7. Grafana: Metrics visualization and dashboards

## Data Flow
1. Producer generates login events → user-login topic
2. Consumer processes events and performs analysis
3. Processed data → processed-logins topic
4. Metrics exposed via Prometheus endpoint
5. Grafana visualizes metrics and provides dashboards

## Prerequisites
1. Python 3.9 or later
2. Docker and Docker Compose
3. Make utility

## Installation & Setup
1. Clone the repository:
    git clone <https://github.com/PrateekKumar1709/kafka-stream-processor.git>
    cd kafka-stream-processor
2. Initialize the project:
    make init
3. Start all services:
    make start

### Available Make Commands
1. make init: Initialize project and install dependencies
2. make build: Build Docker images
3. make run: Start all services
4. make stop: Stop all services
5. make clean: Clean up all artifacts and containers
6. make test: Run unit and integration tests
7. make lint: Run code linting
8. make logs: View application logs
9. make health: Check system health
10. make monitor: Open Kafdrop UI

## Monitoring & Management
### Access Points
1. Kafdrop UI: http://localhost:9000
2. Prometheus: http://localhost:9090
3. Grafana: http://localhost:3000 (User/Pass: admin/admin)

## Available Metrics
1. Message processing rate
2. Processing time distribution
3. Risk score distribution
4. Error rates by type
5. System health metrics

## Testing
### Running Tests
1. Run all tests with coverage
    make test

2. Run linting
    make lint

### Test Structure
1. Unit tests for individual components
2. Integration tests for Kafka interactions
3. Mocked external dependencies

### Troubleshooting Common Issues
1. Connection refused errors: Ensure all services are   running (docker-compose ps)
Check logs (make logs)
2. Missing metrics:
Verify Prometheus target status
Check consumer metrics endpoint
3. Topic creation issues:
Use Kafdrop UI to verify topic existence
Check Kafka broker logs

## Next Steps:
### Production Deployment Strategy:
1. Use Kubernetes for container orchestration instead of Docker Compose
2. Implement CI/CD pipeline using GitHub Actions/Jenkins with:
    Automated testing
    Security scanning
    Image versioning
    Deployment stages (dev, staging, prod)
3. Use proper secret management (HashiCorp Vault/AWS Secrets Manager)
4. Configure proper networking and security groups
5. Implement proper logging aggregation (ELK Stack/Splunk)

### Additional Production Components:
1. Security:
SSL/TLS encryption for Kafka
2. Authentication/Authorization (SASL)
API Gateway for external access
3. Network segmentation
4. Monitoring & Alerting:
Alert manager for Prometheus
PagerDuty integration
SLO/SLA monitoring
Enhanced logging with correlation IDs
5. Data Management:
Schema Registry for message validation
Dead Letter Queue for failed messages
Data backup and recovery solution
Data retention policies
6. High Availability:
Multi-AZ deployment
Load balancers
Service mesh (Istio)
Circuit breakers
### Scaling Strategies:
1. Kafka Scaling:
Increase partition count for topics
Add more Kafka brokers
Implement consumer groups for parallel processing
2. Consumer Scaling:
Horizontal scaling of consumer instances
Implement back-pressure handling
Add caching layer (Redis)
Optimize batch processing
3. Infrastructure Scaling:
Auto-scaling groups
Resource quotas and limits
Performance monitoring and tuning
Database sharding if needed
4. Monitoring Scaling:
Distributed tracing (Jaeger/Zipkin)
Metrics aggregation
Log rotation and archival
Capacity planning
