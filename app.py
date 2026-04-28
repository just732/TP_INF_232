import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime

# --- CONFIGURATION ET THÈME ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide")

def local_css():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(rgba(0, 43, 92, 0.85), rgba(0, 43, 92, 0.85)), 
                        url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
            background-size: cover; background-attachment: fixed; color: white;
        }
        .main-card {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 30px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 20px;
        }
        h1, h2, h3 { color: #00d4ff !important; }
        .stButton>button {
            background-color: #00d4ff !important; color: #002b5c !important;
            font-weight: bold; border-radius: 25px; width: 100%;
        }
        .confidential-tag {
            background-color: #28a745; color: white; padding: 5px 15px;
            border-radius: 50px; font-size: 14px; font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# --- GESTION DE LA BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('patient_plus.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, nom TEXT, prenom TEXT)')
    c.execute('''CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, hopital TEXT, 
                    service TEXT, reponses TEXT, date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- LOGIQUE DE NAVIGATION ---
if 'step' not in st.session_state: st.session_state.step = "Accueil"
if 'user' not in st.session_state: st.session_state.user = None

def go_to(step_name):
    st.session_state.step = step_name
    st.rerun()

# --- DONNÉES DE L'APPLICATION ---
hospitals = {
    "Hôpital Général de Yaoundé (HGY)": "Yaoundé",
    "Hôpital Général de Douala (HGD)": "Douala",
    "Hôpital Laquintinie": "Douala",
    "Hôpital Central de Yaoundé (HCY)": "Yaoundé",
    "Hôpital Gynéco-Obstétrique (HGOPY)": "Yaoundé",
    "Hôpital Gynéco-Obstétrique (HGOPD)": "Douala"
}

services_questions = {
    "Urgences": [
        "Quel est le délai moyen entre votre arrivée et le premier triage ?",
        "Le protocole d'accueil des urgences était-il affiché ?",
        "Le personnel a-t-il réagi immédiatement à votre état ?"
    ],
    "Imagerie (Scanner/IRM)": [
        "Les équipements semblaient-ils bien entretenus ?",
        "Quel a été le délai de remise de votre compte-rendu ?",
        "Avez-vous été informé des précautions liées à l'examen ?"
    ],
    "Laboratoire": [
        "L'étiquetage de vos prélèvements a-t-il été fait devant vous ?",
        "Le délai d'attente pour la prise de sang était-il acceptable ?",
        "La traçabilité semble-t-elle rigoureuse ?"
    ],
    "Médecine et Chirurgie": [
        "Le personnel a-t-il vérifié votre identité avant chaque soin (Règle des 5B) ?",
        "L'hygiène des mains a-t-elle été respectée par les soignants ?",
        "Le dossier médical a-t-il été renseigné en votre présence ?",
        "Une check-list sécurité a-t-elle été remplie (si chirurgie) ?"
    ],
    "Pharmacie et Logistique": [
        "Y a-t-il eu une rupture de stock sur vos médicaments ?",
        "La température de conservation semblait-elle contrôlée ?",
        "Le système d'appel-malade dans votre chambre fonctionnait-il ?"
    ]
}

questions_transversales = [
    "Le personnel s'est-il identifié lors de la prise en charge ?",
    "Avez-vous reçu une explication claire sur votre traitement ?",
    "Votre douleur a-t-elle été évaluée régulièrement (échelle EVA) ?",
    "Le respect de votre intimité a-t-il été garanti ?"
]

# --- PAGES ---

# 1. ACCUEIL : BUT ET PUBLICITÉ
if st.session_state.step == "Accueil":
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.title("🛡️ Patient Plus : Votre Voix pour une Santé d'Excellence")
    st.markdown("""
        ### Devenez acteur du changement !
        **Patient Plus** est la plateforme nationale dédiée à l'audit de la qualité des soins au Cameroun. 
        Notre mission est de transformer nos hôpitaux en centres d'excellence grâce à **VOS** expériences.
        
        **Pourquoi participer ?**
        Chaque formulaire rempli est une donnée précieuse qui remonte directement aux autorités sanitaires pour corriger les failles (attente, hygiène, équipements).
        
        <span class='confidential-tag'>🔒 Confidentialité Garantie</span>
        *Vos réponses sont anonymisées. Votre identité sert uniquement à certifier l'authenticité de l'audit.*
    """, unsafe_allow_html=True)
    if st.button("Découvrir les Services Hospitaliers →"): go_to("Services")
    st.markdown("</div>", unsafe_allow_html=True)

# 2. SERVICES HOSPITALIERS
elif st.session_state.step == "Services":
    st.title("🏥 Notre Réseau de Soins de Haut Niveau")
    st.write("Le Cameroun dispose d'infrastructures de référence réparties sur tout le territoire.")
    
    df_hosp = pd.DataFrame([
        {"Nom": "Hôpital Général (Ydé/Dla)", "Catégorie": "1ère (Général)", "Spécialité": "Oncologie, Dialyse, Chirurgie complexe"},
        {"Nom": "Hôpital Central (Ydé/Dla)", "Catégorie": "2ème (Central)", "Spécialité": "Urgences traumatiques, Proximité"},
        {"Nom": "Hôpital Gynéco-Obstétrique", "Catégorie": "1ère (Général)", "Spécialité": "Santé Mère-Enfant"}
    ])
    st.table(df_hosp)
    
    st.info("💡 Saviez-vous ? Le pays compte 4 hôpitaux généraux, 4 hôpitaux centraux et 164 hôpitaux de district.")
    if st.button("Voir les Performances Nationales →"): go_to("Stats")

# 3. STATISTIQUES DE PERFORMANCE
elif st.session_state.step == "Stats":
    st.title("📊 Baromètre de la Santé au Cameroun")
    st.markdown("""
        Voici l'état actuel du système de santé que nous cherchons à améliorer ensemble :
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Efficience Globale", "48%", "Hôpitaux Publics")
    col2.metric("Fréquentation Privé", "55.6%", "Concurrence Douala")
    col3.metric("Mortalité Maternelle", "550", "/100k naissances")

    st.write("---")
    st.subheader("Dépenses de Santé")
    st.warning("⚠️ Les ménages supportent 94% des coûts directs de santé. Patient Plus aide à optimiser ces coûts en exigeant une meilleure qualité.")
    
    if st.button("Commencer mon Audit (Connexion) →"): go_to("Login")

# 4. AUTHENTIFICATION (LOGIN/SIGNUP CLASSIQUE)
elif st.session_state.step == "Login":
    st.title("🔐 Accès Sécurisé")
    tab1, tab2 = st.tabs(["Connexion", "Créer un compte"])
    
    with tab1:
        u = st.text_input("Email ou Numéro")
        p = st.text_input("Mot de passe", type="password")
        if st.button("Se connecter"):
            # Simulation connexion
            st.session_state.user = u
            go_to("Formulaire")
            
    with tab2:
        st.markdown("### Rejoignez la communauté des auditeurs")
        new_nom = st.text_input("Nom")
        new_pre = st.text_input("Prénom")
        new_dob = st.date_input("Date de naissance")
        new_u = st.text_input("Email ou Téléphone")
        new_p = st.text_input("Choisir un mot de passe", type="password")
        if st.button("Créer mon compte"):
            st.success("Compte créé avec succès ! Connectez-vous.")

# 5. LE FORMULAIRE DYNAMIQUE
elif st.session_state.step == "Formulaire":
    st.title("📝 Formulaire d'Audit Qualité")
    
    # --- PAGE 1 : IDENTITÉ ---
    with st.expander("Étape 1 : Identification du Patient", expanded=True):
        st.write(f"Connecté en tant que : **{st.session_state.user}**")
        c1, c2 = st.columns(2)
        ident_nom = c1.text_input("Nom", placeholder="Nom de famille")
        ident_pre = c2.text_input("Prénom", placeholder="Prénoms")
        ident_dob = c1.date_input("Date de naissance", min_value=datetime(1920,1,1))
        ident_cont = c2.text_input("Email ou Téléphone de contact")

    # --- PAGE 2 : HÔPITAL ET SERVICE ---
    with st.expander("Étape 2 : Détails de la Consultation", expanded=True):
        hopital_choisi = st.selectbox("Sélectionnez l'établissement consulté", list(hospitals.keys()))
        service_choisi = st.selectbox("Quel service avez-vous fréquenté ?", list(services_questions.keys()))

    # --- PAGE 3 : QUESTIONS DYNAMIQUES ---
    st.subheader(f"🛠️ Évaluation du Service : {service_choisi}")
    reponses = {}
    
    # Questions spécifiques
    for q in services_questions[service_choisi]:
        reponses[q] = st.select_slider(q, options=["Très Insatisfait", "Insatisfait", "Neutre", "Satisfait", "Très Satisfait"])
    
    # Questions transversales
    st.subheader("🌟 Expérience Patient (Général)")
    for q in questions_transversales:
        reponses[q] = st.select_slider(q, options=["Non, pas du tout", "Plutôt non", "Moyennement", "Plutôt oui", "Oui, tout à fait"])

    if st.button("Soumettre l'Audit Final"):
        st.balloons()
        st.success(f"Félicitations ! Votre audit sur l'établissement {hopital_choisi} a été transmis en toute confidentialité. Merci de contribuer à l'amélioration de la santé au Cameroun.")
        if st.button("Retour à l'accueil"): go_to("Accueil")
