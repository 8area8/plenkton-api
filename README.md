# plenkton-api

Plenkton-api

## Workflow

We use Docker in development

### Install

This project only uses Docker to develop and deploy the application.

- Install Docker and Docker-compose (don't forget the post install ;) )
- Run `docker-compose build` at the root of the repository

### Usage

- Run `docker-compose up`
- You can now access to localhost:3000 (and also localhost:8000)

### How to access to the Python/nodeJs environments ?

- These environments are accessible inside the web container :
- Install Vscode Remote Container
- Run VScode inside the web container
- And _voila_ !

### Using Python Invoke

If you install invoke globally (`pip3 install invoke`), you can use the invoke tasks defined in [tasks.py](./tasks.py) !

- pattern: `inv <task>`
- example: `inv build` - will build the containers.
