FROM alpine:3.19

WORKDIR /app

COPY requirements.txt .

RUN apk update && \
apk add --no-cache python3 py3-pip gcc musl-dev python3-dev libffi-dev openssl-dev cargo rust

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["python", "app.py"]