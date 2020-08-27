release: python manage.py migrate
web: gunicorn backend.wsgi --log-file -
web: npm run start
