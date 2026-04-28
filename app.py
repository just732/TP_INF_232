import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus", layout="wide", initial_sidebar_state="collapsed")

# --- STYLE CSS (NAVY BLUE & STYLE SITE WEB) ---
st.markdown("""
    <style>
    /* Global - Couleur Navy Blue */
    .stApp {
        background: linear-gradient(180deg, #001f3f 0%, #003366 100%);
        color: white;
    }
    
    /* Navigation */
    .nav {
        display: flex;
        justify-content: space-between;
        padding: 15px 5%;
        background: rgba(0,0,0,0.3);
        border-bottom: 1px solid #00509d;
        position: fixed; top: 0; width: 100%; z-index: 99;
    }

    /* Hero Section */
    .hero {
        padding: 120px 10% 40px 10%;
        text-align: center;
    }
    .hero-title { font-size: 45px; font-weight: bold; color: #00d4ff; }
    
    /* Cartes */
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #00509d;
        margin-bottom: 20px;
    }

    /* Boutons */
    .stButton>button {
        background-color: #00d4ff !important;
        color: #001f3f !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        width: 100%;
    }

    /* Inputs */
    input { background-color: white !important; color: black !important; }
    
    /* Cacher les éléments Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('patient_plus_data.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_nom TEXT, dob TEXT, hopital TEXT, 
                    service TEXT, satisfaction INTEGER, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- LOGIQUE DE NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"

def naviguer(nom):
    st.session_state.page = nom
    st.rerun()

# ==========================================
# HEADER (SITE WEB)
# ==========================================
st.markdown("""
    <div class="nav">
        <div style="font-weight:bold; font-size:22px; color:#00d4ff;">PATIENT PLUS</div>
        <div style="display:flex; gap:20px; font-size:14px; padding-top:5px;">
            ACCUEIL &nbsp;&nbsp; SERVICES &nbsp;&nbsp; STATISTIQUES &nbsp;&nbsp; AUDIT
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# PAGE D'ACCUEIL
# ==========================================
if st.session_state.page == "Accueil":
    
    # --- HERO SECTION ---
    st.markdown(f"""
        <div class="hero">
            <h1 class="hero-title">Plateforme de Collecte de Données sur la Qualité de Service</h1>
            <p style="font-size:18px; opacity:0.9; max-width:800px; margin:auto; margin-top:20px;">
                Patient Plus est une plateforme dédiée au recueil d'informations précises sur la qualité de prise en charge 
                dans les différents services hospitaliers du pays. Votre contribution permet de bâtir une cartographie 
                réelle des soins pour améliorer la santé de tous.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- SECTION SERVICES ---
    st.markdown("<h2 style='text-align:center; color:#00d4ff;'>Nos Services d'Audit</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="card"><h3>Diagnostic</h3><p>Urgences, Imagerie et Laboratoires. Analyse de la réactivité.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3>Médecine</h3><p>Chirurgie et Soins intensifs. Analyse de la sécurité des soins.</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><h3>Supports</h3><p>Pharmacie et Logistique. Analyse de la disponibilité des produits.</p></div>', unsafe_allow_html=True)

    # --- SECTION STATISTIQUES RÉELLES (Diagrammes et Camemberts) ---
    st.markdown("<h2 style='text-align:center; color:#00d4ff;'>Statistiques des Audits Réalisés</h2>", unsafe_allow_html=True)
    
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM audits", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée collectée pour le moment. Soyez le premier à auditer un hôpital !")
    else:
        c1, c2 = st.columns(2)
        with c1:
            # Diagramme en barres : Audits par hôpital
            fig_bar = px.bar(df['hopital'].value_counts().reset_index(), 
                             x='hopital', y='count', 
                             title="Nombre d'audits par Hôpital",
                             labels={'index': 'Hôpital', 'count': 'Nombre d\'audits'},
                             template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with c2:
            # Camembert : Répartition par service
            fig_pie = px.pie(df, names='service', title="Répartition des audits par Service",
                             hole=0.4, template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- BOUTON D'ACTION ---
    st.markdown("<br><center>", unsafe_allow_html=True)
    if st.button("CRÉER UN COMPTE & DÉMARRER L'AUDIT"):
        naviguer("Inscription")
    st.markdown("</center>", unsafe_allow_html=True)

# ==========================================
# PAGE INSCRIPTION / CONNEXION
# ==========================================
elif st.session_state.page == "Inscription":
    st.markdown("<br><br><br><center><h2>Création de votre compte sécurisé</h2></center>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("auth"):
            st.text_input("Nom d'utilisateur")
            st.text_input("Mot de passe", type="password")
            if st.form_submit_button("S'INSCRIRE ET CONTINUER"):
                naviguer("Formulaire_P1")

# ==========================================
# FORMULAIRE PAGE 1 (IDENTITÉ)
# ==========================================
elif st.session_state.page == "Formulaire_P1":
    st.markdown("<br><br><br><h2>Étape 1 : Informations Personnelles</h2>", unsafe_allow_html=True)
    with st.form("p1"):
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        # Date de naissance jusqu'à 1915
        dob = st.date_input("Date de naissance", 
                            min_value=datetime(1915, 1, 1), 
                            value=datetime(1990, 1, 1))
        contact = st.text_input("Email ou Numéro de téléphone")
        
        if st.form_submit_button("SUIVANT"):
            st.session_state.temp_user = {"nom": nom, "dob": str(dob)}
            naviguer("Formulaire_P2")

# ==========================================
# FORMULAIRE PAGE 2 (AUDIT DYNAMIQUE)
# ==========================================
elif st.session_state.page == "Formulaire_P2":
    st.markdown("<br><br><br><h2>Étape 2 : Évaluation de l'Hôpital</h2>", unsafe_allow_html=True)
    
    with st.form("p2"):
        # L'utilisateur doit entrer le nom de l'hôpital lui-même
        hopital_saisi = st.text_input("Nom de l'Hôpital consulté (Saisie libre)")
        
        service_choisi = st.selectbox("Service visité", 
                                      ["Urgences", "Imagerie", "Laboratoire", "Chirurgie", "Pharmacie"])
        
        st.write("---")
        st.subheader(f"Questions pour le service : {service_choisi}")
        
        # Questions de satisfaction simplifiées pour la démo statistique
        satisfaction = st.slider("Note globale de satisfaction pour ce service (1 à 5)", 1, 5, 3)
        st.text_area("Observations ou remarques particulières")
        
        if st.form_submit_button("TRANSMETTRE L'AUDIT"):
            # Enregistrement dans la base de données
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO audits (patient_nom, dob, hopital, service, satisfaction, date) VALUES (?,?,?,?,?,?)",
                      (st.session_state.temp_user['nom'], st.session_state.temp_user['dob'], 
                       hopital_saisi, service_choisi, satisfaction, str(datetime.now())))
            conn.commit()
            conn.close()
            
            st.success(f"Merci ! L'audit pour l'établissement '{hopital_saisi}' a été enregistré.")
            if st.form_submit_button("RETOUR À L'ACCUEIL"):
                naviguer("Accueil")
