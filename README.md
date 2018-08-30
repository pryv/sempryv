# SemPryv

This repository contains the code of the SemPryv project, developed by the
[AISLab group][] with [Pryv][].

[aislab group]: https://aislab.hevs.ch
[hes-so valais/wallis]: https://www.hevs.ch/
[pryv]: https://pryv.com/

## Prerequisites

The rest of this documentation is assuming the following prerequisites:

1.  A working and recent linux environment.

2.  A `.env` file in the `backend/` folder containing the following content:

    ```conf
    BIOPORTAL_API_KEY=...
    ```

    The `BIOPORTAL_API_KEY` can be obtained by creating an account on the
    [bioportal website][].

3.  A `.env` file in the `frontend/` folder containing the following content:

    ```conf
    VUE_APP_BACKEND=...
    ```

    The `VUE_APP_BACKEND` should contain the root URL where the backend service
    can be accessed. For instance for development setup it can be set to:
    `http://localhost:8000`.

[bioportal website]: https://bioportal.bioontology.org/account

## Production setup

To run SemPryv locally in production mode, the following steps are required:

1.  Install `docker` (tested with version `18.05.0-ce`, build `f150324782`)

2.  Ensure the `.env` files exist as described in the
    [requirements](#requirements) section.

3.  Build and deploy the containers with:

    ```shell
    docker-compose up
    ```

If successful, the website should then be accessible at http://localhost.

For a production deployment on a server, the steps are similar, but don't forget
to modify the `docker-compose.yml` file to your need (ports, volumes, …).

## Development setup

For the development setup, two terminals will be needed, one for running the
backend and one for running the frontend. The procedures are described below:

_**Backend**_

1.  Go to the backend directory:

    ```shell
    cd backend
    ```

2.  Create a virtual environment:

    ```shell
    python -m venv venv
    ```

3.  Activate the virtual environment:

    ```shell
    . ./venv/bin/activate
    ```

4.  Install python dependencies for the development:

    ```shell
    pip install -r dev-requirements.txt
    ```

5.  Start the backend development server:

    ```shell
    python -m sempryv
    ```

If successful, you should be able to access a page at http://localhost:8000
returning a `404 Not Found` error.

_**Frontend**_

1.  Go to the frontend directory:

    ```shell
    cd frontend
    ```

2.  Install dependencies with `npm`:

    ```shell
    npm install
    ```

3.  Start the frontend development server:

    ```shell
    npm run serve
    ```

If successful, you should be able to access the website at http://localhost:8080
