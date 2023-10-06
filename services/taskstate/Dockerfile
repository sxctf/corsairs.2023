FROM python:3

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000

ENTRYPOINT ["./start.sh"]