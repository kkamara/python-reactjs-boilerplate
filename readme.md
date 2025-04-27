# python-reactjs-boilerplate [![Tests Pipeline](https://github.com/kkamara/python-reactjs-boilerplate/actions/workflows/build.yml/badge.svg)](https://github.com/kkamara/python-reactjs-boilerplate/actions/workflows/build.yml)

(2022) With docker support.

* [Using Postman?](#postman)

* [Installation](#installation)

* [Add testing seed data](#add-testing-seed-data)

* [Usage](#usage)

* [Using Docker](#using-docker)

* [iPython Django Shell](#ipython-django-shell)

* [API](#api)

* [Admin](#admin)

* [Cache react app & view templates](#cache-templates)

* [Mail server](#mail-server)

* [Misc](#misc)

* [Contributing](#contributing)

* [License](#license)

<a name="postman"></a>
## Using Postman?

[Get Postman HTTP client](https://www.postman.com/).

[Postman API Collection for Python ReactJS Boilerplate](https://github.com/kkamara/python-reactjs-boilerplate/blob/main/python-reactjs-boilerplate.postman_collection.json).

[Postman API Environment for Python ReactJS Boilerplate](https://github.com/kkamara/python-reactjs-boilerplate/blob/main/python-reactjs-boilerplate.postman_environment.json).

## Installation

```bash
cp .env.example .env

python3 -m venv .env
source .venv/bin/activate

python3 manage.py migrate

cd frontend
npm i
npm run build
cd ..
python3 manage.py collectstatic
```

##### Add testing seed data

Example:

Load data [auth_user.json](https://github.com/kkamara/python-react-boilerplate/blob/main/app/fixtures/auth_user.json) into database.

```bash
python manage.py loaddata app/fixtures/auth_user
```

## Usage

```bash
# alias py="python3"
py manage.py runserver 3000
# http://localhost:3000
```

## Using Docker?

```bash
alias compose='docker-compose -f local.yml'
compose build
compose up
# http://localhost:3000
```

## iPython Django Shell

```bash
  py manage.py shell -i ipython
```

## API

```bash
  py manage.py show_urls
```

View the api collection [here](https://documenter.getpostman.com/view/17125932/UVyxQYrt).

## Admin

Admin creds are set in [./compose/local/django/start](https://raw.githubusercontent.com/kkamara/python-react-boilerplate/develop/compose/local/django/start)

```bash
export DJANGO_SUPERUSER_PASSWORD=secret

py manage.py createsuperuser --username admin_user --email admin@django-app.com --no-input
```

## Cache react app & view templates <a name="cache-templates"></a>

```bash
py manage.py collectstatic
```

## Mail Server

![docker-mailhog.png](https://raw.githubusercontent.com/kkamara/useful/main/docker-mailhog.png)

Mail environment credentials are at [.env](https://raw.githubusercontent.com/kkamara/python-react-boilerplate/develop/.env.example).

The [mailhog](https://github.com/mailhog/MailHog) docker image runs at `http://localhost:8025`.

## Misc

[See your Python code do web browsing on your screen with GUI.](https://github.com/kkamara/python-selenium)

[See PHP Scraper.](https://github.com/kkamara/php-scraper)

[See Python ReactJS Boilerplate app.](https://github.com/kkamara/python-reactjs-boilerplate)

[See PHP ReactJS Boilerplate app.](https://github.com/kkamara/php-reactjs-boilerplate)

[See Python Docker Skeleton.](https://github.com/kkamara/python-docker-skeleton)

[See Python Desktop Mobile.](https://github.com/kkamara/python-desktop-mobile)

[See Python for Finance.](https://github.com/kkamara/python-for-finance)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[BSD](https://opensource.org/licenses/BSD-3-Clause)
