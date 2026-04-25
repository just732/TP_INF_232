import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Système Audit", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'audit_publie' not in st.session_state: st.session_state.audit_publie = False
if 'investigateur' not in st.session_state: st.session_state.investigateur = {}

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES NATIONALES ---
data_cameroun = {
    "Centre": ["Hôpital Général", "Hôpital Central", "CHU"],
    "Littoral": ["Hôpital Général Douala", "Laquintinie"],
    "Ouest": ["Hôpital Régional Bafoussam"],
    "Nord": ["Hôpital Régional Garoua"],
    "Est": ["Hôpital Régional Bertoua"]
}

# --- DESIGN ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }
    .info-bubble {
        background: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 20px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }
    .nav-card {
        background-color: rgba(255, 255, 255, 0.15); border: 2px solid white; 
        border-radius: 20px; padding: 20px; text-align: center;
    }
    .stButton>button { background-color: #e1395f !important; color: white !important; border-radius: 50px !important; }
    .white-box { background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_v9.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, email_p TEXT, region TEXT, hopital TEXT, 
                    attente INTEGER, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    
    if st.session_state.audit_publie:
        st.success(f"📍 MISSION ACTIVE : {st.session_state.investigateur['objectif']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-bubble"><h4>Hôpitaux Cameroun</h4><p>Seuls 48% des 172 hôpitaux publics sont performants.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-bubble"><h4>Maternité</h4><p>35.9% des accouchements se font hors hôpital.</p></div>', unsafe_allow_html=True)

    st.markdown("<h3 style='text-align:center;'>MENU</h3>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        if st.button("LANCER L'AUDIT"): changer_page("AuditPatient")
    with n2:
        if st.button("ESPACE ENQUÊTEUR"): changer_page("Admin")
    with n3:
        if st.button("INFOS APP"): changer_page("Infos")

# --- ESPACE ENQUÊTEUR ---
elif st.session_state.page == "Admin":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown("<div class='white-box'>", unsafe_allow_html=True)
    st.subheader("🛠 Paramétrage de la Mission d'Audit")
    
    with st.form("admin_setup"):
        nom_e = st.text_input("Nom de l'enquêteur")
        email_e = st.text_input("Email de réception")
        objectif = st.text_area("OBJECTIF DE L'ENQUÊTE (Ex: Qualité des urgences à Douala)")
        
        if st.form_submit_button("PUBLIER L'AUDIT DANS L'APP"):
            st.session_state.investigateur = {"nom": nom_e, "email": email_e, "objectif": objectif}
            st.session_state.audit_publie = True
            st.success("Formulaire généré et publié !")

    if st.session_state.audit_publie:
        st.divider()
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()
        st.subheader("📊 Résultats collectés")
        st.write(f"Rapports envoyés vers : {st.session_state.investigateur['email']}")
        st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

# --- ESPACE PATIENT ---
elif st.session_state.page == "AuditPatient":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    if not st.session_state.audit_publie:
        st.error("Aucun audit n'est publié. L'enquêteur doit d'abord configurer une mission.")
    else:
        st.markdown(f"<h2>Mission : {st.session_state.investigateur['objectif']}</h2>", unsafe_allow_html=True)
        with st.form("patient_form"):
            nom_p = st.text_input("Nom")
            prenom_p = st.text_input("Prénom")
            reg = st.selectbox("Région", list(data_cameroun.keys()))
            hop = st.selectbox("Hôpital", data_cameroun[reg])
            attente = st.slider("Attente (min)", 0, 300, 30)
            sug = st.text_area("Suggestions")
            if st.form_submit_button("VALIDER"):
                conn = get_connection()
                c = conn.cursor()
                c.execute("INSERT INTO rapports (nom, prenom, region, hopital, attente, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?)",
                          (nom_p, prenom_p, reg, hop, attente, sug, datetime.now()))
                conn.commit()
                conn.close()
                st.success("Données envoyées à l'enquêteur !")

elif st.session_state.page == "Infos":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown("<div class='white-box'><h3>Comment ça marche ?</h3><p>L'enquêteur crée une mission, le patient y répond, et les données sont centralisées.</p></div>", unsafe_allow_html=True)
