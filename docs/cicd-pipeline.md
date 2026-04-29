# CI/CD Pipeline

## Overview

The CI/CD pipeline is implemented using GitHub Actions.

## Flow

1. Code is pushed to the `main` branch.
2. GitHub Actions starts the deployment workflow.
3. The workflow connects to the personal AWS EC2 instance using SSH.
4. Deployment files are copied to the EC2 instance.
5. The deployment script runs Docker Compose commands.
6. ERPNext Helpdesk containers are restarted.
7. Scheduler remains disabled for staging safety.
8. A health check confirms the application is reachable.

## Health Check

The deployment is considered successful only if the following command succeeds on the EC2 instance:

curl -fsS http://localhost:8080

## Safety

The deployment script keeps the scheduler disabled so the staging environment does not process real scheduled jobs.
