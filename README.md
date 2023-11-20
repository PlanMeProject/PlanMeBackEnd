# PlanMeBackEnd

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![CI](https://github.com/PlanMeProject/PlanMeBackEnd/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/PlanMeProject/PlanMeBackEnd/actions/workflows/ci.yml)

License: MIT

## Overview
This repo contains everything about the backend implementation for PlanMe.

## Technology Stack
- Django REST Framework
- PostgreSQL
- Docker
- Google OAuth for authentication
- Other notable Python libraries and tools

## Installation

Follow these steps to set up the backend environment for PlanMe:

1. **Clone the Repository**
   - Open your terminal.
   - Clone the repository using Git:
     ```
     git clone https://github.com/PlanMeProject/PlanMeBackEnd.git
     ```
   - Navigate into the cloned directory:
     ```
     cd PlanMeBackEnd
     ```

2. **Set Up a Virtual Environment (Optional)**
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```
       venv\Scripts\activate
       ```
     - On MacOS/Linux:
       ```
       source venv/bin/activate
       ```

3. **Install Dependencies**
     ```
     pip install -r requirements.txt
     ```

4. **Environment Variables**
   - Set up your environment variables in `.env` files (This should be a secrets).

5. **Docker Configuration**
   - Ensure Docker is installed and running on your machine.
     ```
     docker-compose -f loyal.yml build
     ```
   - The command builds the Docker images as defined in `loyal.yml` file. It might take some time to complete, depending on your Docker configuration and network speed.

## Running the Application
1. **Database Migrations**
   - Before using the application, you need to apply database migrations. Run the following command:
     ```
     docker-compose -f local.yml run --rm django python manage.py migrate
     ```

2. **Running Docker Containers**
   - After the build is complete, start the containers:
     ```
     docker-compose -f loyal.yml up
     ```


## Testing
   - To run the tests, run the following command:
    ```
    docker-compose -f local.yml run --rm django pytest -vv
    ```
