FROM python:3.8-slim-buster

RUN mkdir /app
WORKDIR app

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY . .

ENTRYPOINT gunicorn -b 0.0.0.0:$PORT app.app:app --workers $WORKERS
