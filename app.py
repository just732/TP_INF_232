import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Audit Quantitatif Hospitalier", layout="wide")

# --- DESIGN "QUANTITATIVE METHODS" (Bleu & Blanc) ---
st.markdown("""
    <style>
    /* Fond principal gris très clair */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Barre latérale bleu foncé */
    [data-testid="stSidebar"] {
        background-color: #002b5c;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* En-tête bleu comme sur l'image */
    .header-box {
        background-color: #002b5c;
        padding: 40px;
        border-radius: 0px 0px 50px 50px;
        text-align: center;
        margin-bottom: 30px;
    }
    .header-box h1 {
        color: white !important;
        font-family: 'Helvetica', sans-serif;
        font-weight: bold;
    }
    /* Cartes blanches pour le contenu */
    .stat-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 5px solid #0056b3;
    }
    div.stButton > button {
        background-color: #002b5c;
        color: white;
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_v3.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT,
                    raison_visite TEXT, nom_hopital TEXT, temps_urgence INTEGER,
                    qualite_soins TEXT, attitude_personnel TEXT, efficacite_travail TEXT,
                    option_rdv_ligne TEXT, rdv_medecin_specifique TEXT,
                    date_enregistrement DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION ---
page = st.sidebar.radio("Navigation", ["🏠 Accueil & Méthodologie", "📝 Formulaire d'Audit", "📊 Dashboard Analyse"])

# --- PAGE 1 : ACCUEIL ---
if page == "🏠 Accueil & Méthodologie":
    st.markdown('<div class="header-box"><h1>Quantitative Audit Methods</h1><p style="color:white;">Amélioration continue des soins hospitaliers</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="stat-card"><h3>1</h3><p><b>Collecte de Données</b><br>Analyse des temps de réponse et flux de patients.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-card"><h3>2</h3><p><b>Analyse Qualitative</b><br>Évaluation du comportement du personnel médical.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-card"><h3>3</h3><p><b>Digitalisation</b><br>Étude de faisabilité des rendez-vous en ligne.</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <br><br>
    ### 🎯 Objectif de l'Audit
    Ce système utilise des **méthodes quantitatives** pour transformer le ressenti des patients en données exploitables. 
    En participant, vous aidez le ministère de la santé à identifier les goulots d'étranglement dans les hôpitaux sélectionnés.
    """, unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif page == "📝 Formulaire d'Audit":
    st.header("📋 Formulaire d'Audit Patient")
    
    with st.form("main_form"):
        st.subheader("🔹 Identification")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom")
        prenom = c2.text_input("Prénom")
        dom = c1.text_input("Domicile")
        job = c2.text_input("Métier")
        
        st.subheader("🔹 Contexte Médical")
        raison = st.text_area("De quoi souffriez-vous avant votre visite ?")
        hopital = st.selectbox("Hôpital concerné", ["Hôpital Général", "CHU", "Clinique Privée", "Hôpital Militaire"])
        
        st.subheader("🔹 Évaluation du Service")
        t_urgence = st.slider("Temps de réaction urgences (min)", 0, 120, 15)
        attitude = st.select_slider("Attitude du personnel", options=["Impoli", "Neutre", "Accueillant", "Excellent"])
        
        st.subheader("🔹 Digitalisation")
        rdv_ligne = st.radio("L'option générale de RDV en ligne est-elle préférable ?", ["Oui", "Non"])
        
        # NOUVELLE QUESTION DEMANDÉE
        rdv_specifique = st.radio("Vous conviendrait-il de prendre rendez-vous en ligne spécifiquement avec un médecin de cet hôpital ?", ["Oui, ce serait idéal", "Non, je préfère le contact direct"])

        if st.form_submit_button("VALIDER L'AUDIT"):
            if nom and prenom:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, attitude_personnel, option_rdv_ligne, 
                            rdv_medecin_specifique, date_enregistrement) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, dom, job, raison, hopital, t_urgence, attitude, rdv_ligne, rdv_specifique, datetime.now()))
                conn.commit()
                conn.close()
                st.success("✅ Audit enregistré avec succès.")
            else:
                st.error("Veuillez remplir les champs d'identification.")

# --- PAGE 3 : ANALYSE ---
elif page == "📊 Dashboard Analyse":
    st.header("📈 Résultats Quantitatifs")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée à analyser.")
    else:
        # Style des métriques
        m1, m2, m3 = st.columns(3)
        m1.metric("Nombre d'Audits", len(df))
        m2.metric("Moyenne Attente", f"{round(df['temps_urgence'].mean(), 1)} min")
        
        # Calcul préférence RDV médecin
        fav = len(df[df['rdv_medecin_specifique'].str.contains("Oui")])
        m3.metric("Favorable RDV Médecin", f"{round((fav/len(df))*100, 1)}%")

        st.divider()
        
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.pie(df, names='rdv_medecin_specifique', title="Intérêt pour le RDV médecin en ligne", color_discrete_sequence=['#002b5c', '#6699ff'])
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            fig2 = px.bar(df.groupby('nom_hopital')['temps_urgence'].mean().reset_index(), x='nom_hopital', y='temps_urgence', title="Temps moyen par hôpital")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📋 Liste des participants à l'audit")
        st.dataframe(df[['nom', 'prenom', 'metier', 'raison_visite', 'rdv_medecin_specifique']], use_container_width=True)
