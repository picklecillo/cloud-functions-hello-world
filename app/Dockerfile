FROM python:3.7

COPY . /function
WORKDIR /function

RUN pip install -r function/requirements.txt
RUN pip install -r function/dev_requirements.txt
RUN pip install .

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["serve.py"]
