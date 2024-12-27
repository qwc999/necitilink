from pydantic import BaseModel
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
from db.connection import connect_to_db, disconnect_from_db
from s3.operations import download_file
from db.models import Item, Category
from schemas import UserLogin, UserRegister, ItemToCart
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



# async def post_request(update: dict) -> None:
#     """Пример отправления JSON в топик request

#     Args:
#         update (dict): JSON
#     """
#     await broker.publish(update, topic="request", partition=4)

                
ITEMS_PER_PAGE = 18

async def post_http_request(addr: str, responce) -> httpx._models.Response:
    async with httpx.AsyncClient() as client:
        return await client.post(
            f"http://backend:8000{addr}", 
            data=responce,
            headers={"Content-Type": "application/json"}
        )
        
async def get_http_request(addr: str, responce = None) -> httpx._models.Response:
    async with httpx.AsyncClient() as client:
        return await client.get(
            f"http://backend:8000{addr}", 
            data=responce,
            headers={"Content-Type": "application/json"}
        )


async def get_all_products():
    return await Item.objects.all()


async def display_all_products_page(products, page):
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_page_products = products[start_idx:end_idx]
    for i in range(0, len(current_page_products), 3):
        cols = st.columns(3)
        for col, product in zip(cols, current_page_products[i:i + 3]):
            with col:
                st.image(product.img)
                st.subheader(product.name)
                st.write(f"{product.price}₽")
                if st.button("В корзину", key=f"all_add_{product.name}"):
                    await broker.publish(
                        ItemToCart(
                            item=product,
                            user_id=st.session_state.user_id
                            ).model_dump(), 
                        topic="add_to_cart")


async def display_category_products_page(products, page):
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_page_products = products[start_idx:end_idx]
    for i in range(0, len(current_page_products), 3):
        cols = st.columns(3)
        for col, product in zip(cols, current_page_products[i:i + 3]):
            with col:
                st.image(product.img)
                st.subheader(product.name)
                st.write(f"{product.price}₽")
                if st.button("В корзину", key=f"all_add_{product.name}"):
                    await broker.publish(
                        ItemToCart(
                            item=product,
                            user_id=st.session_state.user_id
                            ).model_dump(), 
                        topic="add_to_cart")


def display_basket_page(products, page):
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    current_page_products = products[start_idx:end_idx]
    for i in range(0, len(current_page_products), 3):
        cols = st.columns(3)
        for col, product in zip(cols, current_page_products[i:i + 3]):
            with col:
                st.image(product.img)
                st.subheader(product.name)
                st.write(f"{product.price}₽")
                if st.button("Удалить из корзины", key=f"basket_remove_{product.name}"):
                    pass


async def main():
    await connect_to_db()
    
    st.set_page_config(page_title="Shop", page_icon="🛒", layout="wide", initial_sidebar_state="auto")
    st.markdown(
        r"""<style>.stDeployButton {visibility: hidden;}</style>""", unsafe_allow_html=True
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
            products = await get_all_products()
            total_pages = (len(products) - 1) // ITEMS_PER_PAGE + 1

            if total_pages > 1:
                page = st.slider("Выберите страницу", min_value=0, max_value=total_pages - 1, step=1)
                await display_all_products_page(products, page)
            else:
                await display_all_products_page(products, 0)
                
        with tab2:
            st.header("Товары по категориям")
            products_list = [i.name for i in await Category.objects.all()]
            selected_category = st.selectbox("Выберите категорию:", products_list)
            if selected_category:
                products = await get_all_products()
                total_pages = (len(products) - 1) // ITEMS_PER_PAGE + 1

                if total_pages > 1:
                    page = st.slider("Выберите страницу", min_value=0, max_value=total_pages - 1, step=1, key="category_page")
                    await display_category_products_page(products, page)
                else:
                    await display_category_products_page(products, 0)

        with tab3:
            st.header("Корзина")
            basket_products = await get_all_products()[:10]
            total_pages = (len(basket_products) - 1) // ITEMS_PER_PAGE + 1
        if total_pages > 1:
            page = st.slider("Выберите страницу", min_value=0, max_value=total_pages - 1, step=1, key="basket_page")
            display_basket_page(basket_products, page)
        else:
            display_basket_page(basket_products, 0)

    else:
        tab1_1, tab1_2 = st.tabs([
            "Log in", "Sign In"
        ])

        with tab1_1:
            st.title("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                resp = await post_http_request(
                    "/login", 
                    responce=UserLogin(
                        email=email,
                        password=password
                    ).model_dump()
                )
                if resp.status_code != 200:
                    pass
                    #обработай ошибку
                elif resp.status_code == 200:
                    st.session_state.authenticated = True
                    st.session_state.user_id = resp.json["user_id"]
                

        with tab1_2:
            st.title("Sign In")
            username = st.text_input("Username", key="sign_in_user_name")
            register_email = st.text_input("Email", key="sign_in_email")
            password = st.text_input("Password", type="password", key="sign_in_password")
            if st.button("Sign In"):
                st.session_state.authenticated = True
                st.session_state.username = username
                resp = await post_http_request(
                    "/register", 
                    responce=UserRegister(
                        name=username,
                        email=register_email,
                        password=password
                    ).model_dump()
                )
                if resp.status_code != 200:
                    pass
                    #обработай ошибку
                elif resp.status_code == 200:
                    st.session_state.authenticated = True
                    st.session_state.user_id = resp.json["user_id"]


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(e, exc_info=e)
        
