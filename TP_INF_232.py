import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="MedAudit - Analyse Hospitalière", layout="wide")

# --- GESTION DE LA BASE DE DONNÉES (Robustesse) ---
def init_db():
    conn = sqlite3.connect('hopital_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS collectes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hopital TEXT,
                    temps_urgence INTEGER,
                    qualite_soins TEXT,
                    attitude_personnel TEXT,
                    efficacite_travail TEXT,
                    option_rdv TEXT,
                    date_soumission TEXT)''')
    conn.commit()
    conn.close()

def save_data(hopital, temps_urgence, qualite_soins, attitude_personnel, efficacite_travail, option_rdv):
    conn = sqlite3.connect('hopital_data.db')
    c = conn.cursor()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''INSERT INTO collectes (hopital, temps_urgence, qualite_soins, attitude_personnel, efficacite_travail, option_rdv, date_soumission) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)''', 
              (hopital, temps_urgence, qualite_soins, attitude_personnel, efficacite_travail, option_rdv, date_now))
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect('hopital_data.db')
    df = pd.read_sql_query("SELECT * FROM collectes", conn)
    conn.close()
    return df

# Initialisation
init_db()

# --- INTERFACE UTILISATEUR (Créativité) ---
st.title("🏥 MedAudit : Système de Collecte & d'Analyse Hospitalière")
st.markdown("""
*Cette application permet d'évaluer la qualité des services hospitaliers et d'analyser le ressenti des patients pour améliorer le système de santé.*
""")

# Création de deux onglets : Formulaire et Analyse
tab1, tab2 = st.tabs(["📝 Formulaire de Collecte", "📊 Analyse Descriptive"])

# --- ONGLET 1 : COLLECTE ---
with tab1:
    st.header("Évaluation de votre expérience")
    with st.form("survey_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            hopital = st.selectbox("Nom de l'hôpital", ["Hôpital Général", "Clinique de l'Espoir", "CHU Central", "Hôpital Militaire"])
            temps_urgence = st.slider("Temps de réaction aux urgences (en minutes)", 0, 120, 15)
            qualite_soins = st.select_slider("Qualité globale des soins", options=["Médiocre", "Passable", "Satisfaisant", "Excellent"])

        with col2:
            attitude = st.selectbox("Attitude du personnel", ["Très impoli", "Peu accueillant", "Professionnel", "Très chaleureux"])
            efficacite = st.radio("Efficacité du travail (rapidité administrative)", ["Lent", "Moyen", "Rapide"])
            option_rdv = st.radio("Souhaitez-vous une option de prise de rendez-vous en ligne pour cet hôpital ?", ["Oui, absolument", "Non, pas nécessaire"])

        submit = st.form_submit_button("Soumettre l'évaluation")

        if submit:
            save_data(hopital, temps_urgence, qualite_soins, attitude, efficacite, option_rdv)
            st.success(f"Merci ! Votre évaluation pour {hopital} a été enregistrée avec succès.")
            st.balloons()

# --- ONGLET 2 : ANALYSE DESCRIPTIVE (Efficacité) ---
with tab2:
    st.header("Analyse en temps réel des données")
    df = load_data()

    if df.empty:
        st.warning("Aucune donnée disponible pour le moment. Veuillez remplir le formulaire.")
    else:
        # Métriques clés
        m1, m2, m3 = st.columns(3)
        m1.metric("Total des évaluations", len(df))
        m2.metric("Temps moyen d'urgence (min)", round(df['temps_urgence'].mean(), 1))
        
        rdv_pref = (df['option_rdv'] == "Oui, absolument").sum() / len(df) * 100
        m3.metric("% Favorable RDV en ligne", f"{round(rdv_pref, 1)}%")

        st.divider()

        # Graphiques
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Attitude du Personnel")
            fig1 = px.pie(df, names='attitude_personnel', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig1, use_container_width=True)

        with c2:
            st.subheader("Temps d'attente moyen par Hôpital")
            avg_time = df.groupby('hopital')['temps_urgence'].mean().reset_index()
            fig2 = px.bar(avg_time, x='hopital', y='temps_urgence', color='hopital', text_auto=True)
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Vue d'ensemble des données collectées")
        st.dataframe(df.sort_values(by="date_soumission", ascending=False), use_container_width=True)