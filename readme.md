# python-react-boilerplate

(08-Apr-2022) An MVC Python Django (5.2 LTS) boilerplate with React Redux SPA.

* [Using Postman?](#using-postman)

* [Requirements](#requirements)

* [Installation](#installation)

* [Usage](#usage)

* [Using Docker?](#using-docker)

    * [Existing Admin User When Using Docker](#existing-admin-user-when-using-docker)

    * [Using Docker's Mail Server](#using-dockers-mail-server)

* [iPython Django Shell](#ipython-django-shell)

* [API](#api)

* [Cache View Templates](#cache-view-templates)

* [Contributing](#contributing)

* [License](#license)

## Using Postman?

[Get Postman HTTP client](https://www.postman.com).

[Postman API Collection for Python React Boilerplate](./python-react-boilerplate.postman_collection.json).

[Postman API Environment for Python React Boilerplate](./python-react-boilerplate.postman_environment.json).

## Requirements

* [Tested using Python 3.13](https://www.python.org)

## Installation

```bash
cp .env.example .env

python -m venv env
source env/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

cd frontend
cp .env.example .env
yarn
yarn build
# in root .env, set DEBUG=True
yarn start
```

## Usage

```bash
python manage.py runserver
# http://localhost:8000
```

## Using Docker?

```bash
alias compose='docker-compose -f local.yml'
compose build
compose up
# http://localhost:8000
```

#### Existing Admin User When Using Docker

The admin user details are set in [./compose/local/django/start](./compose/local/django/start).

```bash
export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-secret}"

python manage.py createsuperuser \
  --no-input \
  --username admin_user \
  --email admin@django-app.com
```

#### Using Docker's Mail Server

<img src="https://raw.githubusercontent.com/kkamara/useful/main/docker-mailhog.png" alt="docker-mailhog.png" width="300px"/>

Mail environment credentials are at [.env](./.env.example).

The [Mailhog](https://github.com/mailhog/MailHog) Docker mail client runs at `http://localhost:8025`. This is running in the above image that is receiving emails from your Django app.

## iPython Django Shell

```bash
python manage.py shell -i ipython
```

## API

```bash
python manage.py show_urls
```

## Cache View Templates

This includes the React app build files.

```bash
python manage.py collectstatic
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[BSD](https://opensource.org/licenses/BSD-3-Clause)
