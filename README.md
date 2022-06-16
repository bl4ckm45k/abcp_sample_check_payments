## Ubuntu 20.04
[Начальная настройка сервера](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-20-04-ru)    
[Настройка ключей ssh](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04-ru)    

> Без настройки ssh подключения ваш сервер может быть уязвим
#### Обновите и установите пакеты

```
apt update  
apt install -y htop git build-essential libssl-dev libffi-dev python3-pip python3-dev python3-setuptools python3-venv postgresql postgresql-contrib
```

Если требуется добавьте в строку выше nginx redis-server certbot python3-certbot-nginx

#### Зайдите в терминал управления PostgreSQL

```
sudo -u postgres psql
```

#### Смените пароль пользователя postgres

```
ALTER USER postgres with password 'ВАШ_ПАРОЛЬ';
```

#### Посмотрите кодировку шаблона базы данных (Потребуется пароль):

```
sudo -u postgres psql
\l
```

#### Если кодировка отличается от "en_US.utf8" выполните команды

```
UPDATE pg_database SET datistemplate = FALSE WHERE datname = 'template1'; 
DROP DATABASE template1;
CREATE DATABASE template1 WITH owner=postgres ENCODING = 'UTF-8' lc_collate = 'en_US.utf8' lc_ctype = 'en_US.utf8' template template0;
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template1';
```

#### Создайте базу данных

```
CREATE DATABASE abcp;
```

#### Установите прослушиваение адресов только из локальной системы

```
nano /etc/postgresql/12/main/postgresql.conf
```

Переменная listen_addresses = 'localhost'

#### Разрешите пользователю postgres локальную аутентификаю с md5

```
nano /etc/postgresql/12/main/pg_hba.conf
```

Найдите в конце файла строку
```# Database administrative login by Unix domain socket```   
Строка ниже должна выглядеть как ```local   all             postgres                                md5 ```

#### Перезагрузите PostgreSQL

```
sudo service postgresql restart
```

#### Включите Firewall и разрешите подключаться из локальной сети к БД

```
sudo ufw enable
sudo ufw allow proto tcp from 127.0.0.1/24 to any port 5432
```

#### Откройте папку назначения, скачайте репозиторий, переименуйте папку и файл с настройками

```
cd /home
git clone https://github.com/bl4ckm45k/abcp_sample_check_payments.git
mv abcp_sample_check_payments sample
cd /home/sample
mv .env.example .env
```

#### Отредактируйте настройки в файле ```.env``` под себя

```
nano /home/sample/.env
```

| Параметр         | Откуда брать                                                                                 |
|------------------|----------------------------------------------------------------------------------------------|
| BOT_TOKEN        | [BotFather (Получить токен)](https://t.me/BotFather/)                                        |
| ADMINS           | Поменяйте после запуска (Узнать командой /chat_id), если администратор один укажите два раза |
| USE_REDIS        | Если не знаете, то оставьте как есть                                                         |
| PAYMENTS_CHAT_ID | chat_id куда отправлять информацию об оплатах                                                |
| DB_NAME          | Имя созданной таблицы (По умолчанию abcp)                                                    |
| DB_PASS          | Пароль к БД, который ввели на шагах выше                                                     |
| Настройки ABCP   | [Настройки ABCP](https://cp.abcp.ru/?page=allsettings&systemsettings&apiInformation)         |

#### Создайте виртуальное окружение и установите зависимости

```
python3 -m venv .venv
source /home/sample/.venv/bin/activate
pip install -r /home/sample/requirements.txt
```

#### Сделайте тестовый запуск

```
/home/sample/.venv/bin/python /home/sample/bot.py
```

#### Если всё успешно создайте сервис

```
nano /etc/systemd/system/abcp.service
```

В настройках User и Group не рекомендуется использовать пользователя root.     
На случай если пропустили создание пользователя при начальной настроке сервера

```
[Unit]
Description=Telegram Bot for online payments
After=network.target
After=system-postgresql.slice
After=postgresql@12-main.service
[Service]
User=root
Group=root

WorkingDirectory=/home/sample/
Environment="PYTHONPATH=/home/sample/"
ExecStart=/home/sample/.venv/bin/python /home/sample/bot.py
Restart=always
[Install]
WantedBy=multi-user.target
```

#### Активируйте и запустите сервис

```
systemctl enable abcp
systemctl start abcp
```