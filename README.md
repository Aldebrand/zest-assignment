# Zest Home Assignment: GitHub Repository Manager

Welcome to the GitHub Repository Manager application! This application allows users to interact with the GitHub REST API to fetch the top 100 GitHub repositories sorted by stars, save their favorite repositories, and manage them efficiently.

---

## Architecture:

The application is structured following a microservices architecture, partitioning the business logic into three distinct, independently deployable services, each with its own defined functionality and responsibility:

1. **GitHub Data Service**: 
   - Responsible for fetching and providing data from the GitHub API.
   - Utilizes Redis for caching the top 100 starred repositories, capitalizing on the infrequent changes in this data set to optimize response times and reduce the load on the GitHub API. The cache expiration time is configurable within the GitHub Data Service settings to cater to different data freshness requirements.

2. **Authentication Service**: 
   - Manages user authentication, ensuring secure and streamlined user access.

3. **User Favorites Service**: 
   - Manages the user's favorite repositories, providing a personalized experience.

In addition to the aforementioned services, this project leverages two key data management technologies:

- **Redis**: 
   - Employed to cache the top 100 starred repositories, thereby significantly enhancing the application's performance. Redis was chosen for its high-speed data access, simplicity, and the value it provides in scenarios where data changes are less frequent.

- **MongoDB**: 
   - Selected as the primary database due to its flexibility and capability to efficiently handle the data types present in this project, which mainly revolve around repository data from the GitHub API, and user data including emails and passwords. 
   - The project utilizes two collections within MongoDB; one for users and another for storing the favorite repositories against user IDs. The schema-less, document-oriented nature of MongoDB is particularly beneficial in this scenario as it allows for straightforward storage and retrieval of diverse repository data alongside user data, all while maintaining a clean and understandable data model.
   - MongoDB's ability to handle evolving data models is advantageous as it supports potential future enhancements to the application, such as incorporating additional data fields from the GitHub API or extending user profile information.
   - Furthermore, MongoDB provides the necessary tools for scaling the database horizontally, ensuring the application remains performant and resilient as data and user loads grow over time.

The combination of Redis for caching and MongoDB for persistent data storage provides a balanced data management solution, aligning with the microservices architecture to promote scalability, performance, and maintainability.

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

## Usage Guide:

The application is designed to provide a seamless and intuitive user experience. Here's a step-by-step guide on how to interact with the services:

1. **User Registration and Authentication**:
   - Your journey begins by signing up through the Authentication Service. 
   - Once you provide your email and password, you will receive a JWT (JSON Web Token) which remains valid for 12 hours.
   - This token is crucial for accessing other services securely.

2. **Exploring GitHub Repositories**:
   - With authentication out of the way, head over to the GitHub Data Service to fetch the top 100 starred repositories on GitHub.
   - This data is neatly packaged, ready for you to browse through, and discover projects that pique your interest.

3. **Managing Your Favorite Repositories**:
   - Found some repositories you love? It's time to save them!
   - Utilize the User Favorites Service to add repositories to your favorites list. You can use the data returned from the GitHub Data Service for this purpose.
   - You can also remove repositories from your favorites or retrieve your entire favorites list anytime you wish.
   
The flow from signing up, to exploring repositories, and finally managing your favorites is designed to be straightforward and user-friendly, allowing you to make the most out of the vast ocean of projects on GitHub.

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

Certainly! Here's the refined version of your notes formatted in Markdown:

## Considerations:

1. **Logging Infrastructure**:
   - In this project, a conventional logging setup with a rotating file handler is utilized. However, in a production environment, it's prudent to employ a robust logging service. A setup that writes logs to Elastic Search and optionally connects to an event bus like Kafka to capture and log events across services would be ideal. This exercise was time-bound which necessitated a focus on the core functionality, hence a simpler logging setup was adopted.

2. **Testing**:
   - Manual testing was the primary mode of verification due to the time constraints of this exercise. While every effort has been made to ensure the application operates correctly, should any issues arise, I am readily available to address them. The lack of automated testing in this instance is acknowledged, and under different circumstances, a comprehensive suite of tests covering all services and applications would be implemented to guarantee reliability and correctness.

Your understanding and consideration regarding these aspects are greatly appreciated. This project serves as a testament to what can be achieved within a limited timeframe while also highlighting areas for further enhancement in a more expansive development window.

## Questions or Concerns? 🤔

If you stumble upon any bumps or have some burning questions, feel free to reach out! I'm here to clear the fog and make your journey with this project as smooth as a piece of cake. 🍰 Remember, there's no such thing as a silly question. Hit me up, and let's solve those puzzles together! 🧩🎉

---