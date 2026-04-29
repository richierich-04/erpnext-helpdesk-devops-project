# System Architecture

## Overview

This project implements a DevOps workflow for an ERPNext Helpdesk staging environment hosted on a personal AWS EC2 instance.

## Architecture

GitHub Repository
→ GitHub Actions
→ SSH to AWS EC2
→ Docker Compose deployment
→ ERPNext Helpdesk application
→ Prometheus and Grafana monitoring

## Runtime Components

- ERPNext Helpdesk
- Frappe Framework
- MariaDB
- Redis
- Nginx frontend container
- Background worker containers
- Prometheus
- Grafana
- Node Exporter
- cAdvisor
- Blackbox Exporter

## Environment Isolation

The staging environment runs in a personal AWS account and is isolated from the company production-like deployment.
