# YaYa-Wallet-Webhook-Implementation
This project implements a webhook endpoint for YaYa Wallet's transaction notification system. It receives transaction notifications, verifies their authenticity, and stores them in a PostgreSQL database.
# Features
+ Webhook endpoint for receiving transaction notifications
+ HMAC SHA256 signature verification
+ Replay attack prevention using timestamp validation
+ PostgreSQL database storage
+ Docker containerization
+ Flask-based REST API
# Prerequisites
+ Docker and Docker Compose
+ Python 3.9+
+ PostgreSQL
# Installation
Clone the repository:

##bashCopy git clone https://github.com/Yonatankinfe/YaYa-Wallet-Webhook-Implementation
##cd YaYa-Wallet-Webhook-Implementation

Build and run using Docker Compose:

bashCopydocker-compose up --build
The application will be available at http://localhost:5000
