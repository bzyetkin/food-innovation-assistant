import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st
import json
import os
import random
import pandas as pd

# -------------------------
# DATA FUNCTIONS
# -------------------------

def load_data():
    if not os.path.exists("data.json"):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

data = load_data()

# -------------------------
# ENGINES (Similarity & Suggestions)
# -------------------------

def find_similar(target, data):
    if target not in data:
        return []
    base = data[target]
    results = []
    for name, info in data.items():
        if name == target: continue
        score = 0
        if info.get("category") == base.get("category"): score += 1
        if info.get("function") == base.get("function"): score += 2
        if info.get("texture") == base.get("texture"): score += 1
        if score >= 2:
            results.append(name)
    return results

def suggest_pairings(ingredient, data):
    if ingredient not in data:
        return []
    flavor = data[ingredient].get("flavor")
    suggestions = []
    for name, info in data.items():
        if name == ingredient: continue
        if info.get("flavor") == flavor:
            suggestions.append(name)
    return random.sample(suggestions, min(len(suggestions), 5))

# -------------------------
# UI STYLE
# -------------------------

st.set_page_config(page_title="R&D Food Lab", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#F5F7F6;}
h1, h2, h3 {color:#1B4332 !important;}
.stButton>button {background:#2D6A4F; color:white; border-radius:8px;}
.stMetric {background: white; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);}
</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🧪 R&D Control Center")

# BULK IMPORT
st.sidebar.subheader("📂 Bulk Import")
file = st.sidebar.file_uploader("Upload dataset (CSV/Excel)", type=["csv", "xlsx"])

if file:
    if st.sidebar.button("Import File"):
        try:
            df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
            for _, row in df.iterrows():
                name = str(row["Name"]).strip().capitalize()
                data[name] = {
                    "pairings": [p.strip().capitalize() for p in str(row["Pairings"]).split(",")],
                    "category": row.get("Category", "Other"),
                    "flavor": row.get("Flavor", "Neutral"),
                    "fat_content": int(row.get("Fat", 0)),
                    "texture": row.get("Texture", "N/A"),
                    "function": row.get("Function", "N/A"),
                    "cost": float(row.get("Cost", 0)), # MALİYET EKLENDİ
                    "allergens": str(row.get("Allergens", "None")).split(",") # ALERJEN EKLENDİ
                }
            save_data(data)
            st.sidebar.success("Dataset Imported!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# ADD INGREDIENT
st.sidebar.subheader("➕ Add Ingredient")
with st.sidebar.form("add"):
    name = st.text_input("Name").strip().capitalize()
    category = st.selectbox("Category", ["Proteins", "Lipids", "Carbs", "Additives", "Dairy", "Spices"])
    flavor = st.selectbox("Flavor", ["Sweet", "Sour", "Neutral", "Bitter", "Umami", "Spicy"])
    fat = st.slider("Fat %", 0, 100, 0)
    cost = st.number_input("Cost (per kg/L)", min_value=0.0, step=0.1)
    texture = st.selectbox("Texture", ["Liquid", "Powder", "Solid", "Creamy", "Gel"])
    function = st.selectbox("Function", ["Base", "Emulsifier", "Thickener", "Sweetener", "Stabilizer"])
    allergens = st.multiselect("Allergens", ["Gluten", "Dairy", "Nuts", "Soy", "Egg", "Fish"])
    pairs = st.text_area("Pairings (comma separated)")
    submit = st.form_submit_button("Add to Lab")

    if submit and name:
        data[name] = {
            "pairings": [p.strip().capitalize() for p in pairs.split(",") if p],
            "category": category, "flavor": flavor, "fat_content": fat,
            "texture": texture, "function": function, "cost": cost, "allergens": allergens
        }
        save_data(data)
        st.sidebar.success(f"{name} added!")
        st.rerun()

# DELETE
st.sidebar.subheader("🗑️ Management")
target = st.sidebar.selectbox("Select to Delete", ["None"] + sorted(list(data.keys())))
if st.sidebar.button("Delete Permanently") and target != "None":
    del data[target]
    save_data(data)
    st.rerun()

# -------------------------
# MAIN PAGE
# -------------------------

st.title("🧪 Food Innovation AI Lab")

# SEARCH SECTION
search = st.text_input("🔍 Search Technical Database (e.g. Lecithin, Butter)")

if search:
    results = [k for k in data if search.lower() in k.lower()]
    if results:
        selected = st.selectbox("Select Ingredient", results)
        item = data[selected]
        
        st.success(f"### TECHNICAL ANALYSIS: {selected}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Fat %", f"{item.get('fat_content', 0)}%")
        c2.metric("Cost/kg", f"${item.get('cost', 0):.2f}")
        c3.metric("Function", item.get("function", "N/A"))
        c4.metric("Category", item.get("category", "N/A"))

        # Alerjen Uyarısı
        if item.get("allergens") and item["allergens"] != ["None"]:
            st.warning(f"⚠️ **Allergens:** {', '.join(item['allergens'])}")

        st.write(f"**Texture Profile:** {item.get('texture')} | **Flavor Profile:** {item.get('flavor')}")

        # Pairings & Similarities
        tab1, tab2, tab3 = st.tabs(["🤝 Pairings", "🧬 Similar Ingredients", "🤖 AI Suggestions"])
        
        with tab1:
            cols = st.columns(4)
            for i, p in enumerate(item.get("pairings", [])):
                cols[i % 4].info(p)
        
        with tab2:
            sim = find_similar(selected, data)
            cols = st.columns(4)
            for i, s in enumerate(sim):
                cols[i % 4].warning(s)
        
        with tab3:
            try:
                ai_pairs = suggest_pairings(selected, data)
                cols = st.columns(4)
                for i, p in enumerate(ai_pairs):
                    cols[i % 4].success(p)
            except: st.write("Add more data for AI suggestions.")

# FORMULATION BUILDER
st.divider()
st.subheader("📝 Formulation Builder & Costing")

if data:
    selected_ingredients = st.multiselect("Select Ingredients for Formula:", sorted(list(data.keys())))
    if selected_ingredients:
        recipe_data = []
        total_cost = 0
        total_fat = 0
        
        for ing in selected_ingredients:
            col_a, col_b = st.columns([3, 1])
            ratio = col_b.number_input(f"% {ing}", 0.0, 100.0, 0.0, key=f"rec_{ing}")
            
            if ratio > 0:
                cost_contrib = (data[ing].get('cost', 0) * (ratio / 100))
                fat_contrib = (data[ing].get('fat_content', 0) * (ratio / 100))
                total_cost += cost_contrib
                total_fat += fat_contrib
                recipe_data.append({"Ingredient": ing, "Ratio %": ratio, "Cost Contrib": cost_contrib})

        st.metric("Total Formulation Cost (per kg/L)", f"${total_cost:.2f}")
        st.metric("Final Product Fat Content", f"%{total_fat:.2f}")

# NETWORK VISUALIZATION
st.divider()
st.subheader("🕸️ Ingredient Network Map")
if st.button("Generate Network Graph"):
    G = nx.Graph()
    for name, info in data.items():
        for p in info.get("pairings", []):
            if p in data:
                G.add_edge(name, p)
    
    if len(G.nodes) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='#B7E4C7', node_size=800, font_size=7, edge_color='#40916C')
        st.pyplot(fig)
    else:
        st.write("Not enough connected data to show network.")

if st.sidebar.checkbox("Show Raw Database"):
    st.json(data)