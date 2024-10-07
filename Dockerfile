FROM python:3.8

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

RUN alembic upgrade head

WORKDIR src

CMD ["gunicorn -w 4 -k uvicorn.workers.UvicornWorker \"main:app\" -b 0.0.0.0:8000"]