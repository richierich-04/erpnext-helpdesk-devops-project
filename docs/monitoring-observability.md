# Monitoring and Observability

## Stack

- Prometheus
- Grafana
- Node Exporter
- cAdvisor
- Blackbox Exporter

## Dashboards

The project includes dashboards for:

- EC2 CPU, memory, and disk usage
- Docker container status
- Container resource usage
- ERPNext Helpdesk HTTP uptime
- HTTP status code
- Helpdesk ticket KPIs

## Application KPIs

Grafana connects to MariaDB using a read-only database user and visualizes:

- Total tickets
- Open tickets
- Closed tickets
- Resolved tickets
- Tickets by status
- Tickets by priority
- Tickets created per day
