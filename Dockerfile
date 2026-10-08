# Imagen base: Python 3.11 mínima
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias Python
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Recolectar archivos estáticos
RUN python manage.py collectstatic --no-input \
    --settings=core.settings \
    || echo "collectstatic con settings base"

# Exponer puerto
EXPOSE $PORT

# Ejecutar migraciones y después iniciar Gunicorn
CMD python manage.py migrate --no-input && \
    gunicorn core.wsgi \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --log-file -