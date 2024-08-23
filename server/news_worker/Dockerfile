FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./__init__.py /code/server/__init__.py
COPY ./database.py /code/server/database.py
COPY ./sqs.py /code/server/sqs.py

COPY ./news_worker/article_queue.py /code/server/news_worker/article_queue.py
COPY ./news_worker/news_worker.py /code/server/news_worker/news_worker.py

CMD ["python", "-m", "server.news_worker.news_worker"]