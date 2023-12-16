FROM python:3.9

WORKDIR /api
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY . /api/app

CMD ["uvicorn", "app.db_api.main:app", "--host", "0.0.0.0", "--port", "9000"]