import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Hôpital - Collecte & Analyse", layout="wide")

# --- FONCTION BASE DE DONNÉES (ROBUSTESSE) ---
def get_connection():
    # Crée une connexion à SQLite (le fichier sera créé automatiquement)
    return sqlite3.connect('donnees_hopital.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_hopital TEXT,
                    temps_urgence INTEGER,
                    traitement_patients TEXT,
                    attitude_personnel TEXT,
                    efficacite_travail TEXT,
                    option_rdv TEXT,
                    date_enregistrement DATETIME)''')
    conn.commit()
    conn.close()

# Initialisation au démarrage
init_db()

# --- INTERFACE ---
st.title("🏥 Plateforme d'Évaluation des Services Hospitaliers")
st.markdown("---")

# Création des onglets pour séparer la Collecte de l'Analyse (EFFICACITÉ)
tab_collecte, tab_analyse = st.tabs(["📝 Collecte des Données", "📊 Analyse Descriptive"])

# --- ONGLET 1 : COLLECTE DES DONNÉES ---
with tab_collecte:
    st.header("Formulaire de satisfaction patient")
    
    with st.form("form_patient", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nom_h = st.selectbox("Sélectionnez l'Hôpital", ["Hôpital Central", "Clinique Sainte-Marie", "CHU Nord", "Hôpital de District"])
            t_urgence = st.number_input("Temps de réaction aux urgences (en minutes)", min_value=0, max_value=300, value=15)
            traitement = st.select_slider("Comment les patients sont-ils traités ?", 
                                         options=["Très mal", "Moyen", "Bien", "Excellent"])
        
        with col2:
            attitude = st.selectbox("Attitude du personnel", ["Désagréable", "Neutre", "Accueillante", "Très chaleureuse"])
            travail = st.radio("Façon de travailler du personnel", ["Désorganisée", "Passable", "Très organisée"])
            rdv_en_ligne = st.radio("L'option de rendez-vous en ligne est-elle préférable ?", ["Oui", "Non"])

        submitted = st.form_submit_button("Enregistrer les données")
        
        if submitted:
            try:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom_hopital, temps_urgence, traitement_patients, 
                            attitude_personnel, efficacite_travail, option_rdv, date_enregistrement) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                         (nom_h, t_urgence, traitement, attitude, travail, rdv_en_ligne, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Données enregistrées avec succès !")
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement : {e}")

# --- ONGLET 2 : ANALYSE DESCRIPTIVE (CRÉATIVITÉ) ---
with tab_analyse:
    st.header("Analyse Visuelle des Performances")
    
    # Lecture des données
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée à analyser pour le moment. Veuillez remplir le formulaire.")
    else:
        # 1. Indicateurs clés (KPIs)
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total d'avis", len(df))
        kpi2.metric("Temps Urgence Moyen", f"{round(df['temps_urgence'].mean(), 1)} min")
        
        oui_rdv = len(df[df['option_rdv'] == "Oui"])
        percent_rdv = (oui_rdv / len(df)) * 100
        kpi3.metric("Favorable au RDV en ligne", f"{round(percent_rdv, 1)}%")

        st.markdown("---")

        # 2. Graphiques
        g1, g2 = st.columns(2)

        with g1:
            st.subheader("Attitude du personnel")
            fig_pie = px.pie(df, names='attitude_personnel', hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)

        with g2:
            st.subheader("Temps d'urgence par Hôpital")
            fig_bar = px.bar(df.groupby('nom_hopital')['temps_urgence'].mean().reset_index(), 
                             x='nom_hopital', y='temps_urgence', color='nom_hopital')
            st.plotly_chart(fig_bar, use_container_width=True)

        # 3. Tableau de données
        st.subheader("Historique des saisies")
        st.dataframe(df, use_container_width=True)
