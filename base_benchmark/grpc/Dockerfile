FROM python:3.9

WORKDIR /code

COPY ./base_benchmark/grpc/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./base_benchmark/grpc/app /code/app

EXPOSE 50051

CMD ["python", "app/main.py"]
