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

# --- DONNÉES NATIONALES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie"],
    "Est": ["Hôpital Régional de Bertoua"], "Extrême-Nord": ["Hôpital Régional de Maroua"],
    "Nord": ["Hôpital Régional de Garoua"], "Nord-Ouest": ["Hôpital Régional de Bamenda"],
    "Ouest": ["Hôpital Régional de Bafoussam"], "Sud": ["Hôpital Régional d'Ebolowa"],
    "Sud-Ouest": ["Hôpital Régional de Buea"]
}

# --- DESIGN CSS (REPRODUCTION EXACTE DE VOTRE DERNIÈRE IMAGE) ---
st.markdown("""
    <style>
    /* Fond global : Hôpital Général de Yaoundé */
    .stApp {
        background: linear-gradient(rgba(0, 20, 50, 0.85), rgba(0, 20, 50, 0.85)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* TITRE ET TEXTES D'ACCUEIL */
    .title-main { text-align: center; font-size: 70px; font-weight: 900; margin-bottom: 0px; }
    .subtitle-main { text-align: center; font-size: 20px; margin-bottom: 50px; opacity: 0.9; }
    .nav-header { text-align: center; font-size: 26px; font-weight: bold; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px; }

    /* LES TROIS BULLES (FORMAT RECTANGULAIRE EXACT) */
    div.nav-block .stButton > button {
        height: 280px !important;
        width: 100% !important;
        background-color: rgba(26, 51, 82, 0.6) !important; /* Bleu marine semi-transparent */
        color: white !important;
        border: 2px solid white !important; /* Bordure blanche fine */
        border-radius: 20px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: pre-wrap !important;
        line-height: 1.5 !important;
        transition: 0.3s !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }

    div.nav-block .stButton > button:hover {
        background-color: #1a3352 !important;
        border-color: white !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5) !important;
    }

    /* PETIT BOUTON RETOUR RECTANGULAIRE */
    .back-btn .stButton > button {
        height: 35px !important; width: 100px !important; font-size: 12px !important;
        background-color: rgba(255, 255, 255, 0.1) !important; border-radius: 4px !important;
        border: 1px solid white !important;
    }

    /* Info cards stats */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 15px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #e1395f;
    }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('patient_plus_vfinal.db', check_same_thread=False)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, email TEXT, region TEXT, hopital TEXT, 
                    motif TEXT, attente INTEGER, eval_inf TEXT, eval_med TEXT, 
                    suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()
init_db()

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<div class='title-main'>PATIENT PLUS</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-main'>Amélioration du traitement de service dans les services d'urgence.</div>", unsafe_allow_html=True)

    # Statistiques directes
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits", len(df)), c2.metric("Attente Moy.", f"{round(df['attente'].mean(),1)}m"), c3.metric("Régions", df['region'].nunique())

    col_a, col_b = st.columns(2)
    with col_a: st.markdown('<div class="info-card"><h4>Hôpitaux Publics</h4><p>Analyse des établissements pour optimiser la performance nationale.</p></div>', unsafe_allow_html=True)
    with col_b: st.markdown('<div class="info-card"><h4>Maternité</h4><p>Analyse des naissances assistées pour renforcer la sécurité.</p></div>', unsafe_allow_html=True)

    st.markdown("<div class='nav-header'>NAVIGUER DANS L'APPLICATION</div>", unsafe_allow_html=True)

    # --- LES TROIS BULLES EXACTES (NAVIGATION) ---
    st.markdown('<div class="nav-block">', unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.button("📝\n\nAUDIT\n\nParticiper à l'enquête", on_click=lambda: changer_page("Audit"))
    with n2:
        st.button("🔐\n\nADMIN\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
    with n3:
        st.button("ℹ️\n\nINFOS\n\nÀ propos du projet", on_click=lambda: changer_page("Infos"))
    st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 : AUDIT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    with st.form("audit_f"):
        st.subheader("Identification")
        nom, prenom, email = st.text_input("Nom"), st.text_input("Prénom"), st.text_input("Email")
        reg = st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        attente = st.slider("Attente (min)", 0, 300, 30)
        e_inf = st.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        e_med = st.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        sug = st.text_area("Suggestions")
        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection(); c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, email, region, hopital, attente, eval_inf, eval_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
                     (nom, prenom, email, reg, hop, attente, e_inf, e_med, sug, datetime.now()))
            conn.commit(); conn.close()
            st.success("Données transmises."); changer_page("Accueil")

# --- PAGE 3 : ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    pwd = st.text_input("Code Enquêteur", type="password")
    if st.button("DÉVERROUILLER"):
        if pwd == "admin123":
            conn = get_connection(); df = pd.read_sql_query("SELECT * FROM rapports", conn); conn.close()
            st.dataframe(df)

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='background:white; padding:30px; border-radius:15px; color:black;'>Patient Plus est une plateforme d'audit national au Cameroun.</div>", unsafe_allow_html=True)
