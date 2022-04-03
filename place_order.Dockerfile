FROM python:3-slim
WORKDIR /usr/src/app
COPY place_order_reqs.txt ./
RUN python -m pip install --no-cache-dir -r place_order_reqs.txt
COPY ./telebotNotification.py ./place_order.py ./amqp_setup.py ./invokes.py ./
CMD [ "python", "./place_order.py" ] 

