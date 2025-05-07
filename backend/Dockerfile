FROM python:3.12-slim

# Install PostgreSQL build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["/wait-for-db.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]