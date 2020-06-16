FROM registry.cn-hangzhou.aliyuncs.com/chenxl/python3.6
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install  -r requirements.txt
COPY . /usr/src/app


CMD ["python", "./block_number_producer.py"]
