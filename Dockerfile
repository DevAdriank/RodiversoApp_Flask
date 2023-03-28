FROM python:3.10.4

COPY requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y unixodbc-dev
RUN pip install -r /app/requirements.txt

COPY . /app/

WORKDIR /app

CMD ["python", "flask_app.py"]