FROM registry.cn-beijing.aliyuncs.com/fww/api-async-base:2025.04.25.17.32

WORKDIR /app

COPY . .

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

CMD [ "uvicorn","app.main:app","--host","0.0.0.0","--port","80"]

# CMD ["sh", "-c", "while true; do sleep 1; done"]