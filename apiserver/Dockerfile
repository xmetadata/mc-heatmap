# python:alpine is 3.{latest}
FROM python:alpine

LABEL maintainer="PaaS.ST"

COPY . /src

RUN pip install -r /src/requirements.txt

EXPOSE 5050

ENTRYPOINT ["python", "/src/app.py"]
