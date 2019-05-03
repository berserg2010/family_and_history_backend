## FAMILY AND HISTORY

### BACKEND

#### INSTALL

##### DEBIAN

>###### FOLDER STRUCTURE
>
>```
>    work/
>        family_and_history/
>            backend/
>```


From _python3_:

\# `apt install python3-virtualenv python3-pip python3-dev virtualenv`


>###### FROM DB POSTGRES
>
>\# `apt install libpq-dev postgresql postgresql-contrib`
>
>
>And add to `requirements.txt`:
>
>     psycopg2
>     psycopg2-binary
>
>\# `sudo su postgres`
>
>\$ `psql`
>
>```SQL
>CREATE ROLE admin WITH SUPERUSER LOGIN PASSWORD '1234' ;
>
>CREATE DATABASE family_and_history
>    WITH ENCODING='UTF8'
>        OWNER=admin
>        LC_COLLATE='ru_RU.UTF-8'
>        LC_CTYPE='ru_RU.UTF-8'
>        CONNECTION LIMIT=-1;
>
>\q
>```
>
>Create database
>
>\# `psql family_and_history -U admin -h localhost -f new_database.sql`
>
>Before migrations remove in `settings.py` (work/family_and_history/backend/backend/backend/) DATABASES block:
>
>```python
>DATABASES = {
>    'default': {
>        'ENGINE': 'django.db.backends.postgresql',
>        'NAME': 'family_and_history',
>        'USER': 'admin',
>        'PASSWORD': '1234',
>        'HOST': 'localhost',
>        'PORT': '5432',
>    }
>}
>```


In `family_and_history/backend/`:

\$ `git clone https://github.com/berserg2010/family_and_history_backend`

\$ `virtualenv --prompt="(venv:family_and_history)" -p /usr/bin/python3 ./venv/`

\$ `source ./venv/bin/activate`

\$ `pip3 install -U -r requirements.txt`

\$ `cd backend/`


###### MIGRATIONS FROM CUSTOM USER

\$ `python3 manage.py makemigrations auth_app`

\$ `python3 manage.py migrate auth_app`

\$ `python3 manage.py migrate`

\$ `python3 manage.py makemigrations`

\$ `python3 manage.py migrate`


***

#### TESTING

##### TEST AND COVERAGE

To run the tests, you must run in a virtual environment:

`pytest`

Execute

`pytest --cov-report html --cov .`

and then open `htmlcov/index.html` to see the coverage report.


***

#### DEPLOY

##### NGINX + UWSGI + SYSTEMD

\# `usermod -aG www-data user`

`user` is your login

\# `apt install libpcre3 libpcre3-dev uwsgi uwsgi-plugin-python3`


###### UWSGI

\# `nano /etc/uwsgi/sites/family_and_history.ini`

```ini
[uwsgi]
env = LANG=en_US.UTF-8
project = family_and_history
uid = user
base = /home/%(uid)
chdir = %(base)/work/%(project)/backend/backend
home = %(base)/work/%(project)/backend/venv
module = backend.wsgi:application
master = true
processes = 5
threads = 2
socket = /tmp/uwsgi/%(project).socket
chown-socket = %(uid):www-data
chmod-socket = 660
vacuum = true
plugins = python3
```


###### NGINX

\# `nano /etc/nginx/sites-available/family_and_history.conf`

```conf
server {
    listen 9999;
    location = /favicon.ico { access_log off; log_not_found off; }

    charset utf-8;
    access_log      /var/log/nginx/family_and_history.access.log combined;
    error_log       /var/log/nginx/family_and_history.error.log warn;

    location / {
        include         uwsgi_params;
        uwsgi_pass      unix:/tmp/uwsgi/family_and_history.socket;
    }

    location /static/ {
        root /home/user/work/family_and_history/backend/backend;
        expires 30d;
    }

    location /media/ {
        root /home/user/work/family_and_history/backend/backend;
    }
}
```

\# `ln -s /etc/nginx/sites-available/family_and_history.conf /etc/nginx/sites-enabled/`

\# `nginx -t`


###### SYSTEMD

\# `nano /etc/systemd/system/family_and_history_uwsgi.service`

```service
[Unit]
Description=uWSGI Emperor service

[Service]
ExecStartPre=/bin/bash -c 'mkdir -p /tmp/uwsgi; chown user:www-data /tmp/uwsgi'
ExecStart=/usr/bin/uwsgi --emperor /etc/uwsgi/sites
Restart=always
KillSignal=SIGQUIT
Type=notify
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

\# `systemctl start family_and_history_uwsgi.service`

\# `systemctl restart nginx.service`

\# `systemctl enable family_and_history_uwsgi.service`

***

### FRONTEND

#### INSTALL

`npm install -g create-react-app`

\$ `create-react-app frontend`

\$ `yarn add react-router-dom` or \$ `npm add react-router-dom`

`npm install apollo-client apollo-cache-inmemory apollo-link-http react-apollo graphql-tag graphql --save`
