# Installation
*NOTE:* following code only applies to manjaro

#### 1. install `poetry`
`sudo pacman -S python-poetry`

#### 2. install `mariadb` or `msql
- `sudo pacman -S mariadb`
- `sudo systemctl start mysqld`
- `sudo mysql_install_db --user=mysql --basedir=/usr --datadir=/var/lib/mysql`
- `sudo systemctl start mysqld && sudo mysql_secure_installation`

#### 3. setup database
- `sudo mysql -u root -p` (you should be in mysql shell)
- `create database rawr_db;`
- `create user rawr@localhost identified by 'ollave123';`
- `grant all privileges on rawr_db.* to rawr@localhost;`

#### 4. install dependencies
`poetry install`

#### 5. turn on virtual environment
`poetry shell`

#### 6. install pre-commit
`pre-commit install`

#### 7. migrate django
`python manage.py migrate`
