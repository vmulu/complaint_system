FROM python:3.14-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

ENV FLASK_APP=complaint_system.app

EXPOSE 5000

CMD ["sh", "-c", "flask db upgrade && flask run --host=0.0.0.0 --port=5000"]