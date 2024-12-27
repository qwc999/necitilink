FROM python:3.12-bullseye
WORKDIR /backend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt
RUN chmod 755 .
COPY . .
ENV TZ=Europe/Moscow
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]