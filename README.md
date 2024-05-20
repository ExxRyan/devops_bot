# Dockerized Telegram Bot

This repository contains a Dockerized Telegram bot that is designed to be easily deployed and scaled using Docker containers. The bot was created as part of the DevOps module during the PT_START internship.

## Features

- Dockerized architecture for easy deployment and scalability
- Replication for high availability and load balancing
- Custom images for the bot and its dependencies

## Prerequisites

Before you can run the Telegram bot, make sure you have the following prerequisites installed:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

To get started with the Telegram bot, follow these steps:

1. Clone this repository:

    ```shell
    git clone https://github.com/ExxRyan/devops_bot.git
    ```

2. Build the custom Docker images:

    ```shell
    docker-compose build
    ```

3. Start the Docker containers:

    ```shell
    docker-compose up -d
    ```

4. Verify that the Telegram bot is running:

    ```shell
    docker-compose ps
    ```

    You should see the bot container listed as "Up".

## Scaling the Bot

To scale the Telegram bot and handle increased traffic, you can use Docker's built-in scaling capabilities. Here's an example of scaling the bot to 3 replicas:
