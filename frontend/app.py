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
from s3.operations import download_file
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

def add_to_basket():
    pass


def get_all_products():
    return [
        {"name": "Product 1", "price": 100, "description": "Description 1"},
        {"name": "Product 2", "price": 200, "description": "Description 2"},
        {"name": "Product 3", "price": 300, "description": "Description 3"},
        {"name": "Product 4", "price": 400, "description": "Description 4"},
        {"name": "Product 5", "price": 500, "description": "Description 5"},
        {"name": "Product 6", "price": 600, "description": "Description 6"},
    ]
    


async def main():
    st.set_page_config(page_title="Shop", page_icon="🛒", layout="wide", initial_sidebar_state="auto")
    st.markdown(
        r"""
        <style>
        .stDeployButton {
                visibility: hidden;
            }
        </style>
        """, unsafe_allow_html=True
    )

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None

    if st.session_state.authenticated:
        st.sidebar.button("Logout")
        st.sidebar.write(f"Welcome, {st.session_state.username}!")
        st.sidebar.write(f"Role: {st.session_state.role}")

        tab1, tab2, tab3 = st.tabs([
            "Все товары", "Товары по категориям", "Корзина"
        ])

        with tab1:
            st.header("Все товары")
            products = get_all_products()
            for i in range(0, len(products), 3):
                cols = st.columns(3)
                for col, product in zip(cols, products[i:i+3]):
                    with col:
                        st.image("image.png")
                        st.subheader(product["name"])
                        st.write(f"{product['price']}₽")
                        if st.button("В корзину", key=f"add_{product['name']}"):
                            # add_to_basket(product['id'])
                            pass

        with tab2:
            st.header("Товары по категориям")
            products_list = ['PC - Гарнитуры/Наушники', 'Аксессуары - PS2', 'Аксессуары - PS3', 'Аксессуары - PS4',
                             'Аксессуары - PSP', 'Аксессуары - PSVita', 'Аксессуары - XBOX 360',
                             'Аксессуары - XBOX ONE', 'Билеты (Цифра)', 'Доставка товара', 'Игровые консоли - PS2',
                             'Игровые консоли - PS3', 'Игровые консоли - PS4', 'Игровые консоли - PSP',
                             'Игровые консоли - PSVita', 'Игровые консоли - XBOX 360', 'Игровые консоли - XBOX ONE',
                             'Игровые консоли - Прочие', 'Игры - PS2', 'Игры - PS3', 'Игры - PS4', 'Игры - PSP',
                             'Игры - PSVita', 'Игры - XBOX 360', 'Игры - XBOX ONE', 'Игры - Аксессуары для игр',
                             'Игры Android - Цифра', 'Игры MAC - Цифра', 'Игры PC - Дополнительные издания',
                             'Игры PC - Коллекционные издания', 'Игры PC - Стандартные издания', 'Игры PC - Цифра',
                             'Карты оплаты (Кино, Музыка, Игры)', 'Карты оплаты - Live!',
                             'Карты оплаты - Live! (Цифра)', 'Карты оплаты - PSN', 'Карты оплаты - Windows (Цифра)',
                             'Кино - Blu-Ray', 'Кино - Blu-Ray 3D', 'Кино - Blu-Ray 4K', 'Кино - DVD',
                             'Кино - Коллекционное', 'Книги - Артбуки, энциклопедии', 'Книги - Аудиокниги',
                             'Книги - Аудиокниги (Цифра)', 'Книги - Аудиокниги 1С', 'Книги - Бизнес литература',
                             'Книги - Комиксы, манга', 'Книги - Компьютерная литература',
                             'Книги - Методические материалы 1С', 'Книги - Открытки',
                             'Книги - Познавательная литература', 'Книги - Путеводители',
                             'Книги - Художественная литература', 'Книги - Цифра',
                             'Музыка - CD локального производства', 'Музыка - CD фирменного производства',
                              'Музыка - MP3', 'Музыка - Винил', 'Музыка - Музыкальное видео',
                             'Музыка - Подарочные издания', 'Подарки - Атрибутика', 'Подарки - Гаджеты, роботы, спорт',
                             'Подарки - Мягкие игрушки', 'Подарки - Настольные игры',
                             'Подарки - Настольные игры (компактные)', 'Подарки - Открытки, наклейки',
                             'Подарки - Развитие', 'Подарки - Сертификаты, услуги', 'Подарки - Сувениры',
                             'Подарки - Сувениры (в навеску)', 'Подарки - Сумки, Альбомы, Коврики д/мыши',
                             'Подарки - Фигурки', 'Программы - 1С:Предприятие 8', 'Программы - MAC (Цифра)',
                             'Программы - Для дома и офиса', 'Программы - Для дома и офиса (Цифра)',
                             'Программы - Обучающие', 'Программы - Обучающие (Цифра)', 'Служебные',
                             'Служебные - Билеты', 'Чистые носители (шпиль)', 'Чистые носители (штучные)',
                             'Элементы питания']
        selected_category = st.selectbox("Выберите категорию:", products_list)
        if selected_category:
            # products = get_all_products_from_category(selected_category)
            products = get_all_products()
            for i in range(0, len(products), 3):
                cols = st.columns(3)
                for col, product in zip(cols, products[i:i + 3]):
                    with col:
                        st.image("image.png")
                        st.subheader(product["name"])
                        st.write(f"{product['price']}₽")
                        if st.button("В корзину", key=f"add_category{product['name']}"):
                            # add_to_basket(product['id'])
                            pass

        with tab3:
            st.header("Корзина")
            basket_products = get_all_products()
            for i in range(0, len(basket_products), 3):
                cols = st.columns(3)
                for col, product in zip(cols, basket_products[i:i+3]):
                    with col:
                        st.image("image.png")
                        st.subheader(product["name"])
                        st.write(f"{product['price']}₽")
            if st.button("Оплатить", key=f"pay"):
                pass

    else:
        tab1_1, tab1_2 = st.tabs([
            "Log in", "Sign In"
        ])

        with tab1_1:
            st.title("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                '''async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://localhost:8000/login",
                        json={
                            "username": username,
                            "email": None,
                            "password": password
                        })'''
                st.session_state.authenticated = True
                st.session_state.username = username

        with tab1_2:
            st.title("Sign In")
            username = st.text_input("Username", key="sign_in_user_name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password", key="sign_in_password")
            if st.button("Sign In"):
                '''async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        "https://localhost:8000/signin",
                        json={
                            "username": username,
                            "email": email,
                            "password": password
                        })'''
                st.session_state.authenticated = True
                st.session_state.username = username


if __name__ == "__main__":
    asyncio.run(main())
