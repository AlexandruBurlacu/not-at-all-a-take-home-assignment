FROM python:3.10-slim

WORKDIR /app
RUN useradd noroot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

USER noroot

CMD [ "uvicorn", "blog_api:app", "--host", "0.0.0.0" ]

EXPOSE 8000
