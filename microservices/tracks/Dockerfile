# start by pulling the python image
FROM python:3.8-alpine

# switch working directory
WORKDIR /app

RUN pip install flask
RUN pip install flask_api
RUN pip install flask_restful
RUN pip install flask_sqlalchemy
RUN pip install psycopg2-binary

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

EXPOSE 5000

CMD ["tracksService.py"]