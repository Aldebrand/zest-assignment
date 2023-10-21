# Zest Home Assignment: GitHub Repository Manager

Welcome to the GitHub Repository Manager application! This application allows users to interact with the GitHub REST API to fetch the top 100 GitHub repositories sorted by stars, save their favorite repositories, and manage them efficiently.

---

## Architecture

The application adopts a microservices architecture, dividing the business logic into three distinct services:

1. **GitHub Data Service**: Fetches and provides data from the GitHub API.
2. **Authentication Service**: Manages user authentication.
3. **User Favorites Service**: Manages user's favorite repositories.

## Pre-requisites

- Docker and Docker Compose installed on your machine.

## Setup and Running

1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/Aldebrand/zest-assignment.git
    cd zest-assignment
    ```

2. Create environment files (`mongo.env` and `secrets.env`) in the `env_files` directory with the necessary variables as shown below:

    - mongo.env:
        ```env
        MONGO_INITDB_ROOT_USERNAME=<username>
        MONGO_INITDB_ROOT_PASSWORD=<password>
        ```

    - secrets.env:
        ```env
        MONGO_USERNAME=<username> # should be the same as MONGO_INITDB_ROOT_USERNAME
        MONGO_PASSWORD=<password> # should be the same as MONGO_INITDB_ROOT_PASSWORD
        JWT_SECRET_KEY=<secret-key> # example 4d20393ca60f5ed55b55f4fe4009066aebc12ea8378a5e488e61ce354480a438
        ```

3. Navigate to the project root and start the services using Docker Compose.

    ```bash
    docker-compose up --build
    ```

Now, all the services should be running, and you can interact with them through their respective APIs.

## Services & Endpoints

1. **GitHub Data Service** (http://localhost:8080/github)

    - `GET /top-starred-repositories`: Fetches the top 100 GitHub repositories sorted by stars.

2. **Authentication Service** (http://localhost:8081/auth)

    - `POST /login`: Logs in a user with the provided email and password.
    - `POST /signup`: Signs up a new user with the provided email and password.

3. **User Favorites Service** (http://localhost:8082)

    - `POST /favorites`: Adds a repository to a user's favorites list.
    - `DELETE /favorites`: Removes a repository from a user's favorites list.
    - `GET /favorites`: Retrieves the favorite repositories of a user.

## Documentation

The APIs for each service are well-documented using OpenAPI specification. You can find the YAML files describing the API endpoints, request/response formats, and error messages for each service at the following paths:

- **User Favorites Service API**: [OpenAPI Spec](user_favorites_service/user_favorites_service_api.yaml)
- **GitHub Data Service API**: [OpenAPI Spec](github_data_service/github_data_service_api.yaml)
- **Authentication Service API**: [OpenAPI Spec](auth_service/auth_service_api.yaml)

These documentation files provide a clear understanding of how to interact with each microservice and can be used to generate interactive API documentation using tools like Swagger UI or Redoc.


## Dockerization

Dockerfiles have been created for each service, and a Docker Compose file is provided to set up the development environment easily.

## Submission

This project is submitted as a solution to the Zest Home Assignment, following the specified guidelines and requirements. The source code and related documentation are shared via this Git repository.

## Questions or Concerns? 🤔

If you stumble upon any bumps or have some burning questions, feel free to reach out! I'm here to clear the fog and make your journey with this project as smooth as a piece of cake. 🍰 Remember, there's no such thing as a silly question. Hit me up, and let's solve those puzzles together! 🧩🎉

---