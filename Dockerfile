FROM python:3.8.16-alpine
MAINTAINER wangcw
USER root

ENV TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.mirrors.ustc.edu.cn/simple"

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update \
    && apk --update add --no-cache gcc g++ tzdata libffi-dev libxslt-dev \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

COPY . .

WORKDIR /logs
WORKDIR /apiwong

RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip \
    && pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt \
    && chmod +x entrypoint.sh \
EXPOSE 80
ENTRYPOINT [ "sh","entrypoint.sh" ]
