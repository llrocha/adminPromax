REM call ..\..\..\virtualenv\django_1.11\Scripts\activate.bat
REM python manage.py runserver

python -m virtualenv virtualenv
call virtualenv\Scripts\activate.bat
pip instal -r requirements.txt
python manage.py runserver