@echo off
echo Setting up DNB Pay System...

echo Creating virtual environment...
python -m venv dnb_venv

echo Activating virtual environment...
call dnb_venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Creating Django migrations...
python manage.py makemigrations

echo Applying migrations...
python manage.py migrate

echo Populating dummy data...
python manage.py populate_dnb_data --clear

echo Setup complete!
echo.
echo To start the server, run:
echo   dnb_venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Login with: admin_dnb / admin123
pause
