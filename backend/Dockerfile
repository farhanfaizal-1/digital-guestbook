
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

ENV DATA_FILE=/data/guestbook.json

EXPOSE 5000

CMD ["python", "app.py"]


