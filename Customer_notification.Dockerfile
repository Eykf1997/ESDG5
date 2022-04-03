FROM python:3-slim
WORKDIR /usr/src/app
COPY ./Customer_notification.reqs.txt ./
RUN python -m pip install --no-cache-dir -r Customer_notification.reqs.txt
RUN pip install google
COPY ./Customer_notification.py ./amqp_setup.py ./Google.py ./ client_secret.json ./
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
CMD [ "python", "./Customer_notification.py" ] 

