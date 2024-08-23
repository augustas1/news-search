FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt

COPY ./__init__.py /code/__init__.py
COPY ./database.py /code/database.py
COPY ./sqs.py /code/sqs.py

COPY ./search_api/__init__.py /code/search_api/__init__.py
COPY ./search_api/search_api.py /code/search_api/search_api.py

CMD ["fastapi", "run", "search_api/search_api.py"]