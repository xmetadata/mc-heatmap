# python:2.7-alpine is 2.{latest}
FROM python:2.7-alpine

LABEL maintainer="PaaS.ST"

RUN echo "http://mirrors.ustc.edu.cn/alpine/v3.3/main/" > /etc/apk/repositories && apk add alpine-sdk && pip install -r /src/requirements.txt

EXPOSE 5050

ENTRYPOINT ["python", "/src/app.py", "runserver"]
