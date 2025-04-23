FROM python:3.13-alpine

WORKDIR /app

COPY main.py ./

RUN pip install requests python-dotenv

CMD ["python", "main.py"]