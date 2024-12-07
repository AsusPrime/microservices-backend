FROM python:3.14.0a2-slim-bullseye
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "telegram_bot.py"]