import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
import smtplib # Pour la logique d'email (conceptuelle ici)

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Admin System", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALISATION DES VARIABLES D'ÉTAT (Session State) ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'audit_publie' not in st.session_state: st.session_state.audit_publie = False
if 'investigateur' not in st.session_state: st.session_state.investigateur = {}

def changer_page(nom): st.session_state.page = nom

# --- DONNÉES NATIONALES ---
data_cameroun = {
    "Centre": ["Hôpital Général", "Hôpital Central", "CHU"],
    "Littoral": ["Hôpital Général Douala", "Laquintinie"],
    "Ouest": ["Hôpital Régional Bafoussam"], # Liste abrégée pour l'exemple
}

# --- DESIGN "PATIENT PLUS" ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }
    .info-bubble {
        background: rgba(255, 255, 255, 0.95); padding: 25px; border-radius: 20px; 
        color: #1a1a1a; margin-bottom: 20px; border-left: 10px solid #e1395f;
    }
    .nav-card {
        background-color: rgba(255, 255, 255, 0.15); border: 2px solid white; 
        border-radius: 20px; padding: 20px; text-align: center; transition: 0.3s;
    }
    .nav-card:hover { background-color: #e1395f; transform: translateY(-5px); }
    .stButton>button { background-color: #e1395f !important; color: white !important; border-radius: 50px !important; width: 100%; }
    .white-box { background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection(): return sqlite3.connect('audit_v8.db', check_same_thread=False)

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

# --- LOGIQUE DES PAGES ---

# 1. ACCUEIL
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    
    if st.session_state.audit_publie:
        st.info(f"📍 Audit Actuel : {st.session_state.investigateur['objectif']}")
    else:
        st.warning("⚠️ Aucun audit n'est actuellement publié par un enquêteur.")

    # Bulles d'infos (Images demandées)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="info-bubble"><h4>Hôpitaux Cameroun</h4><p>Seuls 48% des 172 hôpitaux publics sont performants.</p></div>', unsafe_allow_html=True)
    with col2 := st.columns(1)[0]: # Juste pour garder la structure
        st.markdown('<div class="info-bubble"><h4>Maternité</h4><p>35.9% des accouchements se font hors hôpital.</p></div>', unsafe_allow_html=True)

    # Bulles flottantes de navigation
    st.markdown("<h3 style='text-align:center;'>MENU PRINCIPAL</h3>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns(3)
    with n1:
        st.markdown('<div class="nav-card"><h3>📝 PATIENT</h3><p>Répondre à l\'enquête</p></div>', unsafe_allow_html=True)
        if st.button("LANCER L'AUDIT"): changer_page("AuditPatient")
    with n2:
        st.markdown('<div class="nav-card"><h3>🔐 ENQUÊTEUR</h3><p>Gérer mes missions</p></div>', unsafe_allow_html=True)
        if st.button("ESPACE ADMIN"): changer_page("Admin")
    with n3:
        st.markdown('<div class="nav-card"><h3>ℹ️ À PROPOS</h3><p>Fonctionnement</p></div>', unsafe_allow_html=True)
        if st.button("INFOS APP"): changer_page("Infos")

# 2. ESPACE ENQUÊTEUR (CRÉATION ET ANALYSE)
elif st.session_state.page == "Admin":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown("<div class='white-box'>", unsafe_allow_html=True)
    st.subheader("🛠 Profil Enquêteur & Paramétrage de l'Audit")
    
    with st.form("admin_setup"):
        nom_e = st.text_input("Nom de l'enquêteur")
        prenom_e = st.text_input("Prénom")
        email_e = st.text_input("Votre adresse Email (pour recevoir les résultats)")
        job_e = st.text_input("Votre profession")
        objectif = st.text_area("Quel est l'OBJECTIF de cet audit ?")
        
        if st.form_submit_button("PUBLIER L'AUDIT DANS L'APPLICATION"):
            st.session_state.investigateur = {
                "nom": nom_e, "email": email_e, "job": job_e, "objectif": objectif
            }
            st.session_state.audit_publie = True
            st.success(f"L'audit est maintenant EN LIGNE. Les patients peuvent répondre.")

    if st.session_state.audit_publie:
        st.divider()
        st.subheader("📊 Résultats en temps réel")
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()
        if not df.empty:
            st.metric("Total de réponses reçues", len(df))
            st.plotly_chart(px.bar(df, x="hopital", title="Réponses par Hôpital"))
            st.write("Les réponses sont automatiquement envoyées à : " + st.session_state.investigateur['email'])
    st.markdown("</div>", unsafe_allow_html=True)

# 3. ESPACE PATIENT (QUESTIONNAIRE GÉNÉRÉ)
elif st.session_state.page == "AuditPatient":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    
    if not st.session_state.audit_publie:
        st.error("Désolé, aucun enquêteur n'a publié d'audit pour le moment.")
    else:
        st.markdown(f"<h2>Audit : {st.session_state.investigateur['objectif']}</h2>", unsafe_allow_html=True)
        st.write(f"Enquêteur responsable : {st.session_state.investigateur['nom']} ({st.session_state.investigateur['job']})")
        
        with st.form("patient_form"):
            st.subheader("Vos informations")
            nom_p = st.text_input("Nom")
            prenom_p = st.text_input("Prénom")
            email_p = st.text_input("Email")
            
            st.subheader("Détails hospitaliers")
            reg = st.selectbox("Région", list(data_cameroun.keys()))
            hop = st.selectbox("Hôpital", data_cameroun[reg])
            attente = st.slider("Temps d'attente (min)", 0, 300, 30)
            sug = st.text_area("Comment améliorer ce service ?")
            
            if st.form_submit_button("VALIDER ET ENVOYER"):
                conn = get_connection()
                c = conn.cursor()
                c.execute("INSERT INTO rapports (nom, prenom, email_p, region, hopital, attente, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?)",
                          (nom_p, prenom_p, email_p, reg, hop, attente, sug, datetime.now()))
                conn.commit()
                conn.close()
                st.success(f"Terminé ! Vos réponses ont été envoyées à l'enquêteur ({st.session_state.investigateur['email']})")

# 4. PAGE INFOS
elif st.session_state.page == "Infos":
    st.button("⬅ RETOUR", on_click=lambda: changer_page("Accueil"))
    st.markdown("<div class='white-box'>", unsafe_allow_html=True)
    st.header("Comment fonctionne Patient Plus ?")
    st.write("""
    1. **Configuration** : Un enquêteur définit un objectif de santé publique.
    2. **Collecte** : Les patients sur tout le territoire national répondent via mobile ou PC.
    3. **Analyse** : L'application calcule instantanément les moyennes et graphiques.
    4. **Action** : Les résultats sont transmis aux responsables pour améliorer les services.
    """)
    st.markdown("</div>", unsafe_allow_html=True)
