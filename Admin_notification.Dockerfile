FROM python:3-slim
WORKDIR /usr/src/app
COPY Admin_notification.reqs.txt ./
RUN python -m pip install --no-cache-dir -r Admin_notification.reqs.txt
COPY ./Admin_notification.py ./amqp_setup.py ./
CMD [ "python", "./Admin_notification.py" ] 

