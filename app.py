import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Santé Cameroun", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DU STATE ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"
if 'est_connecte' not in st.session_state:
    st.session_state.est_connecte = False

def changer_page(nom_page):
    st.session_state.page = nom_page

# --- SÉCURITÉ ---
def hasher_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('patient_plus_final.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Table Satisfaction (Audit Patient)
    c.execute('''CREATE TABLE IF NOT EXISTS satisfaction (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, region TEXT, hopital TEXT, attente INTEGER, 
                    note_accueil TEXT, note_soins TEXT, suggestions TEXT, date TEXT)''')
    # Table Clinique (Collecte Urgences)
    c.execute('''CREATE TABLE IF NOT EXISTS clinique (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT, motif TEXT, gravite TEXT, lit TEXT, date TEXT)''')
    # Table Enquêteurs
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- DESIGN CSS (THÈME V1 : FOND IMAGE + BULLES) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }
    .info-bubble {
        background-size: cover; padding: 25px; border-radius: 25px; color: #1a1a1a; 
        margin-bottom: 20px; border-left: 10px solid #e1395f; min-height: 250px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .img-patient { background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url('https://www.social-sante.gouv.fr/IMG/jpg/pediatrie_hopital.jpg'); }
    .img-medecin { background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url('https://www.unicef.org/cameroon/sites/unicef.org.cameroon/files/styles/hero_desktop/public/UNI354546.jpg'); }
    
    .nav-card {
        background-color: rgba(255, 255, 255, 0.15);
        border: 2px solid white; border-radius: 20px; padding: 20px; text-align: center;
        transition: 0.3s; height: 100%;
    }
    .stButton>button {
        background-color: #e1395f !important; color: white !important;
        border-radius: 50px !important; width: 100%; font-weight: bold !important;
    }
    /* Style pour les champs de saisie pour qu'ils soient lisibles sur le fond sombre */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: white !important; color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DONNÉES RÉGIONALES ---
regions_cam = {
    "Adamaoua": ["HR Ngaoundéré"], "Centre": ["Hôpital Général", "Hôpital Central", "CHU"],
    "Est": ["HR Bertoua"], "Extrême-Nord": ["HR Maroua"], "Littoral": ["Hôpital Laquintinie", "HG Douala"],
    "Nord": ["HR Garoua"], "Nord-Ouest": ["HR Bamenda"], "Ouest": ["HR Bafoussam"],
    "Sud": ["HR Ebolowa"], "Sud-Ouest": ["HR Buea", "HR Limbe"]
}

# --- LOGIQUE DE NAVIGATION ---

# 1. ACCUEIL
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:60px;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:20px;'>Plateforme nationale d'amélioration des soins hospitaliers au Cameroun.</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="info-bubble img-patient"><h3>⭐ Espace Citoyen</h3><p>Donnez votre avis sur votre séjour à l\'hôpital pour nous aider à améliorer l\'accueil et les soins.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-bubble img-medecin"><h3>🩺 Espace Médical</h3><p>Outils de collecte de données cliniques et tri des urgences en temps réel.</p></div>', unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;'>SERVICES DISPONIBLES</h2>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown('<div class="nav-card"><h3>📝 AUDIT</h3><p>Formulaire de satisfaction patient</p></div>', unsafe_allow_html=True)
        st.button("DONNER MON AVIS", on_click=lambda: changer_page("Audit"))
    with n2:
        st.markdown('<div class="nav-card"><h3>🏥 COLLECTE</h3><p>Tri et Admission Urgences</p></div>', unsafe_allow_html=True)
        st.button("SAISIE CLINIQUE", on_click=lambda: changer_page("Clinique"))
    with n3:
        st.markdown('<div class="nav-card"><h3>📊 ADMIN</h3><p>Analyse des données nationales</p></div>', unsafe_allow_html=True)
        st.button("ACCÈS ENQUÊTEUR", on_click=lambda: changer_page("Admin"))

# 2. FORMULAIRE SATISFACTION (AUDIT)
elif st.session_state.page == "Audit":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown("<h2>⭐ Audit de Satisfaction Patient</h2>", unsafe_allow_html=True)
    with st.form("form_audit"):
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom complet (Optionnel)")
        reg = c2.selectbox("Région de l'Hôpital", list(regions_cam.keys()))
        hop = st.selectbox("Hôpital visité", regions_cam[reg])
        attente = st.slider("Temps d'attente (minutes)", 0, 300, 30)
        
        st.write("---")
        n_acc = st.select_slider("Qualité de l'accueil", options=["Médiocre", "Passable", "Bien", "Excellent"])
        n_soin = st.select_slider("Qualité des soins reçus", options=["Médiocre", "Passable", "Bien", "Excellent"])
        sug = st.text_area("Vos suggestions d'amélioration")
        
        if st.form_submit_button("ENVOYER MON AVIS"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO satisfaction (nom, region, hopital, attente, note_accueil, note_soins, suggestions, date) VALUES (?,?,?,?,?,?,?,?)",
                     (nom, reg, hop, attente, n_acc, n_soin, sug, str(datetime.now())))
            conn.commit()
            st.success("Merci ! Votre avis a été enregistré.")
            st.balloons()

# 3. FORMULAIRE CLINIQUE (URGENCES)
elif st.session_state.page == "Clinique":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown("<h2>🩺 Collecte de Données Cliniques</h2>", unsafe_allow_html=True)
    with st.form("form_clinique"):
        st.subheader("Admission & Tri")
        p_id = st.text_input("ID Patient (ex: CMR-102)")
        motif = st.text_area("Motif de consultation")
        grav = st.radio("Niveau de gravité", ["Faible", "Moyen", "Urgent", "Critique"])
        lit = st.toggle("Lit d'urgence disponible")
        
        if st.form_submit_button("ENREGISTRER L'ADMISSION"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO clinique (patient_id, motif, gravite, lit, date) VALUES (?,?,?,?,?)",
                     (p_id, motif, grav, "Oui" if lit else "Non", str(datetime.now())))
            conn.commit()
            st.success("Données cliniques synchronisées avec le Ministère.")

# 4. ESPACE ADMIN (ANALYSE)
elif st.session_state.page == "Admin":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    
    if not st.session_state.est_connecte:
        st.subheader("🔐 Connexion Enquêteur")
        user = st.text_input("Identifiant")
        pw = st.text_input("Mot de passe", type="password")
        if st.button("SE CONNECTER"):
            # Simplifié pour le test : id: admin, mdp: admin
            if user == "admin" and pw == "admin":
                st.session_state.est_connecte = True
                st.rerun()
            else:
                st.error("Identifiants incorrects")
    else:
        st.sidebar.button("Déconnexion", on_click=lambda: st.session_state.update({"est_connecte": False}))
        st.title("📊 Tableau de Bord National")
        
        conn = get_connection()
        df_sat = pd.read_sql_query("SELECT * FROM satisfaction", conn)
        df_cli = pd.read_sql_query("SELECT * FROM clinique", conn)
        
        tab1, tab2 = st.tabs(["Satisfaction Patients", "Données Cliniques"])
        
        with tab1:
            if not df_sat.empty:
                st.plotly_chart(px.histogram(df_sat, x="region", title="Nombre d'audits par région"))
                st.plotly_chart(px.box(df_sat, x="hopital", y="attente", title="Temps d'attente par hôpital"))
                st.dataframe(df_sat)
            else: st.info("Aucun audit disponible.")
            
        with tab2:
            if not df_cli.empty:
                st.plotly_chart(px.pie(df_cli, names="gravite", title="Répartition de la gravité des cas"))
                st.dataframe(df_cli)
            else: st.info("Aucune donnée clinique enregistrée.")
