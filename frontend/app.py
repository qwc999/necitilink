import streamlit as st
import asyncio
import httpx
from faststream import FastStream
from faststream.kafka import KafkaBroker
from faststream.security import SASLPlaintext
from config.logger import logger
from config.settings import (
    KAFKA_URL,
    KAFKA_PASSWORD,
    KAFKA_USERNAME
)

# Отсюда 
security = SASLPlaintext(
    username=KAFKA_USERNAME,
    password=KAFKA_PASSWORD,
    use_ssl=False
)
broker = KafkaBroker(
    KAFKA_URL,
    security=security
    )
stream = FastStream(broker)
# до сюда не трогать



async def post_request(update: dict) -> None:
    """Пример отправления JSON в топик request

    Args:
        update (dict): JSON
    """
    await broker.publish(update, topic="request", partition=4)


async def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    if st.session_state.authenticated:
        st.sidebar.button("Logout")
        # st.sidebar.button("Logout", on_click=logout)
        st.sidebar.write(f"Welcome, {st.session_state.username}!")
        st.sidebar.write(f"Role: {st.session_state.role}")

        tab1, tab2, tab3 = st.tabs([
            "Все товары", "Товары по категориям", "Корзина"
        ])

        with tab1:
            st.header("Все товары")

        with tab2:
            st.header("Товары по категориям")

        with tab3:
            st.header("Корзина")

    else:
        st.title("Login")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            async with httpx.AsyncClient() as client:
                # Use client for requests here    
                resp = await client.post(
                    "https://localhost:8000/login", 
                    json={
                    "username": username,
                    "email": email,
                    "password": password
                })
            # auth_result = authenticate(username, password)
            st.session_state.authenticated = True
            st.session_state.username = username
            st.query_params.authenticated = "true"


if __name__ == "__main__":
    asyncio.run(main())
