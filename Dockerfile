FROM python:3.10-slim

WORKDIR /app
ENTRYPOINT [ "python", "-u" ]
RUN useradd noroot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY blog_api.py .

USER noroot

CMD [ "-m", "uvicorn", "blog_api:app", "--host", "0.0.0.0" ]

EXPOSE 8000
