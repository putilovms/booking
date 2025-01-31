# Booking
*Educational project*

The Hotel Booking project is implemented on the FastAPI framework. Working with the database is implemented using PostgreSQL and the SQLAlchemy module. The booking API allows you to book hotels, receive reservations, and list hotels and rooms. An authorization and authentication system has been implemented.

## System requirements:

* Python 3.10 or higher
* PostgreSQL 15 database
* UV tools provided by Python packages
* Reddis

## Stack

Python, PostgreSQL, UV, FastAPI, SQLAlchemy, pydantic, alembic, asyncio, sqladmin, pytest, pytest-asyncio, ruff, Celery, Flower, Prometheus, Grafana

## Installation

1. Requires Python version 3.10 or higher and UV
2. Clone the project: `>> git clone git@github.com:putilovms/booking.git`
3. Create an `.env` file for example `.env.example` in the root of the project
4. Install migrations with the command: `>> make update`
5. Starting the server: `>> make run`

## Docker Compose

1. Create an `docker.env` file for example `.env.example` in the root of the project. Also add the following variables there:
   * `POSTGRES_DB` - database name
   * `POSTGRES_USER` - username
   * `POSTGRES_PASSWORD` - password
2. The command to launch containers `>> docker-compose up --build`
