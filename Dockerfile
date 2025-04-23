FROM python:3.9-slim

WORKDIR /app

COPY main.py ./

RUN pip install requests python-dotenv

CMD ["python", "main.py"]