FROM python:3.9.1-alpine
LABEL maintainer="Filip Górczyński <filip.gorczynski.services@gmail.com>"

RUN mkdir -p /usr/src/app
# Set working directory
WORKDIR /usr/src/app

# Set environment variables in Docker Image
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install PostgreSQL dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

# Set entrypoint.sh +x
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
