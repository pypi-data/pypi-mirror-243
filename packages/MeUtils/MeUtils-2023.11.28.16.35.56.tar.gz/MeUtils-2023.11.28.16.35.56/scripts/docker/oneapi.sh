#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2023/11/8 08:53
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : https://mp.weixin.qq.com/s/uOcaKQkNROTXqFuKA3hznQ

docker run --name oneapi \
  -d --restart always \
  -p 39001:3000 \
  --add-host="host.docker.internal:host-gateway" \
  -e SQL_DSN="root:xxxxxxxxxxxxxxxx@tcp(host.docker.internal:3306)/oneapi" -e TZ=Asia/Shanghai \
  -v /root/data/oneapi:/data \
  justsong/one-api

docker run --name vip \
  -d --restart always \
  -p 39002:3000 \
  --add-host="host.docker.internal:host-gateway" \
  -e SQL_DSN="root:chatllmchatllm@tcp(host.docker.internal:3306)/oneapi" -e TZ=Asia/Shanghai \
  -v /root/data/xapi:/data \
  calciumion/neko-api:main

docker run --name Xoneapi \
  -d --restart always \
  -p 39001:3000 \
  --add-host="host.docker.internal:host-gateway" \
  -e SQL_DSN="root:chatllmchatllm@tcp(host.docker.internal:3306)/oneapi" -e TZ=Asia/Shanghai \
  -v /root/data/xapi:/data \
  justsong/one-api
