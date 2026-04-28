import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DE LA NAVIGATION ET AUTHENTIFICATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"
if 'est_connecte' not in st.session_state:
    st.session_state.est_connecte = False
if 'user_nom' not in st.session_state:
    st.session_state.user_nom = None

def changer_page(nom_page):
    st.session_state.page = nom_page

# --- FONCTION DE HASHAGE (Pour la sécurité des mots de passe) ---
def hasher_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_national_v7.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Table des rapports d'audit
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, dob TEXT, 
                    region TEXT, domicile TEXT, email TEXT,
                    maladie TEXT, service TEXT, hopital TEXT, attente INTEGER, 
                    eval_inf TEXT, justif_inf TEXT, eval_med TEXT, justif_med TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    # Table des enquêteurs (utilisateurs)
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- FONCTIONS UTILISATEURS ---
def creer_compte(username, password):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hasher_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verifier_connexion(username, password):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hasher_password(password)))
    resultat = c.fetchone()
    conn.close()
    return resultat

# --- DESIGN CSS (Inchangé) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }
    .info-bubble {
        background-size: cover; padding: 25px; border-radius: 25px; color: #1a1a1a; 
        margin-bottom: 20px; border-left: 10px solid #e1395f; min-height: 280px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    .img-pediatrie { background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url('https://www.social-sante.gouv.fr/IMG/jpg/pediatrie_hopital.jpg'); }
    .img-maternite { background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url('https://www.unicef.org/cameroon/sites/unicef.org.cameroon/files/styles/hero_desktop/public/UNI354546.jpg'); }
    .nav-card {
        background-color: rgba(255, 255, 255, 0.15);
        border: 2px solid white; border-radius: 20px; padding: 30px; text-align: center;
        transition: 0.3s; cursor: pointer; height: 100%;
    }
    .stButton>button {
        background-color: #e1395f !important; color: white !important;
        border-radius: 50px !important; width: 100%; font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DONNÉES CAMEROUN ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé"],
    "Est": ["Hôpital Régional de Bertoua", "Hôpital de District de Batouri"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de District de Kousseri"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie"],
    "Nord": ["Hôpital Régional de Garoua", "Hôpital de District de Guider"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda"],
    "Ouest": ["Hôpital Régional de Bafoussam"],
    "Sud": ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi"],
    "Sud-Ouest": ["Hôpital Régional de Buea", "Hôpital Régional de Limbe"]
}

# --- LOGIQUE DES PAGES ---

# 1. ACCUEIL
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown('<div class="info-bubble img-pediatrie"><h4>📊 Performance</h4><p>Audit national pour la qualité des soins.</p></div>', unsafe_allow_html=True)
    with col_info2:
        st.markdown('<div class="info-bubble img-maternite"><h4>👶 Maternité</h4><p>Améliorer la prise en charge des mères.</p></div>', unsafe_allow_html=True)

    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        st.markdown('<div class="nav-card"><h3>📝 AUDIT</h3></div>', unsafe_allow_html=True)
        st.button("OUVRIR LE FORMULAIRE", on_click=lambda: changer_page("Formulaire"))
    with nav2:
        st.markdown('<div class="nav-card"><h3>📊 ANALYSE</h3></div>', unsafe_allow_html=True)
        st.button("ESPACE ENQUÊTEUR", on_click=lambda: changer_page("Admin"))
    with nav3:
        st.markdown('<div class="nav-card"><h3>ℹ️ INFOS</h3></div>', unsafe_allow_html=True)
        st.button("À PROPOS", on_click=lambda: changer_page("Infos"))

# 2. FORMULAIRE (Code existant simplifié pour la démo)
elif st.session_state.page == "Formulaire":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.title("📝 Formulaire Patient")
    with st.form("audit_form"):
        nom = st.text_input("Nom")
        reg = st.selectbox("Région", list(data_cameroun.keys()))
        hop = st.selectbox("Hôpital", data_cameroun[reg])
        attente = st.slider("Attente (min)", 0, 300, 30)
        if st.form_submit_button("VALIDER"):
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, region, hopital, attente, date_soumission) VALUES (?,?,?,?,?)", 
                     (nom, reg, hop, attente, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Merci !")

# 3. PAGE ADMIN / CONNEXION
elif st.session_state.page == "Admin":
    st.button("⬅ RETOUR À L'ACCUEIL", on_click=lambda: changer_page("Accueil"))
    
    if not st.session_state.est_connecte:
        st.subheader("🔐 Accès Enquêteur")
        tab_login, tab_signup = st.tabs(["Connexion", "Créer un compte"])
        
        with tab_login:
            user_in = st.text_input("Nom d'utilisateur")
            pass_in = st.text_input("Mot de passe", type="password")
            if st.button("Se connecter"):
                user = verifier_connexion(user_in, pass_in)
                if user:
                    st.session_state.est_connecte = True
                    st.session_state.user_nom = user_in
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")
        
        with tab_signup:
            new_user = st.text_input("Choisir un nom d'utilisateur")
            new_pass = st.text_input("Choisir un mot de passe", type="password")
            conf_pass = st.text_input("Confirmer le mot de passe", type="password")
            if st.button("S'inscrire"):
                if new_pass == conf_pass and new_user:
                    if creer_compte(new_user, new_pass):
                        st.success("Compte créé ! Connectez-vous.")
                    else:
                        st.error("Ce nom d'utilisateur existe déjà.")
                else:
                    st.error("Les mots de passe ne correspondent pas.")

    else:
        # --- DASHBOARD ADMIN SI CONNECTÉ ---
        st.sidebar.write(f"👤 Connecté : {st.session_state.user_nom}")
        if st.sidebar.button("Se déconnecter"):
            st.session_state.est_connecte = False
            st.rerun()

        st.title("📊 Analyse des Audits Nationaux")
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()
        
        if df.empty:
            st.info("Aucune donnée disponible pour le moment.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(px.pie(df, names='region', title="Répartition par Région", hole=0.4))
            with col2:
                st.plotly_chart(px.histogram(df, x='attente', title="Distribution du temps d'attente (min)"))
            
            st.subheader("Détails des rapports")
            st.dataframe(df)

# 4. INFOS
elif st.session_state.page == "Infos":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.title("À Propos")
    st.write("Projet d'audit hospitalier pour l'amélioration du système de santé au Cameroun.")
