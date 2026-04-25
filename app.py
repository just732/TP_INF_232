import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'admin_auth' not in st.session_state: st.session_state.admin_auth = False

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU", "Gynéco-Obstétrique"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de Bonassama"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de Kousseri"],
    "Nord": ["Hôpital Régional de Garoua"], "Est": ["Hôpital Régional de Bertoua"],
    "Ouest": ["Hôpital Régional de Bafoussam"], "Sud": ["Hôpital Régional d'Ebolowa"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda"], "Sud-Ouest": ["Hôpital Régional de Buea"]
}

# --- DESIGN CSS (REPRODUCTION EXACTE IMAGE 2) ---
st.markdown("""
    <style>
    /* Fond : Hôpital Général de Yaoundé */
    .stApp {
        background: linear-gradient(rgba(0, 30, 70, 0.8), rgba(0, 30, 70, 0.8)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* LES TROIS BULLES LARGES BLEU MARINE */
    .nav-container .stButton > button {
        height: 200px !important;
        width: 100% !important;
        background-color: #1a3352 !important; /* BLEU MARINE DE L'IMAGE */
        color: white !important;
        border: 2px solid white !important; /* BORDURE BLANCHE FINE */
        border-radius: 15px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        white-space: pre-wrap !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4) !important;
        transition: 0.3s;
    }
    .nav-container .stButton > button:hover {
        background-color: #24446d !important;
        transform: translateY(-5px);
    }

    /* PETIT BOUTON RETOUR RECTANGULAIRE */
    .back-btn .stButton > button {
        height: 35px !important; width: 110px !important; font-size: 13px !important;
        background-color: rgba(255, 255, 255, 0.1) !important; border: 1px solid white !important;
    }

    /* Info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 15px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #e1395f;
    }
    label { color: white !important; font-weight: bold; }
    .white-box { background: white; padding: 30px; border-radius: 15px; color: black; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('patient_plus_final_national.db', check_same_thread=False)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, email TEXT, region TEXT, hopital TEXT, 
                    motif TEXT, attente INTEGER, eval_inf TEXT, eval_med TEXT, 
                    suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()
init_db()

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:65px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px;'>Amélioration du traitement de service dans les services d'urgence et hospitaliers.</p>", unsafe_allow_html=True)

    # Statistiques directes
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits", len(df)), c2.metric("Attente Moy.", f"{round(df['attente'].mean(),1)}m"), c3.metric("Régions", df['region'].nunique())

    col_a, col_b = st.columns(2)
    with col_a: st.markdown('<div class="info-card"><h4>Hôpitaux Publics</h4><p>172 établissements suivis pour optimiser la performance nationale.</p></div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="info-card"><h4>Maternité</h4><p>Analyse des naissances assistées pour renforcer la sécurité sanitaire.</p></div>', unsafe_allow_html=True)

    # --- LES TROIS BULLES LARGES (NAVIGATION) ---
    st.markdown("<br><h3 style='text-align:center;'>NAVIGUER DANS L'APPLICATION</h3>", unsafe_allow_html=True)
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1: st.button("📝 AUDIT\n\nParticiper à l'enquête", on_click=lambda: changer_page("Audit"))
    with n2: st.button("🔐 ADMIN\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
    with n3: st.button("ℹ️ INFOS\n\nÀ propos du projet", on_click=lambda: changer_page("Infos"))
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 : AUDIT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.but
