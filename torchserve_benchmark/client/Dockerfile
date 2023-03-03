FROM python:3.9

WORKDIR /code

RUN apt update -y \
     && apt-get install -y --no-install-recommends ffmpeg libsm6 libxext6

COPY ./torchserve_benchmark/client/requirements.txt /code/requirements.txt

RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./torchserve_benchmark/client/app /code/app

ENTRYPOINT ["python", "-u", "app/main.py"]