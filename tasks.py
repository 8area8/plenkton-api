"""Python Invoke tasks.

You need to install invoke globally to use this file.
"""

from invoke import task

@task
def build(command):
    """Build the containers."""
    command.run("docker-compose build", pty=True)

@task
def up(command):
    """Up the containers."""
    command.run("docker-compose up -d", pty=True)

@task
def down(command):
    """Stop and down the containers."""
    command.run("docker-compose down", pty=True)

@task
def pytest(command):
    """Run the python tests inside the web container."""
    command.run("docker-compose run --rm web python3 -m pytest", pty=True)

@task
def jest(command):
    """Run the Jest tests inside the vue container."""
    command.run("docker-compose run --rm vue yarn run jest", pty=True)

@task
def vuesh(command):
    """Create a bash terminal in the vue container."""
    command.run("docker-compose run --rm vue /bin/sh", pty=True)
