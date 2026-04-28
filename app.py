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

# --- STYLE CSS (BLEU NUIT & ÉLÉGANCE) ---
st.markdown("""
    <style>
    /* Global - Bleu Nuit */
    .stApp {
        background-color: #001122;
        color: #e0e0e0;
    }
    
    /* Barre de Navigation */
    .nav-bar {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 5%; background: #001a33;
        border-bottom: 2px solid #00d4ff; position: fixed; top: 0; width: 100%; z-index: 999;
    }
    
    /* Titres et Textes */
    h1, h2, h3 { color: #00d4ff !important; }
    
    /* Boutons personnalisés */
    .stButton>button {
        background-color: #00d4ff !important; color: #001122 !important;
        font-weight: bold !important; border-radius: 25px !important;
        border: none !important; width: 100% !important; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ffffff !important; transform: scale(1.05); }

    /* Champs de saisie */
    input { background-color: white !important; color: black !important; border-radius: 10px !important; }
    
    /* Cacher les éléments Streamlit par défaut */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'user_connecte' not in st.session_state: st.session_state.user_connecte = None

def naviguer(nom_page):
    st.session_state.page = nom_page

# ==========================================
# BARRE DE NAVIGATION (FONCTIONNELLE)
# ==========================================
st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True) # Espace pour la nav fixe
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
# PAGE D'ACCUEIL : BUT DE L'APPLICATION
# ==========================================
if st.session_state.page == "Accueil":
    st.title("Améliorer la qualité de service hospitalier")
    st.markdown("""
    ### Bienvenue sur Patient Plus
    **Patient Plus** est une plateforme citoyenne de collecte de données sur la qualité de service des différents services hospitaliers de notre pays.
    
    Nous croyons que la voix du patient est le levier principal pour transformer notre système de santé. En partageant votre expérience de manière confidentielle, vous aidez l'État et les hôpitaux à identifier les points à améliorer (accueil, réactivité, hygiène, disponibilité des soins).
    
    **Pourquoi nous faire confiance ?**
    - Vos données personnelles sont protégées et cryptées.
    - Seules les statistiques globales sont publiées.
    - Votre témoignage impacte directement la gestion hospitalière.
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg", caption="Hôpital Général de Yaoundé", use_column_width=True)
    
    st.markdown("<center>", unsafe_allow_html=True)
    if st.button("CRÉER UN COMPTE POUR REMPLIR UN FORMULAIRE"): naviguer("Auth")
    st.markdown("</center>", unsafe_allow_html=True)

# ==========================================
# PAGE SERVICES : PRÉSENTATION
# ==========================================
elif st.session_state.page == "Services":
    st.title("Nos Domaines d'Évaluation")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Diagnostic et Urgences")
        st.write("Nous mesurons les délais d'attente au triage, la disponibilité des équipements (Scanner/IRM) et la fiabilité des laboratoires.")
        st.subheader("2. Médecine et Chirurgie")
        st.write("Évaluation de la sécurité des soins (Règle des 5B), de l'hygiène nosocomiale et du suivi des dossiers patients.")
    with col2:
        st.subheader("3. Supports et Logistique")
        st.write("Analyse des stocks de la pharmacie, de la disponibilité des lits et de la maintenance hôtelière.")
        st.subheader("4. Expérience Patient")
        st.write("Évaluation transversale : Accueil, clarté de l'information, gestion de la douleur et respect de la dignité.")

# ==========================================
# PAGE STATISTIQUES (DYNAMIQUES : CAMEMBERTS ET DIAGRAMMES)
# ==========================================
elif st.session_state.page == "Stats":
    st.title("📊 Statistiques Nationales de Performance")
    
    conn = sqlite3.connect('patient_plus_final.db')
    df = pd.read_sql_query("SELECT * FROM formulaires", conn)
    conn.close()

    if df.empty:
        st.info("Aucune donnée collectée pour le moment. Les statistiques s'afficheront ici après les premiers formulaires.")
    else:
        st.write("Ces données sont issues des recherches et des formulaires remplis par les utilisateurs de la plateforme.")
        
        c1, c2 = st.columns(2)
        with c1:
            # Diagramme en barres : Note moyenne par hôpital saisi
            moyennes = df.groupby('hopital')['note'].mean().reset_index()
            fig1 = px.bar(moyennes, x='hopital', y='note', title="Note moyenne de satisfaction par Hôpital", 
                          template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            st.plotly_chart(fig1, use_container_width=True)
        
        with c2:
            # Camembert : Répartition des formulaires par service
            fig2 = px.pie(df, names='service', title="Répartition des signalements par Service", 
                          hole=0.4, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# AUTHENTIFICATION (INSCRIPTION/CONNEXION)
# ==========================================
elif st.session_state.page == "Auth":
    st.title("🔐 Espace Utilisateur")
    choix = st.radio("Souhaitez-vous :", ["Se connecter", "Créer un compte"])
    
    with st.container():
        user = st.text_input("Identifiant (Email ou Téléphone)")
        mdp = st.text_input("Mot de passe", type="password")
        
        if choix == "Créer un compte":
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            if st.button("S'INSCRIRE"):
                conn = sqlite3.connect('patient_plus_final.db')
                c = conn.cursor()
                try:
                    c.execute('INSERT INTO utilisateurs VALUES (?,?,?,?)', (user, hasher_mdp(mdp), nom, prenom))
                    conn.commit()
                    st.success("Compte créé ! Connectez-vous maintenant.")
                except: st.error("Cet identifiant est déjà utilisé.")
                conn.close()
        else:
            if st.button("SE CONNECTER"):
                conn = sqlite3.connect('patient_plus_final.db')
                c = conn.cursor()
                c.execute('SELECT * FROM utilisateurs WHERE username=? AND password=?', (user, hasher_mdp(mdp)))
                resultat = c.fetchone()
                if resultat:
                    st.session_state.user_connecte = user
                    naviguer("Formulaire")
                    st.rerun()
                else: st.error("Identifiants incorrects.")
                conn.close()

# ==========================================
# PAGE FORMULAIRE (DYNAMIQUE)
# ==========================================
elif st.session_state.page == "Formulaire":
    if not st.session_state.user_connecte:
        st.warning("Veuillez vous connecter pour remplir le formulaire.")
        naviguer("Auth")
        st.rerun()

    st.title("📝 Remplir un formulaire de satisfaction")
    
    with st.form("audit_form"):
        st.subheader("1. Informations Personnelles")
        col_id1, col_id2 = st.columns(2)
        nom_f = col_id1.text_input("Nom")
        pre_f = col_id2.text_input("Prénom")
        dob_f = col_id1.date_input("Date de naissance", min_value=datetime(1915, 1, 1), value=datetime(1995, 1, 1))
        tel_f = col_id2.text_input("Email ou Numéro de contact")

        st.subheader("2. Détails de l'Hôpital")
        # --- SAISIE MANUELLE ---
        hopital_nom = st.text_input("Nom de l'hôpital que vous avez consulté")
        service_f = st.selectbox("Service fréquenté", ["Urgences", "Imagerie", "Laboratoire", "Chirurgie", "Pharmacie"])

        st.subheader("3. Évaluation du Service")
        note_f = st.select_slider("Note globale du service (1: Médiocre - 5: Excellent)", options=[1, 2, 3, 4, 5])
        
        # Questions dynamiques
        if service_f == "Urgences":
            st.write("Questions Urgences :")
            st.radio("Le délai d'attente au triage était-il raisonnable ?", ["Oui", "Non"])
            st.radio("Le personnel a-t-il réagi immédiatement ?", ["Oui", "Non"])
        elif service_f == "Chirurgie":
            st.write("Questions Chirurgie :")
            st.radio("L'identité a-t-elle été vérifiée avant l'administration des soins ?", ["Oui", "Non"])
            st.radio("Le matériel semblait-il stérile et propre ?", ["Oui", "Non"])
            
        st.subheader("4. Expérience Patient (Général)")
        st.radio("Le personnel s'est-il identifié lors de la prise en charge ?", ["Oui", "Non"])
        st.radio("Le respect de votre intimité a-t-il été garanti ?", ["Oui", "Non"])
        
        if st.form_submit_button("ENVOYER LE FORMULAIRE"):
            if not hopital_nom:
                st.error("Veuillez saisir le nom de l'hôpital.")
            else:
                conn = sqlite3.connect('patient_plus_final.db')
                c = conn.cursor()
                c.execute('INSERT INTO formulaires (user, hopital, service, note, date) VALUES (?,?,?,?,?)', 
                          (st.session_state.user_connecte, hopital_nom, service_f, note_f, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success("Formulaire envoyé avec succès !")
                st.balloons()
                naviguer("Stats")
                st.rerun()
