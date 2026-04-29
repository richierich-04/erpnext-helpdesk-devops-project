# ERPNext Helpdesk DevOps Project

This repository contains the DevOps implementation for an ERPNext Helpdesk staging environment.

## Scope

- Docker-based ERPNext Helpdesk deployment
- Safe staging restore process
- CI/CD deployment automation
- Prometheus and Grafana observability
- Infrastructure, container, uptime, and Helpdesk ticket KPI dashboards

## Environment

The project runs on an isolated personal AWS EC2 instance. The staging environment contains restored ticket data for project demonstration, while email integrations, webhooks, notifications, and scheduler jobs are disabled for safety.

## Components

- ERPNext Helpdesk
- Docker Compose
- MariaDB
- Redis
- Prometheus
- Grafana
- Node Exporter
- cAdvisor
- Blackbox Exporter

## Repository Contents

- `deploy/deploy.sh` - deployment automation script for staging EC2
- `monitoring/monitoring.compose.yaml` - observability stack
- `monitoring/prometheus/prometheus.yml` - Prometheus scrape configuration
- `monitoring/blackbox/blackbox.yml` - uptime probe configuration
- `docs/` - project documentation

## Safety

This repository does not include private keys, environment files, database backups, site configuration secrets, or private company attachments.
