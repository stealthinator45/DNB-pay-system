#!/bin/bash
echo "Setting up DNB Pay System..."

echo "Creating virtual environment..."
python3 -m venv dnb_venv

echo "Activating virtual environment..."
source dnb_venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating Django migrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate

echo "Populating dummy data..."
python manage.py populate_dnb_data --clear

echo "Setup complete!"
echo ""
echo "To start the server, run:"
echo "  source dnb_venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Login with: admin_dnb / admin123"
