import streamlit as st
import json

# Sayfa Ayarları
st.set_page_config(page_title="Food Innovation Assistant", page_icon="🍳")

def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

# Başlık ve Açıklama
st.title("🍳 Food Innovation Assistant")
st.markdown("Discover perfect flavor pairings and create innovative dishes!")

data = load_data()

# Kullanıcı Girişi
ingredient = st.text_input("Enter an ingredient (e.g., Tomato, Chocolate):").capitalize()

if ingredient:
    if ingredient in data:
        st.success(f"### {ingredient} pairs perfectly with:")
        # Eşleşmeleri görsel kartlar gibi gösterelim
        pairings = data[ingredient]
        cols = st.columns(len(pairings))
        for i, item in enumerate(pairings):
            cols[i].info(item)
    else:
        st.warning(f"I don't have info for '{ingredient}' yet.")
        new_pair = st.text_input(f"What goes well with {ingredient}? (Separate with commas)")
        if st.button("Teach Me!"):
            if new_pair:
                new_list = [item.strip().capitalize() for item in new_pair.split(",")]
                data[ingredient] = new_list
                save_data(data)
                st.success("Thanks! I've learned a new pairing!")
                st.rerun()

# Alt Bilgi
st.divider()
st.caption("Powered by Python & Streamlit | Innovation in the Kitchen")