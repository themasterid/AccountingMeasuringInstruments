# Accounting of Measuring Instruments - учет средств измерений на предприятиях

## Accounting of Measuring Instruments - учет средств измерений на предприятиях

[![AccountingMeasuringInstruments workflow](https://github.com/themasterid/AccountingMeasuringInstruments/actions/workflows/AccountingMeasuringInstruments.yml/badge.svg)](https://github.com/themasterid/AccountingMeasuringInstruments/actions/workflows/AccountingMeasuringInstruments.yml)

Проект учета средств измерений на предприятиях, контроль сроков поверок, консерваций и выбраковки.

Проект доступен по адресу http://62.84.115.143/ для ознакомительных целей.

# Стек
- Python 3.10
- Docker
- docker-compose
- Django 4
- Django REST framework
- CI/CD
- PostgreSQL
- Yandex.Cloud

## Запуск с использованием CI/CD

Установить docker, docker-compose на сервере виртуальной машины Yandex.Cloud:
```bash
ssh username@ip
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Создаем папку infra4:
```bash
mkdir infra4
```
- Переносим файлы docker-compose.yml, default.conf и .env на сервер в папку infra4.

```bash
scp .env username@server_ip:/home/username/infra4/
scp docker-compose.yml username@server_ip:/home/username/infra4/
scp default.conf username@server_ip:/home/username/infra4/
```
- Так же, можно создать пустой файл .env в директории infra4, позже в него будем добавлять данные с git secrets:

```bash
touch .env
```
- Заполнить в настройках репозитория секреты .env

```bash
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='db_name'
POSTGRES_USER='db_user'
POSTGRES_PASSWORD='put_your_password'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=False
```
- Запускаем контейнеры находясь в папке infra4:
```bash
sudo docker-compose up -d --build
```
- Затем применяем миграции, собираем статику:
```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Загружаем данные из csv файлов в базу данных postgresql командами:

```bash
sudo docker-compose exec backend python manage.py EDIT
```

- Остановить:
```bash
sudo docker-compose stop/down
```


## Запуск проекта через Docker на локальной машине:
- Устанавливаем Docker на localhost, пример для Linux:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install curl -y
sudo curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo rm get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

- В папке infra4 переименовываем файл .env_example в .env и заполняем своими данными согласно шаблона:

```bash
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='db_name'
POSTGRES_USER='db_user'
POSTGRES_PASSWORD='put_your_password'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=False
```

- Затем в папке infra4 выполнить команду, запускаем контейнеры:

```bash
sudo docker-compose up -d --build
```

Для доступа к контейнеру backend выполните следующие команды, это позволит собрать статику, сделать миграции и если нужно создать администратора, для доступа в админку:

```bash
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate --noinput 
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

- Остановить:
```bash
sudo docker-compose stop/down
```

## Запуск проекта в dev-режиме

- Установить и активировать виртуальное окружение:

```bash
python3 -m venv venv
```
```bash
source venv/bin/activated
```

- Установить зависимости из файла requirements.txt

```bash
cd EDIT
```
```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

- Создайте базу и пользователя в PosgreSQL:

```bash
sudo -u postgres psql
CREATE DATABASE basename;
CREATE USER username WITH ENCRYPTED PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE basename TO username;
```

- Прописываем данные для работы в dev режиме:

```bash
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='db_name'
POSTGRES_USER='db_user'
POSTGRES_PASSWORD='password'
DB_HOST='db'
DB_PORT='5432'
SECRET_KEY='put_your_code'
ALLOWED_HOSTS='127.0.0.1, localhost, backend, ip_server'
DEBUG=True
```

- Выполняем миграции, собираем статику, создаем администратора:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
```

- Запускаем сервер:
```bash
python manage.py runserver localhost:80
```

Автор: [Клепиков Дмитрий](https://github.com/themasterid)
