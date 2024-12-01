FROM python:3.12-bullseye
WORKDIR /frontend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod 755 .
COPY . .
ENV TZ=Europe/Moscow
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]