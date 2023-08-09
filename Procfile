web: daphne ProjectGo.asgi:application --port $PORT --bind 0.0.0.0
release: python manage.py migrate
worker: python manage.py collectstatic --noinput