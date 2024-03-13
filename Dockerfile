FROM python:3.11

RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x .deploy/wait-for-db.sh

CMD [".deploy/wait-for-db.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]