import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Portail National de Santé", layout="wide")

# --- NAVIGATION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"
if 'selected_hopital' not in st.session_state:
    st.session_state.selected_hopital = None

# --- DESIGN PERSONNALISÉ (Style Image de Référence) ---
st.markdown("""
    <style>
    /* Global */
    .stApp { background-color: #ffffff; }
    
    /* Hero Banner - Image d'Hôpital de Référence */
    .hero-section {
        background: linear-gradient(rgba(0, 43, 92, 0.7), rgba(0, 43, 92, 0.7)), 
                    url('https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?auto=format&fit=crop&q=80&w=2000');
        background-size: cover;
        background-position: center;
        padding: 100px 50px;
        color: white;
        text-align: center;
        border-radius: 0 0 50px 50px;
    }
    .hero-section h1 { font-size: 60px !important; font-weight: 800; margin-bottom: 20px; }
    .hero-section p { font-size: 24px !important; max-width: 900px; margin: 0 auto; opacity: 0.9; }

    /* Section Blanche - Informations Sanitaires */
    .info-section {
        padding: 50px;
        background-color: white;
        text-align: center;
    }
    .info-card {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        height: 100%;
        border-top: 5px solid #0056b3;
    }

    /* Section Bas - Réformes & Audit (Dégradé) */
    .bottom-section {
        background: linear-gradient(135deg, #002b5c 0%, #0056b3 100%);
        padding: 60px 50px;
        color: white;
        border-radius: 50px 50px 0 0;
        margin-top: 50px;
    }
    
    /* Boutons et Inputs */
    div.stButton > button {
        background-color: #002b5c;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
    }
    .stTextInput>div>div>input { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_institutionnel.db', check_same_thread=False)

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

# --- LOGIQUE NAVIGATION ---
def go_to_form(hopital_name):
    st.session_state.selected_hopital = hopital_name
    st.session_state.page = "Formulaire"

def go_to_home():
    st.session_state.page = "Accueil"
    st.session_state.selected_hopital = None

# --- PAGE 1 : ACCUEIL STYLE LANDING PAGE ---
if st.session_state.page == "Accueil":
    
    # 1. HERO SECTION (Objectif + Image Hôpital)
    st.markdown("""
        <div class="hero-section">
            <h1>PORTAIL NATIONAL DE LA QUALITÉ HOSPITALIÈRE</h1>
            <p>Cet audit institutionnel permet de transformer les données de terrain en décisions stratégiques 
            pour garantir des soins d'excellence à chaque citoyen.</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. SECTION INFORMATIONS OMS & SANTÉ (Zone Blanche)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="info-card">
                <h4>Directives de l'OMS</h4>
                <p style='font-size:14px; color:black;'>La santé pour tous nécessite des systèmes résilients basés sur des soins primaires de qualité et un financement public durable.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-card">
                <h4>Règles Essentielles</h4>
                <p style='font-size:14px; color:black;'>Hygiène des mains systématique, nutrition équilibrée, vaccination à jour et activité physique régulière.</p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="info-card">
                <h4>Réformes Nationales</h4>
                <p style='font-size:14px; color:black;'>Digitalisation du parcours patient, couverture santé universelle et modernisation des plateaux techniques.</p>
            </div>
        """, unsafe_allow_html=True)

    # 3. SECTION AUDIT (Zone Dégradée)
    st.markdown("<div class='bottom-section'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:white;'>Sélection de l'Établissement pour Audit</h2>", unsafe_allow_html=True)
    
    hospitals = ["Hôpital Général", "CHU Central", "Clinique de la Paix", "Hôpital de District"]
    cols_h = st.columns(len(hospitals))
    
    for i, name in enumerate(hospitals):
        with cols_h[i]:
            st.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.1); padding:20px; border-radius:15px;'><b>{name}</b></div>", unsafe_allow_html=True)
            if st.button(f"Lancer l'Audit", key=name):
                go_to_form(name)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Accéder au Rapport d'Analyse Global"):
        st.session_state.page = "Analyse"
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif st.session_state.page == "Formulaire":
    st.button("⬅ Retour à l'accueil", on_click=go_to_home)
    st.header(f"Questionnaire d'Audit : {st.session_state.selected_hopital}")
    
    with st.form("audit_form"):
        st.subheader("I. Identification & Motif")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        dom, job = c1.text_input("Domicile"), c2.text_input("Métier")
        raison = st.text_area("Raison de la consultation (Symptômes)")
        
        st.subheader("II. Évaluation Quantitative")
        t_urgence = st.slider("Attente aux urgences (min)", 0, 240, 30)
        attitude_g = st.selectbox("Attitude globale", ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"])

        st.markdown("**III. Audit Spécifique**")
        col_inf, col_med = st.columns(2)
        with col_inf:
            e_inf = st.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
            j_inf = st.text_area("Justification Infirmières")
        with col_med:
            e_med = st.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
            j_med = st.text_area("Justification Médecins")

        st.subheader("IV. Amélioration du Service")
        rdv = st.radio("Favorable au RDV en ligne avec un médecin spécifique ?", ["Favorable", "Défavorable"])
        suggestions = st.text_area("Quelles mesures concrètes préconisez-vous pour améliorer cet établissement ?")

        if st.form_submit_button("VALIDER LE RAPPORT"):
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
                st.success("Données enregistrées avec succès.")
                go_to_home()

# --- PAGE 3 : ANALYSE ---
elif st.session_state.page == "Analyse":
    st.button("⬅ Retour à l'accueil", on_click=go_to_home)
    st.title("Tableau de Bord National")
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée disponible.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Audits", len(df))
        c2.metric("Attente Moy.", f"{round(df['temps_urgence'].mean(), 1)} min")
        taux = (len(df[df['rdv_ligne'] == "Favorable"]) / len(df)) * 100
        c3.metric("Adhésion Digital", f"{round(taux, 1)}%")

        st.plotly_chart(px.bar(df, x='nom_hopital', y='temps_urgence', color='attitude_globale', barmode='group'), use_container_width=True)
        st.subheader("Recommandations d'Amélioration")
        st.dataframe(df[['nom_hopital', 'suggestions', 'date_soumission']], use_container_width=True)
