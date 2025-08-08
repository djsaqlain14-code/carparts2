import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import random

# Replace with your OpenAI key
openai.api_key = "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx"

# Currency conversion approx: 1 USD = 83 INR
INR_TO_USD = 1/83

# ---------------------
# Functions
# ---------------------

def get_price_from_carparts(query):
    search_url = f"https://www.carparts.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
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
    except Exception:
        return None

def calculate_gp():
    # Random GP in INR converted to USD
    gp_inr = random.randint(100, 250)
    return round(gp_inr * INR_TO_USD, 2)

# ---------------------
# Streamlit UI
# ---------------------

st.set_page_config(page_title="Car Parts Price Bot Demo", page_icon="🚗")
st.title("🚗 Car Parts Price Bot Demo")

st.markdown("""
Type your car part request like:  
**2018 Toyota Camry alternator**  
Then click **Get Price**.
""")

part_query = st.text_input("Enter part details:", key="part_input")

if st.button("Get Price", key="get_price_btn"):
    if not part_query.strip():
        st.warning("Please enter a part name.")
    else:
        with st.spinner("Searching carparts.com..."):
            selling_price = get_price_from_carparts(part_query)
            if selling_price:
                gp = calculate_gp()
                final_price = selling_price + gp
                st.success(f"We have an A-grade {part_query} for ${selling_price:.2f}.")
                st.info(f"Our added profit is approx ${gp:.2f}, so total price for you is ${final_price:.2f}.")
                st.write("Would you like to order?")
            else:
                st.error("Sorry, we couldn't find that part. Please try again or contact support.")
