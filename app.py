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
if 'investigateur' not in st.session_state: st.session_state.investigateur = None

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES NATIONALES ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé", "Hôpital Gynéco-Obstétrique"],
    "Est": ["Hôpital Régional de Bertoua", "Hôpital de District de Batouri"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de District de Mokolo"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital de District de Bonassama"],
    "Nord": ["Hôpital Régional de Garoua", "Hôpital de District de Guider"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda", "Hôpital de District de Wum"],
    "Ouest": ["Hôpital Régional de Bafoussam", "Hôpital de District de Dschang"],
    "Sud": ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi"],
    "Sud-Ouest": ["Hôpital Régional de Buea", "Hôpital Régional de Limbe"]
}

# --- DESIGN CSS (REPRODUCTION EXACTE) ---
st.markdown("""
    <style>
    /* Image de fond Hôpital Général */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.85), rgba(0, 43, 92, 0.85)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* LES TROIS GRANDES BULLES (Sans boutons rouges) */
    .nav-container .stButton > button {
        height: 350px !important;
        width: 100% !important;
        background-color: #1a3352 !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 25px !important;
        font-size: 35px !important;
        font-weight: bold !important;
        white-space: pre-wrap !important;
        transition: 0.4s !important;
        box-shadow: 0 15px 30px rgba(0,0,0,0.4) !important;
    }
    .nav-container .stButton > button:hover {
        background-color: #e1395f !important;
        border-color: #e1395f !important;
        transform: translateY(-15px) !important;
    }

    /* PETIT BOUTON RETOUR RECTANGULAIRE */
    .back-btn-box .stButton > button {
        height: 35px !important;
        width: 120px !important;
        font-size: 13px !important;
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid white !important;
        border-radius: 5px !important;
    }

    /* Info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }
    .white-box { background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_v15_final.db', check_same_thread=False)
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, email TEXT, region TEXT, hopital TEXT, 
                    motif TEXT, attente INTEGER, eval_inf TEXT, justif_inf TEXT, 
                    eval_med TEXT, justif_med TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()
init_db()

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:75px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:24px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # Calculs automatiques
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits", len(df)), c2.metric("Attente Moy.", f"{round(df['attente'].mean(),1)}m"), c3.metric("Régions", df['region'].nunique())

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="info-card"><h4>Hôpitaux Publics</h4><p>172 établissements audités pour une performance nationale accrue.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><h4>Maternité</h4><p>Analyse des 35,9% de naissances hors milieu assisté.</p></div>', unsafe_allow_html=True)

    # LES TROIS BULLES GÉANTES (REPRODUCTION EXACTE)
    st.markdown("<br><br><div class='nav-container'>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.button("WELCOME\n\nAccéder à l'Audit", on_click=lambda: changer_page("Audit"))
    with n2:
        st.button("INQUIRY\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
    with n3:
        st.button("INFORMATION\n\nInfos du Projet", on_click=lambda: changer_page("Infos"))
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 : AUDIT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("Formulaire d'Audit National")
    with st.form("audit_form"):
        c1, c2 = st.columns(2)
        nom, prenom, email = c1.text_input("Nom"), c2.text_input("Prénom"), c1.text_input("Email")
        age, reg = c2.number_input("Âge", 0, 110, 25), st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        motif, attente = st.text_area("Motif de consultation"), st.slider("Attente (min)", 0, 300, 30)
        
        ci, cm = st.columns(2)
        e_inf, j_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"]), ci.text_area("Justification (Infirmières)")
        e_med, j_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"]), cm.text_area("Justification (Médecins)")
        sug = st.text_area("Suggestions d'amélioration")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, age, email, region, hopital, motif, attente, eval_inf, justif_inf, eval_med, justif_med, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                     (nom, prenom, age, email, reg, hop, motif, attente, e_inf, j_inf, e_med, j_med, sug, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Données envoyées.")
            changer_page("Accueil")

# --- PAGE 3 : ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)

    pwd = st.text_input("Code Enquêteur", type="password")
    if st.button("DÉVERROUILLER"):
        if pwd == "admin123": st.session_state.admin_auth = True
        else: st.error("Code incorrect.")
            
    if st.session_state.admin_auth:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()
        st.write(df)

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-btn-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h3>À propos</h3><p>Patient Plus centralise les données pour la réforme hospitalière camerounaise.</p></div>", unsafe_allow_html=True)
