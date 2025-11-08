FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads

EXPOSE 5000

ENV FLASK_APP=run.py
ENV PYTHONBUFFERED=1

CMD ["python", "run.py"]