import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'investigateur' not in st.session_state: st.session_state.investigateur = None
if 'admin_auth' not in st.session_state: st.session_state.admin_auth = False

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES ---
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

# --- DESIGN PROFESSIONNEL (CSS) ---
st.markdown("""
    <style>
    /* Fond d'écran Hôpital Général */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.85), rgba(0, 43, 92, 0.85)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* Grandes Bulles de Navigation (Boutons stylisés) */
    .stButton > button {
        height: 250px !important;
        width: 100% !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 25px !important;
        font-size: 30px !important;
        font-weight: bold !important;
        transition: 0.4s !important;
    }
    .stButton > button:hover {
        background-color: #e1395f !important;
        border-color: #e1395f !important;
        transform: scale(1.02);
    }

    /* Style spécifique pour le bouton RETOUR (Petit et discret) */
    div[data-testid="stForm"] .stButton > button, 
    .back-btn-container .stButton > button {
        height: 40px !important;
        width: auto !important;
        font-size: 14px !important;
        padding: 0 20px !important;
        border-radius: 5px !important;
        background-color: transparent !important;
    }

    /* Cartes d'info accueil */
    .info-card {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }

    .white-box { background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_v10_final.db', check_same_thread=False)

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
    st.markdown("<h1 style='text-align:center; font-size:60px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:24px; padding: 0 100px;'>Cette application améliore la qualité du traitement dans les services d'urgence du Cameroun.</p>", unsafe_allow_html=True)

    # Dashboard de synthèse sur l'accueil
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Audits Complétés", len(df))
        c2.metric("Attente Moyenne", f"{round(df['attente'].mean(), 1)} min")
        c3.metric("Régions", df['region'].nunique())

    # Bulles d'info
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="info-card"><h4>Surcharge Hospitalière</h4><p>Le Cameroun compte 172 hôpitaux publics. La performance globale est estimée à 48%.</p></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="info-card"><h4>Maternité & Soins</h4><p>35,9% des accouchements se font hors milieu assisté, un défi majeur pour la santé néonatale.</p></div>', unsafe_allow_html=True)

    # GRANDES BULLES DE NAVIGATION (Pas de petits boutons)
    st.markdown("<br><br>", unsafe_allow_html=True)
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        st.button("📝 AUDIT PATIENT", on_click=lambda: changer_page("Audit"))
    with nav2:
        st.button("🔐 ESPACE ADMIN", on_click=lambda: changer_page("Admin"))
    with nav3:
        st.button("ℹ️ INFOS PROJET", on_click=lambda: changer_page("Infos"))

# --- PAGE 2 : AUDIT PATIENT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.header("Formulaire d'Audit National")
    with st.form("audit_form"):
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        email, age = c1.text_input("Email"), c2.number_input("Âge", 0, 110, 25)
        reg = st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        motif = st.text_area("Motif de consultation")
        attente = st.slider("Attente (min)", 0, 300, 30)
        
        ci, cm = st.columns(2)
        e_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
        j_inf = ci.text_area("Justification (Infirmières)")
        e_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
        j_med = cm.text_area("Justification (Médecins)")
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

# --- PAGE 3 : ESPACE ENQUÊTEUR ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👤 Création Compte", "📊 Accès Résultats"])
    
    with tab1:
        st.markdown("<div class='white-box'>", unsafe_allow_html=True)
        with st.form("acc"):
            n_e = st.text_input("Nom Enquêteur")
            e_e = st.text_input("Email Professionnel")
            if st.form_submit_button("VALIDER LE COMPTE"):
                st.session_state.investigateur = n_e
                st.success("Compte Enquêteur activé.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        pwd = st.text_input("Mot de passe de l'audit", type="password")
        col_v1, col_v2 = st.columns([1, 4])
        if col_v1.button("VALIDER"):
            if pwd == "admin123":
                st.session_state.admin_auth = True
                st.success("Accès autorisé.")
            else: st.error("Incorrect")
            
        if st.session_state.admin_auth:
            conn = get_connection()
            df = pd.read_sql_query("SELECT * FROM rapports", conn)
            conn.close()
            st.dataframe(df)
            if st.button("RETOURNER À L'INTERFACE D'AUDIT"):
                st.session_state.admin_auth = False
                changer_page("Audit")

# --- PAGE 4 : INFOS ---
elif st.session_state.page == "Infos":
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    st.button("⬅ Retour", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h3>À propos</h3><p>Patient Plus est une plateforme d'audit citoyen pour la santé nationale au Cameroun.</p></div>", unsafe_allow_html=True)
