# Media library - Django application

This project is a media library app with two applications inside, one for public where they can 
consult library's medias. A second application reserved for librarians only where they can manage medias,
 members and borrowings. Medias available in this library are books, CD, DVD and parlour games.

---

## Main features

- Public application
  - Media research
- Librarians application
  - CRUD interface for medias management
  - CRUD interface for members management
  - Create new borrowings and save return
  - Borrowings specificities
    - No borrowing for parlour games
    - No more than three current borrowings per members
    - A member has one week to return the media. If he's late returning media, he's blocked
    - A blocked member can't have new borrowing even if he has less than three current borrowings

---

## Technologies

- IDE : [PyCharm](https://www.jetbrains.com/fr-fr/pycharm/download/?section=windows)
- [Python](https://www.python.org/downloads/)


- Django 5.1.7
- HTML / CSS for Django templates
- JavaScript
- [XAMPP](https://www.apachefriends.org/fr/download.html) with [MariaDB 11.4.5](https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.4.5&os=windows&cpu=x86_64&pkg=msi&mirror=starburst_portsmouth) for the database

---

## Local installation

1. **Download project**

Go [here](https://github.com/fb-lb/CEF_devoirs_mediatheque)
Click on green button 'Code' and 'Download ZIP'
Extract files

2. **Virtual environment**

In the terminal, go to the project's root

*Creation*
```bash
python -m venv venv
```

*Activation*
```bash
venv\Scripts\activate
```
(now you see (venv) before the path in the terminal)

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create your database**

With Xampp interface, activate Apache and MySQL and go to [PHPMyAdmin](http://localhost/phpmyadmin/)
Be sure that MariaDB version is 10.5 or newer

Create the database with utf8mb4_general_ci character set, keep the name of the database,
you will need it for the next step.

Then create a sql_user for this database. Keep the name of the sql_user and the password, you will need them in the next step
Give all privileges to this user on the database you've just created

5. **Environment variables**

Go back to the root project and create a `.env` file
Inside this file put :
```.env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DB_USER=sql_user
DJANGO_DB_PASSWORD=your_mysql_password
DJANGO_DB_HOST=your_database_host
DJANGO_DB_PORT=your_database_port
MYSQL_DATABASE=your_database_name
DJANGO_SSL_MODE=your_database_connection_ssl_mode
```
Values for DJANGO_SSL_MODE :  
DISABLED | PREFERRED | REQUIRED | VERIFY_CA | VERIFY_IDENTITY

To generate a valid Django secret key, run this command in the terminal :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

5. **Database initialization**
```bash
python manage.py migrate
```

6. **Use fixtures to fill th database**
```bash
python manage.py loaddata librarians_app/fixtures/users.json
python manage.py loaddata librarians_app/fixtures/members.json
python manage.py loaddata librarians_app/fixtures/medias.json
```

7. **Static files collect**
```bash
python manage.py collectstatic
```

8. **Run server**
```bash
python manage.py runserver
```

9. **Run tests**
```bash
pytest
```

10. **Enjoy**

Now you can use this application.

To connect to the librarians_app, use :
- ID : Notre_livre_notre_media
- Password : librarian

To connect to [Django admin](http://localhost:8000/admin/login/?next=/admin/) with super user, use :
- ID : super_librarian
- Password : new_librarian