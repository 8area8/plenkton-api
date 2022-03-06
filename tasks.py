"""Python Invoke tasks.

You need to install invoke globally to use this file.
"""

from invoke import task

PYTHON_DOCKER = "docker-compose run --rm web"
VUE_DOCKER = "docker-compose run --rm vue"


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


@task(down, build, up)
def repop(command):
    """Stop, build and launch the containers."""


@task
def jest(command):
    """Run the Jest tests inside the vue container."""
    command.run(f"{VUE_DOCKER} yarn run jest", pty=True)


@task
def vuesh(command):
    """Create a bash terminal in the vue container."""
    command.run(f"{VUE_DOCKER} /bin/sh", pty=True)


@task
def pytest(command):
    """Run the python tests inside the web container."""
    command.run("pytest back", pty=True)


@task
def make_migrations(command, msg=""):
    """Generate alembic migration"""
    command.run("alembic revision --autogenerate -m {msg}", pty=True)


@task
def revert_migration(command, version_identifier):
    """Revert alembic migration"""
    command.run("alembic downgrade {version_identifier}", pty=True)


@task
def show_migrations(command):
    """Show alembic migrations."""
    command.run("alembic history", pty=True)


@task
def migrate(command):
    """Apply alembic migrations to the current database."""
    command.run("alembic upgrade head", pty=True)
