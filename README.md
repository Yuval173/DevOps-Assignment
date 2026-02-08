***DevOps Assignment***

**Project Overview**
This project implements a secure Nginx web server environment using Docker Compose. It serves a custom HTML page over HTTP/HTTPS, features rate-limiting protection, and includes an automated testing suite integrated with GitHub Actions.

**Implementation Details**

*Infrastructure:* Custom Dockerfile based on Ubuntu 22.04.

*Ports:*

8080: Serves custom HTML content.

8081: Dedicated error server (Returns 500).

443: Secure HTTPS traffic.

*Rate Limiting:* Configured at 5 requests per second with a burst of 5 to protect against DoS attacks while maintaining accessibility for automated tests.

**Design Decisions & Trade-offs**

*Base Image:* Chose Ubuntu over Alpine to ensure full compatibility with standard troubleshooting tools during the development of security configurations.

*Self-Signed Certificates:* Used for HTTPS to demonstrate protocol implementation without the overhead of external CA management in a lab environment.

*CI Logic:* The GitHub Actions pipeline uses a "continue-on-error" strategy for the Docker run step to ensure artifacts (succeeded or fail files) are always generated for grading.

**Assumptions**
The host machine has Docker and Docker Compose installed.

Port 443 is available and not blocked by local firewalls.

**How to Build and Run**

*Locally:*
Navigate to the project root: cd "DevOps Assignment"

Build and run the environment: docker compose up --build

The server will be available at http://localhost:8080 and https://localhost:443.

*Automated Testing:*
To run the automated Python tests manually: docker compose up --build --exit-code-from test-container
