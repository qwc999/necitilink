FROM python:3.12-bullseye
WORKDIR /backend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod 755 .
COPY . .
ENV TZ=Europe/Moscow
CMD ["python", "app.py"]