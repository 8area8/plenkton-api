# plenkton-api

Plenkton-api

## Workflow

We use Docker in development

### Install

This project only uses Docker to develop and deploy the application.

- Use [VSCode remote container](https://code.visualstudio.com/docs/remote/containers) to build and launch the application.
- Install a local docker volume. Open your Shell on local, and write `docker volume create pgplenkton`

### Usage

- You can now access to localhost:8000
- Migrate your database (see [migration part](#Migrations))
- Optional: add the admin user from `commands.ipnb`

## Google Cloud Storage

We use Google Cloud storage to send the `dist` folder to the cloud.
The production configuration replace the `static/` prefix by the google cloud storage url.

- Install [Google Cloud Console](https://cloud.google.com/sdk/docs/install#deb).
- Create a bucket.
- Render the [bucket public](https://cloud.google.com/storage/docs/access-control/making-data-public?hl=fr)
- Import files/folder from [command line](https://cloud.google.com/storage/docs/uploading-objects#prereq-cli)

### Be sure your CI works

- We use the [upload cloud storage](https://github.com/google-github-actions/upload-cloud-storage) action.
- Add a Github secret variable `GCP_CREDENTIALS` to connect to google cloud from your local machine and from the CI ([generate a key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys), [access to your service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts?referrer=search&project=plenkton)).
- Add a Github secret variable `CLOUD_BASE_URL` to translate the `static` prefix into `https://storage.googleapis.com/<your-bucket>/dist/` when you build the `dist` folder.

## Deploy to Heroku

We deploy to heroku using the `.heroku.yml`. `Procfile` is not required. ;)

- Use heroku cli to login : `heroku login`
- Add your remote to git : `heroku git:remote -a plenkton`
- Set the container stack: `heroku stack:set container`
- Set env variable `DEBUG` to False on Heroku: `heroku config:set DEBUG=False`
- Configure the automatic deployment by [linking heroku to your github account](https://devcenter.heroku.com/articles/github-integration).

## Environment variables

Add a `.env` at the root:

```ini
CLOUD_BASE_URL=data

AUTH0_AUDIENCE=data
AUTH0_ISSUER=data
AUTH0_DOMAIN=data
AUTH0_ALGORITHMS=data

AUTH0_CLIENT_ID=data
AUTH0_CLIENT_SECRET=data
```

Add a `.env` in `./front`:

```ini
VUE_APP_CLOUD_BASE_URL=data

VUE_APP_AUTH0_AUDIENCE=data
VUE_APP_AUTH0_ISSUER=data
VUE_APP_AUTH0_FRONT_ID=data
```

## Migrations

Use alembic to handle database migrations :
- `alembic revision --autogenerate -m <msg>`: make migrations
- `alembic downgrade <hash>`: downgrade to version
- `alembic history`: show history
- `alembic upgrade head`: migrate to last