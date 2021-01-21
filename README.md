# Instructions
- Install Docker: https://www.docker.com/products/docker-desktop
- In **Dockerfile** edit the *app* variable to the name of the app you want to run
- Run depending on environment: (add `-d` flag to run in background)
    - Development: `docker-compose -f development.yml up --build`
    - Staging: `docker-compose -f staging.yml up --build`
    - Production: `docker-compose -f production.yml up --build`
