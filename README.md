# ProjectX APIs

## Installation requirements

- pip install -r requirements.txt

## Configuration ⚙️

- Use ReCaptcha V2
- Set environment variable
  - PRO_DB_HOST
  - PRO_DB_USER
  - PRO_DB_PASSWORD
  - PRO_DB_NAME
  - PRO_JWT_KEY
  - PRO_RE_CAPTCHA_SECRET
  - PRO_SES_FROM_EMAIL
- Create an empty database in database server

## Create a symmetric key for JWT encryption 🔑

- Open terminal
- `python`
- `from jwcrypto import jwk`
- `key = jwk.JWK(generate='oct', size=256)`
- `key.export()`
- Copy value and use as `JWT_KEY`

## Quick Start 🚀

- Open terminal in project root
- Run server: `uvicorn app.main:app --reload --host 0.0.0.0`

## Docker Steps

- Build docker image.
- `docker build -t api:latest .`
- Run container with network access.
- `docker run -d -p 8000:8000 api`
- View container id.
- `docker ps`
- Stop container.
- `docker stop container_id`

## Data Migrations

- To create new migrations from model changes
- `alembic revision --autogenerate -m "Comment"`
- To update database with new changes
- `alembic upgrade head`

## API Documentions

- Open browser and paste
- `{Your_ip}:{Your_port}/docs`
- `(e.g., http://127.0.0.1:8000/docs)`