FROM python:latest
RUN apt-get update -y && apt-get install -y build-essential && apt-get install libmariadb3 libmariadb-dev -y
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 5000
# ENTRYPOINT [ "python3"]
# CMD ["app.py" ]
ENTRYPOINT ["./start.sh"]
