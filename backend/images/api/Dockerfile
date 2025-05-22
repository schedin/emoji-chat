FROM docker.io/library/python:3.12

# RUN apt-get update && \
#     apt-get install -y gcc mariadb-client libmariadb-dev-compat libmariadb-dev && \
#     apt-get clean

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

COPY src /app

EXPOSE 8000

CMD ["python", "main.py"]
