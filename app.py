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

# --- DESIGN CSS : LES BULLES GÉANTES INTERACTIVES ---
st.markdown("""
    <style>
    /* Image de fond principale (Hôpital Général) */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* FORÇAGE DES BOUTONS EN BULLES GÉANTES AVEC IMAGES */
    div.stButton > button {
        height: 450px !important; /* Taille géante */
        width: 100% !important;
        border-radius: 30px !important;
        border: 4px solid white !important;
        font-size: 35px !important;
        font-weight: bold !important;
        color: white !important;
        text-shadow: 2px 2px 8px black;
        transition: 0.5s !important;
        background-size: cover !important;
        background-position: center !important;
        white-space: pre-wrap !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5) !important;
    }

    /* Bulle WELCOME (Image Pédiatrie) */
    div.nav-welcome > div > div > button {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg') !important;
        background-size: cover !important;
    }

    /* Bulle INQUIRY (Image Maternité) */
    div.nav-inquiry > div > div > button {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg') !important;
        background-size: cover !important;
    }

    /* Bulle INFORMATION (Image Hôpital) */
    div.nav-info > div > div > button {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                    url('https://www.social-sante.gouv.fr/IMG/jpg/pediatrie_hopital.jpg') !important;
        background-size: cover !important;
    }

    /* Effet de flottement interactif */
    div.stButton > button:hover {
        transform: translateY(-20px) scale(1.02) !important;
        border-color: #e1395f !important;
        box-shadow: 0 25px 50px rgba(225, 57, 95, 0.4) !important;
    }

    /* Petit bouton RETOUR rectangulaire */
    .back-box .stButton > button {
        height: 40px !important; width: 120px !important; font-size: 14px !important;
        background: rgba(255,255,255,0.2) !important; border-radius: 5px !important;
        border: 1px solid white !important; margin-bottom: 20px !important;
    }

    .white-box { background: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('patient_plus_vfinal.db', check_same_thread=False)
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
    st.markdown("<h1 style='text-align:center; font-size:80px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:26px;'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>", unsafe_allow_html=True)

    # Statistiques du Cameroun sur l'accueil
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()
    if not df.empty:
        c1, c2 = st.columns(2)
        c1.metric("Audits enregistrés", len(df))
        c2.metric("Attente moyenne", f"{round(df['attente'].mean(),1)} min")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # LES 3 BULLES GÉANTES INTERACTIVES (NAVIGATION)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="nav-welcome">', unsafe_allow_html=True)
        st.button("WELCOME\n\nAccéder à l'Audit", on_click=lambda: changer_page("Audit"))
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="nav-inquiry">', unsafe_allow_html=True)
        st.button("INQUIRY\n\nEspace Enquêteur", on_click=lambda: changer_page("Admin"))
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="nav-info">', unsafe_allow_html=True)
        st.button("INFORMATION\n\nInfos du Projet", on_click=lambda: changer_page("Infos"))
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE 2 : AUDIT ---
elif st.session_state.page == "Audit":
    st.markdown('<div class="back-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='color:white;'>📝 Formulaire d'Audit National</h2>", unsafe_allow_html=True)
    with st.form("audit_form"):
        c1, c2 = st.columns(2)
        nom, prenom, email = c1.text_input("Nom"), c2.text_input("Prénom"), c1.text_input("Email")
        age, reg = c2.number_input("Âge", 0, 110, 25), st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        motif, attente = st.text_area("Motif de consultation (Souffrance)"), st.slider("Attente (min)", 0, 300, 30)
        
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
            st.success("Audit envoyé avec succès.")
            changer_page("Accueil")

# --- PAGE 3 : ADMIN ---
elif st.session_state.page == "Admin":
    st.markdown('<div class="back-box">', unsafe_allow_html=True)
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
    st.markdown('<div class="back-box">', unsafe_allow_html=True)
    st.button("RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div class='white-box'><h3>À propos</h3><p>Patient Plus centralise les données nationales pour la réforme hospitalière.</p></div>", unsafe_allow_html=True)
