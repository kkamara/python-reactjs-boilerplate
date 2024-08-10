# python-reactjs-boilerplate [![Tests Pipeline](https://github.com/kkamara/python-reactjs-boilerplate/actions/workflows/build.yml/badge.svg)](https://github.com/kkamara/python-reactjs-boilerplate/actions/workflows/build.yml)

With docker support.

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

## Installation

```bash
cp .env.example .env

pip install virtualenv
virtualenv env
source env/bin/activate

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

[See python react boilerplate app.](https://github.com/kkamara/python-react-boilerplate)

[See python docker skeleton.](https://github.com/kkamara/python-docker-skeleton)

[See python desktop mobile.](https://github.com/kkamara/python-desktop-mobile)

[See python for finance.](https://github.com/kkamara/python-for-finance)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[BSD](https://opensource.org/licenses/BSD-3-Clause)
