# start by pulling the python image
FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install -y python3-pip python3-dev \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy application content from the local file to the container
COPY ./app .

# expose listening port
EXPOSE 5000

# configure the container to run in an executed manner
CMD ["python3", "app.py" ]