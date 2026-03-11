import streamlit as st
import json
import os

# 1. Sayfa Yapılandırması (En üstte olmalı)
st.set_page_config(page_title="Food Innovation v5", page_icon="🍳")

# 2. Veri Yükleme ve Kaydetme Fonksiyonları
def load_data():
    if not os.path.exists('data.json'):
        return {}
    with open('data.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(new_data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4)

data = load_data()

# 3. Yan Menü (Sidebar) - Ekleme Formu Burada
st.sidebar.header("➕ Add New Ingredient")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_name = st.text_input("Ingredient Name:").capitalize()
    new_cat = st.selectbox("Category:", ["Vegetables", "Fruits", "Proteins", "Sweets", "Spices", "Other"])
    new_pairs = st.text_area("Pairings (Separate with commas):")
    submit = st.form_submit_button("Save to Library")

    if submit:
        if new_name and new_pairs:
            # Yazılanları listeye çeviriyoruz
            pair_list = [p.strip().capitalize() for p in new_pairs.split(",")]
            data[new_name] = {"pairings": pair_list, "category": new_cat}
            save_data(data)
            st.success(f"Added {new_name}!")
            st.rerun() # Sayfayı yenileyerek listeyi günceller

# 4. Ana Sayfa Arayüzü
st.title("👨‍🍳 Food Innovation Assistant")
st.markdown("Discover perfect flavor pairings for your culinary creations.")

search = st.text_input("Search an ingredient (e.g. Tomato):").capitalize()

if search:
    if search in data:
        item = data[search]
        st.success(f"### Results for {search}")
        
        col1, col2 = st.columns(2)
        col1.metric("Category", item['category'])
        
        st.write("**Recommended Pairings:**")
        # Şık butonlar/etiketler şeklinde gösterim
        for p in item['pairings']:
            st.info(f"✨ {p}")
    else:
        st.warning(f"I don't know '{search}' yet. You can add it using the sidebar!")

# Geliştirici Modu (İhtiyaç duyarsan açarsın)
if st.sidebar.checkbox("Show Library Details"):
    st.divider()
    st.write(f"Total items in library: {len(data)}")
    st.json(data)