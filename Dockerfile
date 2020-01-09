FROM registry.cn-hangzhou.aliyuncs.com/chenxl/python3.6
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install  -r requirements.txt

CMD ["python", "./block_number_producer.py"]
