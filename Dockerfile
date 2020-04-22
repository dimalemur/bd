FROM python:3.6

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

ENV PATH=$PATH:/usr/src/app/
ENV PYTHONPATH /usr/src/app/
ENV TZ Europe/Moskow
ENV  POSTGRES = postgres:alpine


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
EXPOSE 5432


CMD ["python","app.py"]

