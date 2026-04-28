import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.express as px

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide", initial_sidebar_state="collapsed")

# --- STYLE CSS PERSONNALISÉ (Inspiré de l'image) ---
def apply_custom_design():
    st.markdown("""
        <style>
        /* Couleurs de base */
        :root {
            --primary-red: #e60000;
            --dark-bg: #0f0f0f;
            --card-bg: #1a1a1a;
        }

        .stApp {
            background-color: var(--dark-bg);
            color: white;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }

        /* Barre de Navigation */
        .nav-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 5%;
            background: rgba(0,0,0,0.8);
            border-bottom: 2px solid var(--primary-red);
            position: fixed;
            top: 0; width: 100%; z-index: 999;
        }

        /* Hero Section */
        .hero-section {
            padding: 100px 10% 50px 10%;
            background: linear-gradient(135deg, #0f0f0f 0%, #330000 100%);
            text-align: left;
        }
        .hero-title {
            font-size: 50px; font-weight: bold; color: white; margin-bottom: 10px;
        }
        .red-text { color: var(--primary-red); }

        /* Cartes de Services */
        .service-card {
            background: white;
            color: black;
            padding: 25px;
            border-radius: 10px;
            border-bottom: 5px solid var(--primary-red);
            text-align: center;
            transition: 0.3s;
            margin-bottom: 20px;
        }
        .service-card:hover { transform: translateY(-10px); }
        .service-card h4 { color: var(--primary-red); font-weight: bold; }

        /* Boutons */
        .stButton>button {
            background-color: var(--primary-red) !important;
            color: white !important;
            border-radius: 5px !important;
            border: none !important;
            padding: 10px 25px !important;
            font-weight: bold !important;
            width: 100%;
        }

        /* Formulaires */
        div[data-baseweb="input"] { background-color: #262626 !important; }
        input { color: white !important; }
        
        /* Footer Contact */
        .contact-box {
            background: #1a1a1a;
            padding: 40px;
            border-radius: 15px;
            border: 1px solid #333;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_design()

# --- INITIALISATION STATE ---
if 'step' not in st.session_state: st.session_state.step = "HOME"
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

def nav(target):
    st.session_state.step = target
    st.rerun()

# --- DONNÉES ---
hospitals = ["HGY Yaoundé", "HGD Douala", "Laquintinie", "HCY Yaoundé", "HGOPY"]
services = {
    "Diagnostic (Urgences/Imagerie)": [
        "Délai moyen arrivée vs triage ?", 
        "Protocole urgences vitales affiché ?",
        "Maintenance équipements < 6 mois ?",
        "Traçabilité prélèvements garantie ?"
    ],
    "Médecine et Chirurgie": [
        "Vérification règle des '5 B' ?",
        "Observance hygiène des mains ?",
        "Dossier patient renseigné en temps réel ?",
        "Check-list OMS signée au bloc ?"
    ],
    "Supports (Pharmacie/Logistique)": [
        "Rupture stock médicaments essentiels ?",
        "Traçabilité température frigos ?",
        "Disponibilité des lits ?",
        "Système appel-malade fonctionnel ?"
    ]
}

# ==========================================
# HEADER / NAVIGATION (Simulation de l'image)
# ==========================================
st.markdown("""
    <div class="nav-bar">
        <div style="font-weight:bold; font-size:24px;">PATIENT<span class="red-text">PLUS</span></div>
        <div style="display:flex; gap:20px; font-size:14px;">
            <span>ACCUEIL</span> <span>SERVICES</span> <span>STATISTIQUES</span> <span>SÉCURITÉ</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# PAGE 1 : ACCUEIL & BUT (HERO SECTION)
# ==========================================
if st.session_state.step == "HOME":
    st.markdown("""
        <div class="hero-section">
            <p style="letter-spacing:3px; color:var(--primary-red); font-weight:bold; margin-bottom:0;">ZONE GRAPHIQUE</p>
            <h1 class="hero-title">Améliorer la Qualité <br> de nos <span class="red-text">Hôpitaux</span></h1>
            <p style="max-width:500px; color:#ccc;">
                Patient Plus est une plateforme d'audit citoyen. 
                Votre expérience nous permet de mesurer l'efficacité des services 
                et d'assurer une transparence totale pour la santé au Cameroun.
                <br><br><b>Confidentialité :</b> Vos données sont cryptées et traitées anonymement.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("DÉCOUVRIR LES SERVICES →"): nav("SERVICES_LIST")

# ==========================================
# PAGE 2 : PRÉSENTATION DES SERVICES (CARDS)
# ==========================================
elif st.session_state.step == "SERVICES_LIST":
    st.markdown("<br><br><h2 style='text-align:center;'>Nos pôles d' <span class='red-text'>audit</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888;'>Nous évaluons la réactivité, la sécurité et la logistique.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="service-card"><h4>Diagnostic</h4><p>Urgences, Imagerie et Laboratoires. Focus sur la rapidité et la précision.</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="service-card"><h4>Soins</h4><p>Médecine et Chirurgie. Focus sur la sécurité médicamenteuse et l'hygiène.</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="service-card"><h4>Logistique</h4><p>Pharmacie et Maintenance. Focus sur les stocks et l'hôtellerie.</p></div>""", unsafe_allow_html=True)
    
    if st.button("VOIR LES STATISTIQUES D'HÔPITAUX →"): nav("STATS")

# ==========================================
# PAGE 3 : STATISTIQUES (BLOCKS ALTERNÉS)
# ==========================================
elif st.session_state.step == "STATS":
    st.markdown("<br><br><h2>Performance des <span class='red-text'>établissements</span></h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg")
    with c2:
        st.markdown("<h3 class='red-text'>Hôpital Général de Yaoundé</h3>", unsafe_allow_html=True)
        st.write("Référence en oncologie. 48% d'indice d'efficience globale. Focus sur la réduction des temps d'attente en dialyse.")
    
    st.divider()
    
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("<h3 class='red-text'>Statistiques Nationales</h3>", unsafe_allow_html=True)
        st.write("Mortalité maternelle : 550/100k. Dépenses de santé : 94% supportés par les ménages. Votre audit aide à optimiser ces coûts.")
    with c4:
        st.info("📊 81% des hôpitaux de district possèdent un laboratoire fonctionnel.")

    if st.button("CRÉER UN COMPTE POUR RÉPONDRE →"): nav("AUTH")

# ==========================================
# PAGE 4 : AUTHENTIFICATION (CLASSIC LOGIN)
# ==========================================
elif st.session_state.step == "AUTH":
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("<div class='contact-box'><h3>Créer un compte</h3>", unsafe_allow_html=True)
        st.text_input("Nom d'utilisateur")
        st.text_input("Mot de passe", type="password")
        if st.button("S'INSCRIRE"): 
            st.session_state.logged_in = True
            nav("FORM_P1")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_b:
        st.markdown("<h3>Pourquoi s'identifier ?</h3>", unsafe_allow_html=True)
        st.write("L'identification permet de certifier qu'un audit correspond à un patient réel et évite les doublons, garantissant la fiabilité des résultats envoyés au Ministère.")

# ==========================================
# PAGE 5 : FORMULAIRE P1 (IDENTITÉ)
# ==========================================
elif st.session_state.step == "FORM_P1":
    st.markdown("<br><br><h2>Étape 1 : <span class='red-text'>Votre Profil</span></h2>", unsafe_allow_html=True)
    with st.container():
        st.text_input("Nom")
        st.text_input("Prénom")
        # --- MISE À JOUR DEMANDÉE : DATE DE NAISSANCE JUSQU'A 1915 ---
        st.date_input("Date de naissance", 
                      min_value=datetime(1915, 1, 1), 
                      max_value=datetime.now(),
                      value=datetime(1990, 1, 1))
        st.text_input("Adresse Email ou Numéro de téléphone")
        
        if st.button("CONTINUER →"): nav("FORM_P2")

# ==========================================
# PAGE 6 : FORMULAIRE P2 (DYNAMIQUE)
# ==========================================
elif st.session_state.step == "FORM_P2":
    st.markdown("<br><br><h2>Étape 2 : <span class='red-text'>Audit de Service</span></h2>", unsafe_allow_html=True)
    
    hopital = st.selectbox("Hôpital consulté", hospitals)
    service_choisi = st.selectbox("Service visité", list(services.keys()))
    
    st.divider()
    st.subheader(f"Questions spécifiques : {service_choisi}")
    
    # Génération dynamique des questions selon le service
    for q in services[service_choisi]:
        st.radio(q, ["Oui", "Non", "Partiellement", "Ne sait pas"])
        
    st.divider()
    st.subheader("Expérience Patient (Transversal)")
    questions_t = [
        "Le personnel s'est-il identifié ?",
        "Explication claire du traitement reçue ?",
        "Douleur évaluée régulièrement (EVA) ?",
        "Respect de l'intimité garanti ?"
    ]
    for qt in questions_t:
        st.select_slider(qt, options=["Médiocre", "Moyen", "Bien", "Excellent"])

    if st.button("SOUMETTRE L'AUDIT FINAL"):
        st.balloons()
        st.success("Audit transmis avec succès. Merci de votre confiance.")
        if st.button("RETOUR À L'ACCUEIL"): nav("HOME")

# ==========================================
# FOOTER CONTACT (Simulation de l'image)
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
col_f1, col_f2 = st.columns([1, 1])
with col_f1:
    st.markdown("""
        <div class="contact-box">
            <h3 class="red-text">CONTACTEZ-NOUS</h3>
            <p>📍 Yaoundé, Cameroun</p>
            <p>📞 +237 600 00 00 00</p>
            <p>✉️ contact@patientplus.cm</p>
        </div>
    """, unsafe_allow_html=True)
with col_f2:
    st.markdown("<div class='contact-box'>", unsafe_allow_html=True)
    st.text_input("Votre Nom", key="footer_nom")
    st.text_input("Votre Email", key="footer_email")
    st.text_area("Votre Message", key="footer_msg")
    st.button("ENVOYER")
    st.markdown("</div>", unsafe_allow_html=True)
