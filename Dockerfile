FROM python:3.8.16-alpine
MAINTAINER wangcw
USER root

ENV TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.mirrors.ustc.edu.cn/simple"

RUN echo http://mirrors.aliyun.com/alpine/v3.12/main > /etc/apk/repositories \
    && echo http://mirrors.aliyun.com/alpine/v3.12/community >> /etc/apk/repositories \
    && apk update \
    && apk --update add --no-cache gcc \
    && apk --update add --no-cache g++ \
    && apk --update add --no-cache tzdata \
    && apk --update add --no-cache libffi-dev \
    && apk --update add --no-cache libxslt-dev \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \

WORKDIR /logs
WORKDIR /apiwong

COPY . .

RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip \
    && pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt \
    && chmod +x entrypoint.sh
ENTRYPOINT [ "sh","entrypoint.sh" ]
