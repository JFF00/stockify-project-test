FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --timeout=300 --retries=5 -r requirements.txt

COPY . .

RUN chmod +x manage.py

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]