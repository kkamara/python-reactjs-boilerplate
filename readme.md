# python-react-boilerplate

With docker support.

* [Installation](#installation)

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
pip3 install virtualenv && \
  virtualenv env && \
  source env/bin/activate
```

## Usage

```bash
# alias py3="python3"
py3 manage.py runserver 3000
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
  py3 manage.py shell -i ipython
```

## API

```bash
  py3 manage.py show_urls
```

View the api collection [here](https://documenter.getpostman.com/view/17125932/UVyxQYrt).

## Admin

Admin creds are set in [./compose/local/django/start](https://raw.githubusercontent.com/kkamara/python-react-boilerplate/develop/compose/local/django/start)

```bash
export DJANGO_SUPERUSER_PASSWORD=secret

py3 manage.py createsuperuser \
  --username admin_user \
  --email admin@django-app.com \
  --no-input
```

## Cache react app & view templates <a name="cache-templates"></a>

```bash
py3 manage.py collectstatic
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
