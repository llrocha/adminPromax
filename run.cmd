REM call ..\..\..\virtualenv\django_1.11\Scripts\activate.bat
REM python manage.py runserver

python -m pip install virtualenv --upgrade
python -m virtualenv virtualenv
call virtualenv\Scripts\activate.bat
python -m pip install -r requirements.txt
python manage.py runserver