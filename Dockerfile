FROM python:3.11.5

# USER 1000:1000

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["python","src/main.py"]