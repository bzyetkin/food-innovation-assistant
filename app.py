import streamlit as st
import json
import os
import random
import pandas as pd # Excel/CSV işlemleri için gerekli

# 1. Sayfa Yapılandırması
st.set_page_config(page_title="R&D Food Lab", page_icon="🧪", layout="wide")

# 2. Veri Fonksiyonları
def load_data():
    if not os.path.exists('data.json'):
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump({}, f)
        return {}
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except: return {}

def save_data(new_data):
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)

data = load_data()

# --- GÖRSEL TEMA ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    h1, h2 { color: #1B4332 !important; }
    .stButton>button { background-color: #2D6A4F; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Yan Menü (Sidebar)
st.sidebar.title("🧪 R&D Control Center")

# --- TOPLU VERİ YÜKLEME (CSV/EXCEL) ---
st.sidebar.header("📂 Bulk Import (Excel/CSV)")
uploaded_file = st.sidebar.file_uploader("Upload your ingredient list", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        if st.sidebar.button("Process & Import File"):
            for index, row in df.iterrows():
                name = str(row['Name']).strip().capitalize()
                # Excel'deki sütunları JSON yapımıza eşliyoruz
                data[name] = {
                    "pairings": [p.strip().capitalize() for p in str(row['Pairings']).split(",")],
                    "category": row['Category'],
                    "flavor": row['Flavor'],
                    "fat_content": int(row['Fat']),
                    "texture": row['Texture'],
                    "function": row['Function']
                }
            save_data(data)
            st.sidebar.success(f"Successfully imported {len(df)} items!")
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error: Check column names! {e}")

# --- TEKİL VERİ EKLEME FORMU ---
st.sidebar.divider()
st.sidebar.header("➕ Add Single Ingredient")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_name = st.text_input("Name:").strip().capitalize()
    new_cat = st.selectbox("Category:", ["Proteins", "Lipids", "Carbs", "Dairy", "Spices", "Additives", "Other"])
    new_flavor = st.selectbox("Flavor:", ["Neutral", "Sweet", "Sour", "Bitter", "Spicy", "Umami"])
    new_fat = st.slider("Fat Content (%)", 0, 100, 0)
    new_texture = st.selectbox("Texture:", ["Liquid", "Powder", "Creamy", "Solid", "Gel"])
    new_function = st.selectbox("Function:", ["Base", "Emulsifier", "Thickener", "Flavoring"])
    new_pairs = st.text_area("Pairings (comma separated):")
    submit = st.form_submit_button("Save to Library")

    if submit and new_name:
        pair_list = [p.strip().capitalize() for p in new_pairs.split(",") if p.strip()]
        data[new_name] = {
            "pairings": pair_list, "category": new_cat, "flavor": new_flavor,
            "fat_content": new_fat, "texture": new_texture, "function": new_function
        }
        save_data(data)
        st.sidebar.success(f"Registered: {new_name}")
        st.rerun()

# --- SİLME ---
delete_target = st.sidebar.selectbox("Delete Item:", ["None"] + sorted(list(data.keys())))
if st.sidebar.button("Delete"):
    if delete_target != "None":
        del data[delete_target]
        save_data(data)
        st.rerun()

# 4. Ana Sayfa
st.title("🧪 Food Innovation & R&D Lab")
st.write("Professional formulation and ingredient pairing analysis.")

# ARAMA
search = st.text_input("Search technical database:").strip().capitalize()

if search:
    if search in data:
        item = data[search]
        st.success(f"### TECHNICAL DATA: {search}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Fat Content", f"%{item.get('fat_content', 0)}")
        c2.metric("Function", item.get('function', 'N/A'))
        c3.metric("Category", item['category'])
        
        st.write(f"**Texture Profile:** {item.get('texture', 'N/A')} | **Flavor:** {item.get('flavor', 'N/A')}")
        
        st.divider()
        st.write("**R&D Pairing Suggestions:**")
        cols = st.columns(4)
        for idx, p in enumerate(item['pairings']):
            cols[idx % 4].info(f"🧬 {p}")
    else:
        st.warning("Ingredient not found in R&D database.")

# Developer Mode
if st.sidebar.checkbox("Show Raw Database"):
    st.json(data)