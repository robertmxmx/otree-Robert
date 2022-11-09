# Instructions

- Install Docker: https://www.docker.com/products/docker-desktop
- In **.env** edit the *APP* variable to the name of the app you want to run. For example, if you want to run **non_id5** do:
```
APP=non_id5
```
- Run depending on environment: (add `-d` flag to run in background)
    - Development: `docker-compose -f development.yml up --build`
    - Staging: `docker-compose -f staging.yml up --build`
    - Production: `docker-compose -f production.yml up --build`