import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide")

# --- INITIALISATION DE LA NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"

# --- DESIGN CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    /* Masquer le menu latéral et le header Streamlit */
    [data-testid="stSidebar"], header { display: none !important; }
    .stApp { margin-top: -50px; }

    /* Fond d'écran global (Image 3) */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover;
        background-attachment: fixed;
    }

    /* Style des Bulles avec Images de fond */
    .bubble-container {
        display: flex;
        gap: 20px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 30px;
    }
    
    .bubble {
        width: 45%;
        min-width: 300px;
        height: 400px;
        border-radius: 30px;
        padding: 30px;
        position: relative;
        overflow: hidden;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }

    /* Fond image pour Bulle 1 (Pédiatrie) */
    .bubble-1 {
        background: linear-gradient(to top, rgba(0,0,0,0.9), rgba(0,0,0,0.2)), 
                    url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg');
        background-size: cover;
    }

    /* Fond image pour Bulle 2 (Maternité) */
    .bubble-2 {
        background: linear-gradient(to top, rgba(0,0,0,0.9), rgba(0,0,0,0.2)), 
                    url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg');
        background-size: cover;
    }

    .bubble h3 { font-size: 24px; font-weight: bold; margin-bottom: 10px; }
    .bubble p { font-size: 15px; line-height: 1.4; }

    /* Texte d'objectif central */
    .hero-text {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        color: white;
        margin: 50px 0;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }

    /* Bouton Central Rouge Patient Plus */
    .main-button-container {
        text-align: center;
        margin-top: 50px;
        padding-bottom: 100px;
    }
    
    .stButton>button {
        background-color: #e1395f !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 20px 60px !important;
        font-size: 24px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 10px 20px rgba(225, 57, 95, 0.4) !important;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); }

    /* Formulaire Style Blanc */
    .form-container {
        background: white;
        padding: 40px;
        border-radius: 30px;
        color: #333;
        margin: 0 auto;
        max-width: 900px;
    }
    label { color: #39559e !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('audit_cameroun_v7.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, dob TEXT, 
                    domicile TEXT, email TEXT, maladie TEXT, service TEXT, hopital TEXT, 
                    attente INTEGER, attitude_g TEXT, eval_inf TEXT, justif_inf TEXT, 
                    eval_med TEXT, justif_med TEXT, rdv_ligne TEXT, suggestions TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- LOGIQUE DE NAVIGATION ---
def change_page(name):
    st.session_state.page = name

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:60px; color:white;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='hero-text'>Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</div>", unsafe_allow_html=True)

    # Bulles d'info avec images en fond
    st.markdown("""
        <div class="bubble-container">
            <div class="bubble bubble-1">
                <h3>📊 Performance Hospitalière</h3>
                <p><b>Hôpitaux Régionaux :</b> 4 000 à 6 000 hospitalisations/an (surcharge critique).<br>
                <b>Efficacité :</b> Seuls 48% des 172 hôpitaux publics remplissent les critères de bonne performance.<br>
                <b>Suivi :</b> Les consultations pédiatriques restent un indicateur de santé prioritaire.</p>
            </div>
            <div class="bubble bubble-2">
                <h3>👶 Santé Maternelle</h3>
                <p><b>Admission Institutionnelle :</b> Environ 35,9% des accouchements se font encore à domicile sans assistance médicale au Cameroun.<br>
                <b>Impact :</b> Ce chiffre réduit le taux de sécurité dans nos maternités et nécessite une réforme urgente.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Bouton de redirection vers le formulaire
    st.markdown("<div class='main-button-container'>", unsafe_allow_html=True)
    if st.button("🚀 DÉMARRER L'AUDIT MAINTENANT"):
        change_page("Formulaire")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif st.session_state.page == "Formulaire":
    st.markdown("<div style='text-align:center; padding: 20px;'><button onclick='window.location.reload()' style='background:none; border:none; color:white; cursor:pointer;'>⬅ Retour à l'accueil</button></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#39559e;'>Questionnaire de Qualité</h2>", unsafe_allow_html=True)
        
        with st.form("audit_form", clear_on_submit=True):
            st.subheader("1. État Civil")
            c1, c2 = st.columns(2)
            nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
            age = c1.number_input("Âge", 0, 110, 25)
            sexe = c2.selectbox("Sexe", ["Masculin", "Féminin"])
            metier = c1.text_input("Métier")
            dob = c2.date_input("Date de naissance")
            domicile, email = c1.text_input("Lieu de résidence"), c2.text_input("Email")

            st.subheader("2. Contexte Médical")
            hopital = st.selectbox("Établissement", ["Hôpital Général", "Hôpital Central", "Hôpital de Laquintinie", "Hôpital de District"])
            service, maladie = st.text_input("Service (ex: Urgences)"), st.text_input("Motif / Maladie")
            
            st.subheader("3. Évaluation Personnel")
            attente = st.slider("Temps d'attente (min)", 0, 300, 30)
            attitude_g = st.selectbox("Attitude globale", ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"])
            
            ci, cm = st.columns(2)
            e_inf, j_inf = ci.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"]), ci.text_area("Justif. Infirmières")
            e_med, j_med = cm.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"]), cm.text_area("Justif. Médecins")

            st.subheader("4. Suggestions")
            rdv = st.radio("Favorable aux RDV en ligne avec un médecin spécifique ?", ["Oui", "Non"])
            sug = st.text_area("Mesures concrètes pour améliorer le service")

            if st.form_submit_button("VALIDER L'AUDIT"):
                conn = sqlite3.connect('audit_cameroun_v7.db')
                c = conn.cursor()
                c.execute("INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email, maladie, service, hopital, attente, attitude_g, eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                          (nom, prenom, age, sexe, metier, str(dob), domicile, email, maladie, service, hopital, attente, attitude_g, e_inf, j_inf, e_med, j_med, rdv, sug))
                conn.commit()
                conn.close()
                st.success("Audit enregistré !")
                st.balloons()
        st.markdown("</div>", unsafe_allow_html=True)
