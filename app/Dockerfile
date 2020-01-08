# Base Stage
FROM python:3.7

COPY . /app
WORKDIR /app/app

RUN pip install -r requirements.txt
RUN pip install -r dev_requirements.txt

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["../serve.py"]