FROM python:3.11-bookworm

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

COPY ./src /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
