FROM node:24-trixie-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ca-certificates python3 python3-pip

RUN pip install --break-system-packages workers-py uv
#RUN useradd -u 1000 ubuntu && mkdir /home/ubuntu && chown ubuntu:ubuntu /home/ubuntu
RUN mkdir /app && chown node:node /app

ENV WRANGLER_SEND_METRICS=false
ENV DO_NOT_TRACK=1

ADD src /app
WORKDIR /app
USER node

CMD ["bash"]