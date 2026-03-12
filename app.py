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
# SIMILARITY ENGINE
# -------------------------

def find_similar(target, data):

    if target not in data:
        return []

    base = data[target]
    results = []

    for name, info in data.items():

        if name == target:
            continue

        score = 0

        if info.get("category") == base.get("category"):
            score += 3

        if info.get("function") == base.get("function"):
            score += 3

        if info.get("texture") == base.get("texture"):
            score += 2

        if info.get("flavor") == base.get("flavor"):
            score += 2

        fat_diff = abs(info.get("fat_content",0) - base.get("fat_content",0))

        if fat_diff < 10:
            score += 2
        elif fat_diff < 25:
            score += 1

        if score >= 5:
            results.append((name, score))

    results.sort(key=lambda x: x[1], reverse=True)

    return [r[0] for r in results[:6]]

# -------------------------
# PAIRING ENGINE
# -------------------------

def suggest_pairings(ingredient, data):

    if ingredient not in data:
        return []

    base = data[ingredient]
    suggestions = []

    for name, info in data.items():

        if name == ingredient:
            continue

        score = 0

        if info.get("flavor") == base.get("flavor"):
            score += 3

        if info.get("category") != base.get("category"):
            score += 1

        if ingredient in info.get("pairings", []):
            score += 4

        if score >= 3:
            suggestions.append((name, score))

    suggestions.sort(key=lambda x: x[1], reverse=True)

    return [s[0] for s in suggestions[:6]]

# -------------------------
# UI SETTINGS
# -------------------------

st.set_page_config(page_title="R&D Food Lab", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#F5F7F6;}
h1, h2, h3 {color:#1B4332 !important;}
.stButton>button {background:#2D6A4F; color:white; border-radius:8px;}
.stMetric {background: white; padding: 15px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.title("🧪 R&D Control Center")

# BULK IMPORT
st.sidebar.subheader("📂 Bulk Import")

file = st.sidebar.file_uploader("Upload dataset", type=["csv","xlsx"])

if file:
    if st.sidebar.button("Import File"):

        try:

            df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

            for _,row in df.iterrows():

                name = str(row["Name"]).strip().capitalize()

                data[name] = {

                    "pairings":[p.strip().capitalize() for p in str(row["Pairings"]).split(",")],

                    "category":row.get("Category","Other"),
                    "flavor":row.get("Flavor","Neutral"),
                    "fat_content":int(row.get("Fat",0)),

                    "protein":float(row.get("Protein",0)),
                    "carbs":float(row.get("Carbs",0)),
                    "calories":float(row.get("Calories",0)),

                    "texture":row.get("Texture","N/A"),
                    "function":row.get("Function","N/A"),

                    "cost":float(row.get("Cost",0)),
                    "allergens":str(row.get("Allergens","")).split(",")

                }

            save_data(data)
            st.sidebar.success("Dataset Imported!")
            st.rerun()

        except Exception as e:

            st.sidebar.error(e)

# ADD INGREDIENT

st.sidebar.subheader("➕ Add Ingredient")

with st.sidebar.form("add"):

    name = st.text_input("Name").strip().capitalize()

    category = st.selectbox("Category",["Proteins","Lipids","Carbs","Additives","Dairy","Spices"])

    flavor = st.selectbox("Flavor",["Sweet","Sour","Neutral","Bitter","Umami","Spicy"])

    fat = st.slider("Fat %",0,100,0)

    protein = st.slider("Protein %",0,100,0)

    carbs = st.slider("Carbs %",0,100,0)

    calories = st.number_input("Calories",0)

    cost = st.number_input("Cost",0.0)

    texture = st.selectbox("Texture",["Liquid","Powder","Solid","Creamy","Gel"])

    function = st.selectbox("Function",["Base","Emulsifier","Thickener","Sweetener","Stabilizer"])

    allergens = st.multiselect("Allergens",["Gluten","Dairy","Nuts","Soy","Egg","Fish"])

    pairs = st.text_area("Pairings")

    submit = st.form_submit_button("Add")

    if submit and name:

        data[name]={

        "pairings":[p.strip().capitalize() for p in pairs.split(",") if p],

        "category":category,
        "flavor":flavor,
        "fat_content":fat,
        "protein":protein,
        "carbs":carbs,
        "calories":calories,
        "texture":texture,
        "function":function,
        "cost":cost,
        "allergens":allergens

        }

        save_data(data)

        st.sidebar.success(f"{name} added")

        st.rerun()

# DELETE

st.sidebar.subheader("🗑️ Management")

target = st.sidebar.selectbox("Delete Ingredient",["None"]+sorted(list(data.keys())))

if st.sidebar.button("Delete") and target!="None":

    del data[target]

    save_data(data)

    st.rerun()

# -------------------------
# MAIN PAGE
# -------------------------

st.title("🧪 Food Innovation AI Lab")

# SEARCH

search = st.text_input("🔍 Search Ingredient")

if search:

    results=[

    k for k,v in data.items()

    if search.lower() in k.lower()

    or search.lower() in v.get("category","").lower()

    or search.lower() in v.get("function","").lower()

    or search.lower() in v.get("flavor","").lower()

    ]

    if results:

        selected = st.selectbox("Select Ingredient",results)

        item = data[selected]

        st.success(f"TECHNICAL ANALYSIS : {selected}")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Fat %",item.get("fat_content",0))

        c2.metric("Cost/kg",item.get("cost",0))

        c3.metric("Function",item.get("function"))

        c4.metric("Category",item.get("category"))

        st.write("Texture:",item.get("texture"))

        st.write("Flavor:",item.get("flavor"))

        tab1,tab2,tab3 = st.tabs(["Pairings","Similar","AI Suggestions"])

        with tab1:

            for p in item.get("pairings",[]):

                st.info(p)

        with tab2:

            sim = find_similar(selected,data)

            for s in sim:

                st.warning(s)

        with tab3:

            ai_pairs = suggest_pairings(selected,data)

            for p in ai_pairs:

                st.success(p)

# -------------------------
# FORMULATION BUILDER
# -------------------------

st.divider()

st.subheader("📝 Formulation Builder")

if data:

    selected_ingredients = st.multiselect("Select Ingredients",sorted(list(data.keys())))

    if selected_ingredients:

        total_cost = 0
        total_fat = 0
        total_protein = 0
        total_carbs = 0
        total_calories = 0
        total_ratio = 0

        for ing in selected_ingredients:

            ratio = st.number_input(f"% {ing}",0.0,100.0,0.0,key=ing)

            if ratio>0:

                total_ratio += ratio

                total_cost += data[ing].get("cost",0)*(ratio/100)
                total_fat += data[ing].get("fat_content",0)*(ratio/100)
                total_protein += data[ing].get("protein",0)*(ratio/100)
                total_carbs += data[ing].get("carbs",0)*(ratio/100)
                total_calories += data[ing].get("calories",0)*(ratio/100)

        st.metric("Total Formula %",round(total_ratio,2))

        if total_ratio>100:
            st.error("Formula exceeds 100%")

        elif total_ratio<100:
            st.warning("Formula below 100%")

        else:
            st.success("Formula Balanced")

        st.metric("Cost",round(total_cost,2))
        st.metric("Fat",round(total_fat,2))
        st.metric("Protein",round(total_protein,2))
        st.metric("Carbs",round(total_carbs,2))
        st.metric("Calories",round(total_calories,2))

# -------------------------
# NETWORK GRAPH
# -------------------------

st.divider()

st.subheader("🕸️ Ingredient Network")

if st.button("Generate Network"):

    G = nx.Graph()

    for name,info in data.items():

        for p in info.get("pairings",[]):

            if p in data:

                G.add_edge(name,p)

    if len(G.nodes)>0:

        fig,ax = plt.subplots(figsize=(10,6))

        pos = nx.spring_layout(G)

        node_sizes = [G.degree(n)*300 for n in G.nodes]

        nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="#B7E4C7",
        node_size=node_sizes,
        font_size=8,
        edge_color="#40916C"
        )

        st.pyplot(fig)

    else:

        st.write("Not enough connections")

# RAW DATA

if st.sidebar.checkbox("Show Raw Database"):

    st.json(data)