# Cloud Secure Healthcare Appointment Booking System

## Project Overview
The Healthcare Appointment Booking System named Healthcare+ is a cloud-based web application deployed using AWS infrastructure and DevOps practices. The project enables users to securely access healthcare services, book appointments, and manage healthcare-related activities through a web interface.

The deployment environment was designed with scalability, security, monitoring, automation, and high availability considerations using AWS cloud services and Linux server administration techniques.

---

# Technologies Used

- Python Flask
- MySQL
- Docker
- NGINX
- AWS EC2
- AWS Application Load Balancer (ALB)
- AWS CloudWatch
- AWS S3
- Git & GitHub
- GitHub Actions
- DuckDNS
- Let’s Encrypt SSL/TLS

---

# Features

- User Authentication
- Appointment Booking System
- Dockerized Application Deployment
- Reverse Proxy Configuration using NGINX
- HTTPS/SSL Implementation
- CI/CD Pipeline using GitHub Actions
- Automated Backups to AWS S3
- Server Monitoring and Alerting
- CloudWatch Log Monitoring
- Security Alerts for Failed Login Attempts
- Health Checks and Uptime Monitoring

---

# Project Architecture

The application was deployed using a cloud-based AWS architecture consisting of:

- Public and Private Subnets
- Bastion Host
- Private Application Server
- Application Load Balancer
- NGINX Reverse Proxy
- Dockerized Flask Application
- AWS CloudWatch Monitoring
- AWS S3 Backup Storage

---

# Deployment Steps

## 1. Clone Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd healthcare-app
```
---

## 2. Install Docker

```bash
sudo apt update
sudo apt install docker.io -y
```

---

## 3. Build Docker Image

```bash
sudo docker build -t healthcare-app .
```

---

## 4. Run Docker Container

```bash
sudo docker run -d \
--name healthcare-container \
-p 5000:5000 \
healthcare-app
```

---

## 5. Configure NGINX Reverse Proxy

Configure NGINX to forward incoming traffic to the Flask application running inside the Docker container.

---

## 6. Configure HTTPS

HTTPS was implemented using:
- DuckDNS
- Let’s Encrypt SSL/TLS
- Certbot
- NGINX SSL configuration

---

## 7. Configure CI/CD Pipeline

GitHub Actions was configured to automate:
- Source code synchronization
- Docker image building
- Container deployment
- Automated application updates

---

# Monitoring and Security

The project includes:

- CloudWatch Monitoring
- CPU, Memory, and Disk Monitoring
- Failed SSH Login Alerts
- Log Rotation
- Health Check Monitoring
- HTTPS Enforcement
- HSTS Security Headers
- Fail2Ban Protection

---

# Backup Configuration

Automated backup scripts were configured to:
- Backup application data
- Backup database files
- Upload backups to AWS S3
- Execute scheduled backups using cron jobs

---

# Repository Structure

```text
healthcare-app/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── templates/
├── static/
├── backup.sh
├── nginx/
├── .github/workflows/deploy.yml
└── README.md
```

---

# Application Access

The application can be accessed through:

```text
https://healthcareplus.duckdns.org
```

---

# Conclusion

The Healthcare Appointment Booking System successfully demonstrated practical implementation of AWS cloud deployment, Docker containerization, DevOps automation, server monitoring, infrastructure security, and HTTPS-enabled web application deployment within a real-world healthcare environment.
