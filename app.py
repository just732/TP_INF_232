import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Système d'Audit Hospitalier", layout="wide")

# --- DESIGN PROFESSIONNEL (ÉPURÉ) ---
st.markdown("""
    <style>
    /* Fond dégradé sobre */
    .stApp {
        background: linear-gradient(180deg, #002b5c 0%, #f4f7f9 35%);
        color: #1a1a1a;
    }
    
    /* Bulle d'Objectif Institutionnelle */
    .objective-bubble {
        background-color: white;
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin: 20px 0;
        border-top: 8px solid #002b5c;
        text-align: center;
    }
    .objective-bubble h1 {
        font-size: 48px !important;
        color: #002b5c !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .objective-bubble p {
        font-size: 22px !important;
        color: #34495e;
        max-width: 800px;
        margin: 0 auto;
    }

    /* Cartes de Méthodologie */
    .method-card {
        background-color: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        text-align: center;
        border-bottom: 4px solid #002b5c;
    }
    .method-card h3 { color: #002b5c; font-size: 24px; }

    /* Formulaire Professionnel */
    label { 
        font-size: 16px !important; 
        font-weight: 600 !important; 
        color: #002b5c !important; 
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    /* Bouton de soumission */
    .stButton>button {
        background-color: #002b5c;
        color: white;
        border-radius: 4px;
        padding: 12px 50px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        border: none;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DES DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_hospitalier_final.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT,
                    raison_visite TEXT, nom_hopital TEXT, temps_urgence INTEGER,
                    attitude_globale TEXT, organisation_travail TEXT,
                    eval_infirmieres TEXT, justif_infirmieres TEXT,
                    eval_medecins TEXT, justif_medecins TEXT,
                    rdv_medecin_ligne TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION ADMINISTRATIVE ---
st.sidebar.title("Menu de l'Audit")
page = st.sidebar.radio("Sélectionnez une section :", 
                        ["Présentation de l'Audit", "Collecte des Données", "Rapport d'Analyse"])

# --- PAGE 1 : PRÉSENTATION ---
if page == "Présentation de l'Audit":
    st.markdown("""
        <div class="objective-bubble">
            <h1>Objectif de l'Audit</h1>
            <p>Optimisation de la performance hospitalière par l'analyse quantitative des données patients et l'évaluation de la qualité des soins en milieu médical.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="method-card"><h3>Analyse Statistique</h3><p>Traitement des données de flux et de temps de réponse.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="method-card"><h3>Évaluation RH</h3><p>Audit de la qualité de service par corps de métier.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="method-card"><h3>Digitalisation</h3><p>Étude d\'impact pour les rendez-vous numériques.</p></div>', unsafe_allow_html=True)

# --- PAGE 2 : COLLECTE DES DONNÉES (FORMULAIRE) ---
elif page == "Collecte des Données":
    st.markdown("<h2 style='color:white; text-align:center;'>Questionnaire d'Audit Institutionnel</h2>", unsafe_allow_html=True)
    
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("I. État Civil et Profil")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom de famille")
        prenom = c2.text_input("Prénom")
        dom = c1.text_input("Lieu de résidence")
        job = c2.text_input("Secteur d'activité / Métier")
        raison = st.text_area("Motif médical de la consultation (Symptomatologie)")
        
        st.subheader("II. Évaluation Globale de l'Établissement")
        hopital = st.selectbox("Établissement audité", ["Hôpital Général", "CHU Central", "Hôpital Militaire", "Clinique Conventionnée"])
        t_urgence = st.slider("Délai de prise en charge aux urgences (en minutes)", 0, 240, 30)
        attitude_g = st.selectbox("Évaluation de l'accueil général", ["Insuffisant", "Passable", "Satisfaisant", "Excellent"])
        travail_g = st.radio("Perception de l'organisation interne", ["Désorganisée", "Standard", "Optimisée"])

        st.subheader("III. Audit du Personnel Infirmier")
        e_inf = st.select_slider("Qualité de service (Infirmiers)", options=["Faible", "Moyenne", "Élevée", "Optimale"])
        j_inf = st.text_area("Justification détaillée (Soins infirmiers)")

        st.subheader("IV. Audit du Corps Médical (Médecins)")
        e_med = st.select_slider("Qualité de service (Médecins)", options=["Faible", "Moyenne", "Élevée", "Optimale"])
        j_med = st.text_area("Justification détaillée (Consultation médicale)")

        st.subheader("V. Perspectives de Digitalisation")
        rdv = st.radio("L'implémentation d'un système de rendez-vous en ligne avec un praticien spécifique vous semble-t-elle pertinente ?", 
                      ["Favorable", "Défavorable"])

        if st.form_submit_button("VALIDER ET ENREGISTRER L'AUDIT"):
            if nom and prenom and raison:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, attitude_globale, organisation_travail,
                            eval_infirmieres, justif_infirmieres, eval_medecins, justif_medecins, 
                            rdv_medecin_ligne, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, dom, job, raison, hopital, t_urgence, attitude_g, travail_g,
                          e_inf, j_inf, e_med, j_med, rdv, datetime.now()))
                conn.commit()
                conn.close()
                st.success("Enregistrement confirmé. Les données ont été transmises au serveur d'analyse.")
            else:
                st.error("Erreur : Les champs obligatoires d'identification doivent être complétés.")

# --- PAGE 3 : RAPPORT D'ANALYSE ---
elif page == "Rapport d'Analyse":
    st.markdown("<h2 style='color:white; text-align:center;'>Rapport de Synthèse Statistique</h2>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée disponible pour la génération du rapport.")
    else:
        # Indicateurs de performance
        c1, c2, c3 = st.columns(3)
        c1.metric("Échantillon total", f"{len(df)} audits")
        c2.metric("Moyenne d'attente", f"{round(df['temps_urgence'].mean(), 1)} min")
        taux = (len(df[df['rdv_medecin_ligne'] == "Favorable"]) / len(df)) * 100
        c3.metric("Taux d'adhésion digital", f"{round(taux, 1)}%")

        st.divider()

        # Visualisations
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig1 = px.pie(df, names='attitude_globale', title="Analyse de l'Accueil")
            st.plotly_chart(fig1, use_container_width=True)
        with col_g2:
            fig2 = px.histogram(df, x='nom_hopital', y='temps_urgence', histfunc='avg', title="Performance Temporelle par Site")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Base de Données d'Audit")
        st.dataframe(df, use_container_width=True)
