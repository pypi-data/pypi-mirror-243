#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2023/11/20 12:21
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  :

docker run --name aichat \
  -d --restart always \
  -p 39001:3000 \
  --add-host="host.docker.internal:host-gateway" \
  -e SQL_DSN="root:xxxxxxxxxxxxxxxx@tcp(host.docker.internal:3306)/oneapi" \
  -e TZ=Asia/Shanghai \
  -v /root/data/oneapi:/data \
  justsong/one-api

admin:
    image: nanjiren01/aichat-admin:latest
    container_name: aichat-admin
    restart: always
    depends_on:
      - db
      - redis
    environment:
      DB_URL: jdbc:mysql://aichat-db:3306/aichat?useSSL=false
      DB_USERNAME: root
      DB_PASSWORD: 123456
      REDIS_HOST: aichat-redis
      REDIS_PORT: 6379
      SUPERADMIN_USERNAME: aichat
      SUPERADMIN_PASSWORD: aichatadmin
      PASSWORD_SALT: any-is-ok
      DEFAULT_TOKENS: 3000
      DEFAULT_CHAT_COUNT: 20
      DEFAULT_ADVANCED_CHAT_COUNT: 2
      DEFAULT_DRAW_COUNT: 0
      MAIL_HOST: smtp.qq.com
      MAIL_PORT: 25
      MAIL_USERNAME: your-email-username
      MAIL_PASSWORD: your-email-password
      TZ: Asia/Shanghai
    ports:
      - "8082:8080"

