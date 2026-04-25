import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Portail National d'Audit Hospitalier", layout="wide")

# --- INITIALISATION DES VARIABLES DE NAVIGATION (Session State) ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"
if 'selected_hopital' not in st.session_state:
    st.session_state.selected_hopital = None

# --- DESIGN PROFESSIONNEL ET SOBRE ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #1a1a1a; }
    
    /* En-tête Institutionnel */
    .header-banner {
        background-color: #002b5c;
        padding: 40px;
        color: white;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
    }
    
    /* Cartes Hôpitaux */
    .hospital-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 6px solid #002b5c;
        height: 100%;
    }
    .hospital-card h4 { color: #002b5c; margin-bottom: 10px; }
    .hospital-card p { font-size: 14px; color: #555; height: 60px; }

    /* Zone Objectif */
    .objective-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border-left: 10px solid #002b5c;
        margin: 20px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Style des boutons */
    div.stButton > button {
        background-color: #002b5c;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_hospitalier_v5.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, domicile TEXT, metier TEXT, raison_visite TEXT,
                    nom_hopital TEXT, temps_urgence INTEGER, attitude_globale TEXT,
                    eval_infirmieres TEXT, justif_infirmieres TEXT,
                    eval_medecins TEXT, justif_medecins TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- DONNÉES DES HÔPITAUX ---
hospitals = {
    "Hôpital Général": "Établissement de référence nationale spécialisé dans les soins intensifs et la chirurgie complexe.",
    "CHU Central": "Centre Hospitalier Universitaire axé sur la recherche médicale et la formation des spécialistes.",
    "Clinique de la Paix": "Structure privée conventionnée offrant un service de proximité et des soins personnalisés.",
    "Hôpital de District": "Établissement de santé publique desservant les zones périurbaines pour les soins primaires."
}

# --- NAVIGATION ---
def go_to_form(hopital_name):
    st.session_state.selected_hopital = hopital_name
    st.session_state.page = "Formulaire"

def go_to_home():
    st.session_state.page = "Accueil"
    st.session_state.selected_hopital = None

# --- PAGE 1 : ACCUEIL & PRÉSENTATION ---
if st.session_state.page == "Accueil":
    st.markdown('<div class="header-banner"><h1>SYSTÈME NATIONAL D\'AUDIT HOSPITALIER</h1><p>Ministère de la Santé Publique - Direction de la Qualité</p></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="objective-box">
            <h2 style="color:#002b5c; margin-top:0;">Objectif Institutionnel</h2>
            <p style="font-size:18px;">Cette plateforme centralise les évaluations des usagers afin d'identifier les axes d'amélioration structurels. 
            L'audit permet d'analyser la corrélation entre les ressources humaines et la satisfaction réelle des patients.</p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Sélectionnez l'établissement à auditer")
    cols = st.columns(len(hospitals))
    
    for i, (name, desc) in enumerate(hospitals.items()):
        with cols[i]:
            st.markdown(f'<div class="hospital-card"><h4>{name}</h4><p>{desc}</p></div>', unsafe_allow_html=True)
            if st.button(f"Auditer cet hôpital", key=name):
                go_to_form(name)
    
    st.markdown("---")
    if st.button("Consulter le Rapport d'Analyse Global"):
        st.session_state.page = "Analyse"

# --- PAGE 2 : FORMULAIRE ---
elif st.session_state.page == "Formulaire":
    st.button("⬅ Retour à la liste des hôpitaux", on_click=go_to_home)
    st.header(f"Questionnaire d'Audit : {st.session_state.selected_hopital}")
    
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("I. Informations Démographiques")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom de famille")
        prenom = c2.text_input("Prénom")
        dom = c1.text_input("Ville / Quartier de résidence")
        job = c2.text_input("Profession")
        raison = st.text_area("Motif de consultation (Symptomatologie constatée)")
        
        st.subheader("II. Évaluation des Services et du Personnel")
        t_urgence = st.slider("Délai d'attente aux urgences (min)", 0, 240, 30)
        attitude_g = st.selectbox("Attitude globale du personnel", ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"])

        col_inf, col_med = st.columns(2)
        with col_inf:
            st.markdown("**Personnel Infirmier**")
            e_inf = st.select_slider("Qualité technique et accueil (Infirmiers)", options=["1", "2", "3", "4", "5"], key="inf")
            j_inf = st.text_area("Justification (Audit Infirmiers)")
        with col_med:
            st.markdown("**Corps Médical**")
            e_med = st.select_slider("Expertise et écoute (Médecins)", options=["1", "2", "3", "4", "5"], key="med")
            j_med = st.text_area("Justification (Audit Médecins)")

        st.subheader("III. Digitalisation et Perspectives")
        rdv = st.radio("L'option de rendez-vous en ligne avec un praticien spécifique est-elle souhaitable ?", ["Favorable", "Défavorable"])
        
        st.subheader("IV. Recommandations d'Amélioration")
        suggestions = st.text_area("Selon votre expérience, quelles mesures concrètes préconisez-vous pour améliorer la qualité du service dans cet établissement ?")

        if st.form_submit_button("SOUMETTRE LE RAPPORT D'AUDIT"):
            if nom and prenom and suggestions:
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, domicile, metier, raison_visite, 
                            nom_hopital, temps_urgence, attitude_globale, eval_infirmieres, 
                            justif_infirmieres, eval_medecins, justif_medecins, rdv_ligne, 
                            suggestions, date_soumission) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                         (nom, prenom, dom, job, raison, st.session_state.selected_hopital, 
                          t_urgence, attitude_g, e_inf, j_inf, e_med, j_med, rdv, suggestions, datetime.now()))
                conn.commit()
                conn.close()
                st.success("Données enregistrées. Le rapport a été transmis à la direction centrale.")
                st.info("Redirection vers l'accueil...")
                # Petite pause avant retour accueil
                go_to_home()
            else:
                st.error("Veuillez compléter l'identification et la section Recommandations.")

# --- PAGE 3 : ANALYSE ---
elif st.session_state.page == "Analyse":
    st.button("⬅ Retour à l'accueil", on_click=go_to_home)
    st.title("Tableau de Bord de l'Audit National")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée disponible pour l'analyse.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Volume d'Audits", len(df))
        c2.metric("Attente Moyenne", f"{round(df['temps_urgence'].mean(), 1)} min")
        taux = (len(df[df['rdv_ligne'] == "Favorable"]) / len(df)) * 100
        c3.metric("Adhésion Digitalisation", f"{round(taux, 1)}%")

        st.divider()
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig1 = px.histogram(df, x='nom_hopital', y='temps_urgence', histfunc='avg', title="Performance Temporelle par Établissement")
            st.plotly_chart(fig1, use_container_width=True)
        with col_g2:
            fig2 = px.pie(df, names='attitude_globale', title="Répartition de la Satisfaction Accueil")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Préconisations d'amélioration des usagers")
        st.dataframe(df[['nom_hopital', 'nom', 'suggestions', 'date_soumission']], use_container_width=True)
