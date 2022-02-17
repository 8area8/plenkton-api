"""Python Invoke tasks.

You need to install invoke globally to use this file.
"""

from invoke import task

@task
def build(command):
    """Build the containers."""
    command.run("docker-compose build")

@task
def up(command):
    """Up the containers."""
    command.run("docker-compose up -d")

@task
def down(command):
    """Stop and down the containers."""
    command.run("docker-compose down")

@task
def pytest(command):
    """Run the python tests inside the web container."""
    command.run("docker-compose run --rm web python3 -m pytest")
