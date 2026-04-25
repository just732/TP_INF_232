import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Audit Qualité Hospitalière", layout="wide")

# --- THÈME BLEU NUIT (Correction du paramètre) ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1, h2, h3, p, span, label {
        color: #e0e6ed !important;
    }
    .stButton>button {
        background-color: #2c5282;
        color: white;
        border-radius: 8px;
    }
    /* Style pour les champs de saisie */
    input {
        background-color: #1a202c !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True) # <-- C'était ici l'erreur, c'est corrigé !

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_hopital.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT,
                    raison_visite TEXT, nom_hopital TEXT, temps_urgence INTEGER,
                    qualite_soins TEXT, attitude_personnel TEXT, efficacite_travail TEXT,
                    option_rdv TEXT, date_enregistrement DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION ---
st.sidebar.title("🩺 Navigation")
page = st.sidebar.radio("Aller vers :", ["🏠 Accueil", "📝 Formulaire d'Audit", "📊 Analyse des Données"])

# --- PAGE 1 : ACCUEIL ---
if page == "🏠 Accueil":
    st.title("Audit National pour l'Amélioration des Services Hospitaliers")
    st.info("Système de collecte de données en ligne - Projet INF232")
    
    st.markdown("""
    ### 📌 À propos de cet Audit
    Cette application est un outil d'audit cherchant à **améliorer la qualité des services** dans nos hôpitaux. 
    Elle permet de recueillir des informations sur le parcours des patients et d'analyser l'efficacité du personnel.
    
    **Objectifs de l'étude :**
    - Mesurer le temps d'attente moyen aux urgences.
    - Évaluer le professionnalisme et l'attitude des agents de santé.
    - Sonder l'opinion sur la mise en place d'un système de rendez-vous en ligne.
    
    ---
    **Comment procéder ?**
    1. Utilisez la barre latérale pour accéder au **Formulaire**.
    2. Remplissez honnêtement vos informations.
    3. Consultez les résultats globaux dans l'onglet **Analyse**.
    """)

# --- PAGE 2 : FORMULAIRE D'AUDIT ---
elif page == "📝 Formulaire d'Audit":
    st.header("Saisie des informations de l'audit")
    
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("👤 Identification")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom")
        prenom = c2.text_input("Prénom")
        domicile = c1.text_input("Ville / Quartier")
        metier = c2.text_input("Profession")
        
        st.subheader("🏥 Contexte")
        raison_visite = st.text_area("Raison de la présence à l'hôpital (Symptômes / Maladie)")
        nom_h = st.selectbox("Établissement concerné", ["Hôpital Central", "Clinique Sainte-Marie", "CHU Nord", "Hôpital de District"])
        
        st.subheader("📋 Évaluation")
        col_a, col_b = st.columns(2)
        with col_a:
            t_urgence = st.slider("Temps de réaction aux urgences (min)", 0, 180, 20)
            qualite = st.select_slider("Qualité globale des soins", options=["Médiocre", "Passable", "Satisfaisant", "Excellent"])
        with col_b:
            attitude = st.selectbox("Attitude du personnel", ["Impoli", "Indifférent", "Professionnel", "Chaleureux"])
            travail = st.radio("Efficacité du travail", ["Désorganisée", "Moyenne", "Très organisée"])
            rdv_en_ligne = st.radio("L'option de RDV en ligne est-elle préférable ?", ["Oui", "Non"])

        submitted = st.form_submit_button("Envoyer l'Audit")
        
        if submitted:
            if nom and prenom:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, qualite_soins, attitude_personnel, 
                            efficacite_travail, option_rdv, date_enregistrement) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, domicile, metier, raison_visite, nom_h, t_urgence, 
                          qualite, attitude, travail, rdv_en_ligne, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Données transmises avec succès !")
            else:
                st.warning("⚠️ Veuillez renseigner votre identité.")

# --- PAGE 3 : ANALYSE ---
elif page == "📊 Analyse des Données":
    st.header("Visualisation de l'Audit")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        # Métriques
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Audits", len(df))
        m2.metric("Attente Moyenne", f"{round(df['temps_urgence'].mean(), 1)} min")
        
        # Graphiques
        st.divider()
        g1, g2 = st.columns(2)
        with g1:
            st.subheader("Satisfaction : Attitude")
            fig1 = px.pie(df, names='attitude_personnel', hole=0.3, template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        with g2:
            st.subheader("Attente par Hôpital")
            avg_h = df.groupby('nom_hopital')['temps_urgence'].mean().reset_index()
            fig2 = px.bar(avg_h, x='nom_hopital', y='temps_urgence', template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Base de données brute")
        st.dataframe(df, use_container_width=True)
