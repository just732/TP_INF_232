import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
import hashlib

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus", layout="wide", initial_sidebar_state="collapsed")

# --- FONCTIONS DE SÉCURITÉ ---
def hasher_mdp(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('patient_plus_final.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS utilisateurs (username TEXT PRIMARY KEY, password TEXT, nom TEXT, prenom TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS formulaires (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, hopital TEXT, 
                    service TEXT, note INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- STYLE CSS (BLEU NUIT) ---
st.markdown("""
    <style>
    .stApp { background-color: #001122; color: #e0e0e0; }
    h1, h2, h3 { color: #00d4ff !important; }
    .stButton>button {
        background-color: #00d4ff !important; color: #001122 !important;
        font-weight: bold !important; border-radius: 25px !important;
        width: 100% !important;
    }
    input { background-color: white !important; color: black !important; border-radius: 10px !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'user_connecte' not in st.session_state: st.session_state.user_connecte = None

def naviguer(nom_page):
    st.session_state.page = nom_page

# --- BARRE DE NAVIGATION ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
cols = st.columns([2, 1, 1, 1, 1])
with cols[0]: st.markdown("<h2 style='margin:0;'>PATIENT <span style='color:white;'>PLUS</span></h2>", unsafe_allow_html=True)
if cols[1].button("ACCUEIL"): naviguer("Accueil")
if cols[2].button("SERVICES"): naviguer("Services")
if cols[3].button("STATISTIQUES"): naviguer("Stats")
if st.session_state.user_connecte:
    if cols[4].button("DÉCONNEXION"): 
        st.session_state.user_connecte = None
        naviguer("Accueil")
else:
    if cols[4].button("S'IDENTIFIER"): naviguer("Auth")

# ==========================================
# PAGE D'ACCUEIL
# ==========================================
if st.session_state.page == "Accueil":
    st.title("Collecte de données sur la qualité de service hospitalier")
    st.markdown("""
    **Patient Plus** est une plateforme citoyenne permettant de mesurer la qualité des soins au Cameroun. 
    En remplissant nos formulaires, vous contribuez à améliorer l'accueil et la sécurité dans nos hôpitaux.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg", use_column_width=True)
    
    if not st.session_state.user_connecte:
        if st.button("CRÉER UN COMPTE POUR REMPLIR UN FORMULAIRE"): naviguer("Auth")

# ==========================================
# PAGE STATISTIQUES (DIAGRAMMES & CAMEMBERTS)
# ==========================================
elif st.session_state.page == "Stats":
    st.title("📊 Statistiques des formulaires")
    conn = sqlite3.connect('patient_plus_final.db')
    df = pd.read_sql_query("SELECT * FROM formulaires", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée disponible pour le moment.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            moyennes = df.groupby('hopital')['note'].mean().reset_index()
            fig1 = px.bar(moyennes, x='hopital', y='note', title="Note moyenne par Hôpital", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            fig2 = px.pie(df, names='service', title="Répartition par Service", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# AUTHENTIFICATION
# ==========================================
elif st.session_state.page == "Auth":
    st.title("🔐 Identification")
    choix = st.radio("Action :", ["Se connecter", "Créer un compte"])
    user = st.text_input("Identifiant")
    mdp = st.text_input("Mot de passe", type="password")
    
    if choix == "Créer un compte":
        nom = st.text_input("Nom")
        if st.button("S'INSCRIRE"):
            conn = sqlite3.connect('patient_plus_final.db')
            c = conn.cursor()
            try:
                c.execute('INSERT INTO utilisateurs VALUES (?,?,?,?)', (user, hasher_mdp(mdp), nom, ""))
                conn.commit()
                st.success("Compte créé !")
            except: st.error("Identifiant déjà pris.")
            conn.close()
    else:
        if st.button("SE CONNECTER"):
            conn = sqlite3.connect('patient_plus_final.db')
            c = conn.cursor()
            c.execute('SELECT * FROM utilisateurs WHERE username=? AND password=?', (user, hasher_mdp(mdp)))
            if c.fetchone():
                st.session_state.user_connecte = user
                naviguer("Formulaire")
                st.rerun()
            else: st.error("Erreur d'identifiants.")
            conn.close()

# ==========================================
# PAGE FORMULAIRE (AVEC CALENDRIER AJUSTÉ)
# ==========================================
elif st.session_state.page == "Formulaire":
    if not st.session_state.user_connecte: naviguer("Auth"); st.rerun()

    st.title("📝 Remplir un formulaire de satisfaction")
    with st.form("audit_form"):
        st.subheader("1. Informations Personnelles")
        
        # --- CALENDRIER AJUSTÉ : 1915 À 2026 ---
        date_naissance = st.date_input(
            "Votre date de naissance",
            min_value=datetime(1915, 1, 1),
            max_value=datetime(2026, 12, 31),
            value=datetime(1995, 1, 1)
        )
        
        st.subheader("2. Détails Hospitaliers")
        # Saisie libre du nom de l'hôpital
        hopital_saisi = st.text_input("Nom de l'hôpital consulté")
        service_f = st.selectbox("Service fréquenté", ["Urgences", "Imagerie", "Laboratoire", "Chirurgie", "Pharmacie"])

        st.subheader("3. Note de satisfaction")
        note_f = st.select_slider("Quelle note donnez-vous au service ? (1 à 5)", options=[1, 2, 3, 4, 5])
        
        if st.form_submit_button("ENVOYER LE FORMULAIRE"):
            if not hopital_saisi:
                st.error("Veuillez saisir le nom de l'hôpital.")
            else:
                conn = sqlite3.connect('patient_plus_final.db')
                c = conn.cursor()
                c.execute('INSERT INTO formulaires (user, hopital, service, note, date) VALUES (?,?,?,?,?)', 
                          (st.session_state.user_connecte, hopital_saisi, service_f, note_f, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success("Formulaire envoyé !")
                naviguer("Stats")
                st.rerun()
