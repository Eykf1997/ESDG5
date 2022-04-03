FROM python:3-slim
WORKDIR /usr/src/app
COPY ./activity_logs.reqs.txt ./
RUN python -m pip install --no-cache-dir -r activity_logs.reqs.txt
COPY ./activity_log.py ./amqp_setup.py ./
CMD [ "python", "./activity_log.py" ] 

