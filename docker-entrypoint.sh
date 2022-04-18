#!/bin/bash -x

python manage.py migrate --noinput || exit 1

#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'L!mouCloud786')" | python manage.py shell

exec "$@"