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

```ini
CLOUD_BASE_URL=data

AUTH0_AUDIENCE=data
AUTH0_ISSUER=data
AUTH0_DOMAIN=data
AUTH0_ALGORITHMS=data

AUTH0_FRONT_ID=data
AUTH0_CLIENT_ID=data
AUTH0_CLIENT_SECRET=data
```
