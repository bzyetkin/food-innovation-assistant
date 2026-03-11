import streamlit as st
import json
import os
import random  # <-- Bu yeni satırı ekle
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
    new_flavor = st.selectbox("Flavor Profile:", ["Neutral", "Sweet", "Sour", "Bitter", "Spicy", "Umami"])
    new_pairs = st.text_area("Pairings (Separate with commas):")
    submit = st.form_submit_button("Save to Library")
    # --- SIDEBAR: MALZEME SİLME ---
st.sidebar.header("🗑️ Delete Ingredient")
delete_target = st.sidebar.selectbox("Select to delete:", ["None"] + list(data.keys()))
if st.sidebar.button("Delete from Library"):
    if delete_target != "None":
        del data[delete_target]
        save_data(data)
        st.sidebar.success(f"Removed {delete_target}!")
        st.rerun()

    if submit:
        if new_name and new_pairs:
            # 1. İsmi ve eşleşmeleri temizle (Boşlukları sil)
            clean_name = new_name.strip().capitalize()
            pair_list = [p.strip().capitalize() for p in new_pairs.split(",") if p.strip()]
            
            # 2. Veriyi belleğe (data sözlüğüne) ekle
            data[clean_name] = {
                "pairings": pair_list, 
                "category": new_cat, 
                "flavor": new_flavor
            }
            
            # 3. Dosyaya yaz ve mutlaka kaydet
            save_data(data)
            
            # 4. Başarı mesajı ver ve sayfayı ZORLA yenile
            st.sidebar.success(f"✅ {clean_name} added to database!")
            st.rerun() 
        else:
            st.sidebar.error("⚠️ Please fill in all fields!")
# 4. Ana Sayfa Arayüzü
st.title("👨‍🍳 Food Innovation Assistant")
st.markdown("Discover perfect flavor pairings for your culinary creations.")

search = st.text_input("Search an ingredient (e.g. Tomato):").capitalize()
# --- SURPRISE ME SECTION ---
if st.button("🎲 Surprise Me! (Get Inspired)"):
    if data:
        # Kütüphaneden rastgele bir malzeme seç
        random_ingredient = random.choice(list(data.keys()))
        
        # Kutlama efektleri
        st.balloons() 
        
        # Sonucu şık bir kutuda göster
        st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border-left: 5px solid #ff4b4b;">
            <h3 style="margin:0;">Today's Inspiration: {random_ingredient}</h3>
            <p style="font-size:18px;">Try pairing it with: <b>{", ".join(data[random_ingredient]['pairings'])}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Your library is empty. Add some ingredients first!")

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
    # Kodun en altına ekle:
st.write("Debug - Current Keys in Database:", list(data.keys()))