## Local Setup
- Start local database

    `sudo pg_ctlcluster 13 main start`

- Check local databases
  
    `psql -l`

- Start a gunicorn server

    `gunicorn wsgi:app`

- Run bash command on deployed node

    `heroku run <bash command> -a sheriff-sale`

- Run heroku deployment locally

    `heroku local web -f Procfile.windows`