import streamlit as st
import json
import os
import random

# 1. Sayfa Yapılandırması
st.set_page_config(page_title="Chef's Innovation Assistant", page_icon="🍳", layout="wide")

# 2. Veri Fonksiyonları
def load_data():
    if not os.path.exists('data.json'):
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return {}
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        return {}

def save_data(new_data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)

data = load_data()

# --- GÖRSEL TEMA (CSS) ---
# --- MODERN FOOD INNOVATION THEME ---
st.markdown("""
    <style>
    /* Ana Arka Plan: Modern ve ferah bir fildişi/beyaz */
    .stApp {
        background-color: #FDFDFB;
    }
    
    /* Yan Menü: Hafif bitki yeşili tonu (Profesyonel ve sakin) */
    section[data-testid="stSidebar"] {
        background-color: #F1F4F0;
        border-right: 1px solid #E0E4DF;
    }

    /* Başlıklar: Derin Orman Yeşili (Güven ve doğallık verir) */
    h1, h2, h3 {
        color: #2D463E !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }

    /* Metinler: Okunabilirlik için çok koyu antrasit */
    .stMarkdown, p, b, label {
        color: #1A1C1E !important;
        font-size: 1.05rem;
    }

    /* Butonlar: Canlı Turuncu (İştah açıcı ve aksiyon çağrısı) */
    .stButton>button {
        background-color: #E67E22;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #D35400;
        transform: translateY(-2px);
    }

    /* Bilgi Kutuları: Soft Yeşil (Tazelik hissi) */
    .stAlert {
        background-color: #EBF2ED;
        color: #2D463E;
        border: 1px solid #D1DDD4;
    }

    /* Metricler (Kategoriler) */
    [data-testid="stMetricValue"] {
        color: #E67E22 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Yan Menü (Sidebar)
st.sidebar.title("👨‍🍳 Control Panel")

# --- Malzeme Ekleme Formu ---
st.sidebar.header("➕ Add New Ingredient")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_name = st.text_input("Name:").strip().capitalize()
    new_cat = st.selectbox("Category:", ["Vegetables", "Fruits", "Proteins", "Sweets", "Spices", "Other"])
    new_flavor = st.selectbox("Flavor Profile:", ["Neutral", "Sweet", "Sour", "Bitter", "Spicy", "Umami"])
    new_pairs = st.text_area("Pairings (comma separated):")
    submit = st.form_submit_button("Save to Library")

    if submit:
        if new_name and new_pairs:
            pair_list = [p.strip().capitalize() for p in new_pairs.split(",") if p.strip()]
            data[new_name] = {"pairings": pair_list, "category": new_cat, "flavor": new_flavor}
            save_data(data)
            st.sidebar.success(f"Added {new_name}!")
            st.rerun()

# --- Malzeme Silme ---
st.sidebar.header("🗑️ Management")
delete_target = st.sidebar.selectbox("Select to delete:", ["None"] + sorted(list(data.keys())))
if st.sidebar.button("Delete Selected"):
    if delete_target != "None":
        del data[delete_target]
        save_data(data)
        st.sidebar.warning(f"Deleted {delete_target}")
        st.rerun()

# 4. Ana Sayfa
st.title("🍳 Food Innovation Assistant")
st.write("Find the perfect match for your ingredients and spark your creativity!")

# --- SURPRISE ME BUTONU ---
if st.button("🎲 Surprise Me!"):
    if data:
        ri = random.choice(list(data.keys()))
        st.balloons()
        st.info(f"Today's Inspiration: **{ri}**")
        st.write(f"**Flavor:** {data[ri].get('flavor', 'Neutral')} | **Pairs with:** {', '.join(data[ri]['pairings'])}")

st.divider()

# --- ARAMA BÖLÜMÜ ---
search = st.text_input("What are you cooking with? (e.g., Tomato)").strip().capitalize()

if search:
    if search in data:
        item = data[search]
        st.success(f"### {search}")
        c1, c2 = st.columns(2)
        c1.metric("Category", item['category'])
        c2.metric("Flavor Profile", item.get('flavor', 'Neutral'))
        
        st.write("**Best Pairings:**")
        cols = st.columns(3)
        for idx, p in enumerate(item['pairings']):
            cols[idx % 3].info(f"✨ {p}")
    else:
        st.warning(f"'{search}' is not in the library yet. You can add it from the sidebar!")

# Alt Bilgi / Debug
if st.sidebar.checkbox("Developer Mode"):
    st.write("### Database Preview")
    st.json(data)