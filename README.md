# Network Monitoring and Energy Optimization System

## Project Description

This project is a Python-based solution designed as a demonstration project for educational purposes within a school setting. This project showcases the concept of monitoring and optimizing server resources. Please note that this school project is not intended for actual use and should not be deployed in a production environment.

## Main Features

- **Multi-Agent Data Collection:** The system allows multiple agents to gather and transmit real-time server statistics. These agents run on various servers and concurrently send data to the central server.

- **SSL Encryption:** For secure data transmission, SSL certificates were implemented, ensuring the confidentiality and integrity of the collected information.

- **InfluxDB Database:** Data collected from the agents is stored in an InfluxDB instance, facilitating efficient data management and retrieval.

- **Grafana Visualization:** Grafana was used for data visualization, providing interactive and informative dashboards displaying server statistics, status, and energy consumption.

- **Remote Server Control:** The Flask web application component allowed administrators to view and manage servers connected via Integrated Lights-Out (iLO) interfaces. This feature enabled server identification, status checks, and remote power-off for unused servers.

## How It Works

1. **Data Collection:** Agents, implemented as Python scripts, run on individual servers. They continuously collect server statistics, including IP addresses, CPU usage, memory usage, and running processes, using the psutil library.

2. **Secure Transmission:** The collected data is securely transmitted to the central server using SSL encryption, where it is processed and stored in the InfluxDB database.

3. **Data Visualization:** Grafana connects to the InfluxDB database and presents server statistics through dynamic and informative dashboards.

4. **Remote Server Management:** The Flask web application provides a user-friendly interface to view and manage servers connected via iLO. Administrators can identify servers, check their status, and remotely power off servers that are not actively running critical processes.

## Simple Diagram

![image](https://github.com/mhi1001/ServerMonitoring/assets/35073349/2f27b0f4-2bfa-44e0-92f2-092405bf7560)

