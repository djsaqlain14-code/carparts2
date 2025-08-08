import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

def inr_to_usd(inr):
    return round(inr / 82, 2)

def get_price_from_carparts(query):
    search_url = f"https://www.carparts.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Try common price selectors in order:
        price_selectors = [
            "span.actual-price",
            "span.price-sales",
            "div.price",
            "span.price",
        ]
        
        for selector in price_selectors:
            price_tag = soup.select_one(selector)
            if price_tag:
                price_text = price_tag.text.strip().replace("$", "").replace(",", "")
                try:
                    price = float(price_text)
                    return price
                except ValueError:
                    continue
        return None
    except Exception as e:
        return None


def add_gp(price_usd):
    gp_inr = random.randint(100, 250)
    gp_usd = inr_to_usd(gp_inr)
    final_price = round(price_usd + gp_usd, 2)
    return final_price

def detect_intent(text):
    text = text.lower()
    if "where" in text or "order" in text or "ship" in text:
        return "order_status"
    else:
        return "parts_search"

st.title("📞 Sam Used Auto Parts - Call Simulator")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.intent = None
    st.session_state.make_model_year_part = None

if st.session_state.step == 1:
    st.write("**Bot:** Sam Used Auto Parts, how can we help you today?")
    user_input = st.text_input("You say:")
    if user_input:
        intent = detect_intent(user_input)
        st.session_state.intent = intent
        if intent == "order_status":
            st.session_state.step = 10
        else:
            st.session_state.step = 2

if st.session_state.step == 10:
    st.write("**Bot:** Please hold while I connect you to our order support line.")
    st.stop()

if st.session_state.step == 2:
    st.write("**Bot:** Sure! Please tell me the make, model, year, and the part you need.")
    user_input = st.text_input("You say:")
    if user_input:
        st.session_state.make_model_year_part = user_input
        st.session_state.step = 3

if st.session_state.step == 3:
    query = st.session_state.make_model_year_part
    st.write(f"**Searching CarParts.com for:** {query}")
    price = get_price_from_carparts(query)
    if price:
        final_price = add_gp(price)
        st.write(f"**Bot:** We have an A-grade {query} for ${final_price}. Would you like to place the order?")
        st.session_state.step = 4
    else:
        st.write("**Bot:** Sorry, we couldn't find that part. Please try again or contact support.")
        st.session_state.step = 2

if st.session_state.step == 4:
    user_input = st.text_input("You say:")
    if user_input:
        if user_input.lower() in ["yes", "yeah", "yup", "sure", "order"]:
            st.write("**Bot:** Great! I'll proceed with your order and confirm details shortly. Thank you for choosing Sam Used Auto Parts!")
            st.session_state.step = 99
        else:
            st.write("**Bot:** Okay, let me know if you need anything else.")
            st.session_state.step = 2

if st.session_state.step == 99:
    st.write("**Call ended.**")

