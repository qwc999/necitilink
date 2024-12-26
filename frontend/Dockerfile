FROM python:3.12-bullseye
WORKDIR /frontend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --root-user-action=ignore -r requirements.txt
RUN chmod 755 .
COPY . .
ENV TZ=Europe/Moscow
CMD ["streamlit", "run", "app.py",  "--server.port", "3000"]