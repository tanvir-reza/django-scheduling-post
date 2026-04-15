#!/usr/bin/env bash

# source .venv/bin/activate

echo "Please choose operation:"
echo "1. Run Server"
echo "2. Run Celery Worker"
echo "3. Run Celery Beat"
echo "4. DB Migration"
read -p "Enter your choice (1 ,2, 3, 4): " action_choice


case $action_choice in 
  1)  # Run server
    echo "Run server"
    source .venv/bin/activate
    uvicorn core.asgi:application --host 0.0.0.0 --port 8000 --reload 
    ;;
  2)  # Run Celery Worker
    echo "Run Celery Worker"
    source .venv/bin/activate
    celery -A core worker --loglevel=info
    ;;
  3)  # Run Celery Worker
    echo "Run Celery Worker"
    source .venv/bin/activate
    celery -A core beat --loglevel=info
    ;;
  4)  #Migrate Server
    source .venv/bin/activate
    python manage.py makemigrations --noinput
    python manage.py migrate_schemas --noinput
    ;;
  *)  # Invalid choice
    echo "Invalid choice. Please enter 1 for Backup or 2 for Restore."
    ;;
esac