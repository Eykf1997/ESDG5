FROM python:3-slim
WORKDIR /usr/src/app
COPY Inventory_Management_reqs.txt ./
RUN python -m pip install --no-cache-dir -r Inventory_Management_reqs.txt
COPY ./Inventory_Management.py ./amqp_setup.py ./invokes.py ./
CMD [ "python", "./Inventory_Management.py" ] 

