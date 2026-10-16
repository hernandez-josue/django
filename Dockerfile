# Imagen base: Python 3.11 mínima
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir Pillow==12.3.0 \
    && python -c "import PIL; from PIL import Image; print('Pillow OK:', PIL.__version__)"

# Copiar proyecto
COPY . .

# Archivos estáticos
RUN python manage.py collectstatic --no-input \
    --settings=core.settings \
    || echo "collectstatic con settings base"

# Puerto
EXPOSE 8000

# Migraciones + creación del administrador + Gunicorn
CMD python -m pip show Pillow && \
    python manage.py migrate --no-input && \
    python manage.py shell -c "import os; from django.contrib.auth import get_user_model; User=get_user_model(); username=os.environ.get('DJANGO_SUPERUSER_USERNAME'); email=os.environ.get('DJANGO_SUPERUSER_EMAIL'); password=os.environ.get('DJANGO_SUPERUSER_PASSWORD'); user,created=User.objects.get_or_create(username=username, defaults={'email':email}); user.email=email; user.is_staff=True; user.is_superuser=True; user.set_password(password); user.save()" && \
    gunicorn core.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-file -