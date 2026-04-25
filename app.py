import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide")

# --- INITIALISATION NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- STYLE CSS DYNAMIQUE ---
def local_css():
    if st.session_state.page == "Home":
        # THEME STUDIO PLEY (Sombre / Néon)
        st.markdown("""
            <style>
            [data-testid="stSidebar"], header { display: none !important; }
            .stApp {
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                color: white;
            }
            /* Hero Section */
            .hero-box {
                padding: 60px;
                text-align: left;
                background: url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
                background-size: cover;
                border-radius: 30px;
                box-shadow: inset 0 0 0 2000px rgba(15, 12, 41, 0.7);
                margin-bottom: 40px;
            }
            .hero-title { font-size: 70px !important; font-weight: 800; color: #ff00ff; text-shadow: 0 0 20px #ff00ff; }
            
            /* Cards Neon */
            .neon-card {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 0, 255, 0.3);
                padding: 25px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                height: 400px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                box-shadow: 0 0 15px rgba(255, 0, 255, 0.1);
            }
            /* Fonds images bulles */
            .bubble-1 { background: linear-gradient(to top, #0f0c29, transparent), url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg'); background-size: cover; }
            .bubble-2 { background: linear-gradient(to top, #0f0c29, transparent), url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg'); background-size: cover; }
            
            /* Bouton Studio */
            div.stButton > button {
                background: linear-gradient(90deg, #ff00ff, #00ffff) !important;
                color: white !important;
                border-radius: 50px !important;
                padding: 20px 60px !important;
                font-size: 24px !important;
                font-weight: bold !important;
                border: none !important;
                box-shadow: 0 0 20px rgba(255, 0, 255, 0.5) !important;
                margin-top: 50px;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        # THEME GOOGLE FORM (Clair / Épuré)
        st.markdown("""
            <style>
            [data-testid="stSidebar"], header { display: none !important; }
            .stApp { background-color: #f0ebf8; color: #202124; }
            .form-container {
                background-color: white;
                border-radius: 10px;
                padding: 40px;
                max-width: 800px;
                margin: 20px auto;
                border-top: 10px solid #673ab7;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            label { color: #202124 !important; font-weight: 500 !important; font-size: 16px !important; }
            div.stButton > button {
                background-color: #673ab7 !important;
                color: white !important;
                border-radius: 4px !important;
                padding: 10px 24px !important;
            }
            </style>
        """, unsafe_allow_html=True)

local_css()

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('patient_plus_studio.db', check_same_thread=False)
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

# --- LOGIQUE NAVIGATION ---
def nav(page_name):
    st.session_state.page = page_name

# --- PAGE 1 : ACCUEIL (NEON STUDIO) ---
if st.session_state.page == "Home":
    st.markdown("""
        <div class="hero-box">
            <h1 class="hero-title">PATIENT PLUS</h1>
            <p style="font-size:24px;">Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="neon-card bubble-1">
                <h3 style="color:#00ffff;">📊 Audit Hospitalier</h3>
                <p><b>Statistiques CMR :</b> 172 hôpitaux publics audités.<br>
                Seuls 48% remplissent les critères de performance.<br>
                Flux annuel : 4 000 à 6 000 patients par établissement régional.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="neon-card bubble-2">
                <h3 style="color:#ff00ff;">👶 Services Maternité</h3>
                <p><b>Urgence Sociale :</b> 35,9% des accouchements se font sans assistance médicale.<br>
                L'audit permet d'identifier les zones de danger pour les nouveau-nés.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🚀 DÉMARRER L'AUDIT"):
        nav("Form")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE (GOOGLE FORM STYLE) ---
elif st.session_state.page == "Form":
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#673ab7;'>Questionnaire de Satisfaction Patient</h2>", unsafe_allow_html=True)
    st.write("Veuillez remplir ce formulaire honnêtement pour nous aider à améliorer la santé publique.")
    
    with st.form("google_form", clear_on_submit=True):
        st.markdown("### 📋 Identification")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom")
        prenom = c2.text_input("Prénom")
        age = c1.number_input("Âge", 0, 110, 25)
        sexe = c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier = c1.text_input("Métier")
        dob = c2.date_input("Date de naissance")
        domicile = c1.text_input("Lieu de résidence")
        email = c2.text_input("Email de contact")

        st.markdown("### 🏥 Séjour Hospitalier")
        hopital = st.selectbox("Hôpital visité", ["Hôpital Général", "Hôpital Central", "Laquintinie", "Hôpital de District"])
        service = st.text_input("Service (Urgences, Pédiatrie...)")
        maladie = st.text_input("Motif de consultation")
        
        st.markdown("### ⭐ Évaluation")
        attente = st.slider("Temps d'attente (min)", 0, 300, 30)
        attitude = st.selectbox("Attitude du personnel", ["Médiocre", "Moyenne", "Satisfaisante", "Excellente"])
        
        col_inf, col_med = st.columns(2)
        e_inf = col_inf.select_slider("Note Infirmières", options=["1","2","3","4","5"])
        j_inf = col_inf.text_area("Justification Infirmières")
        e_med = col_med.select_slider("Note Médecins", options=["1","2","3","4","5"])
        j_med = col_med.text_area("Justification Médecins")

        st.markdown("### 💡 Suggestions")
        rdv = st.radio("Favorable au RDV en ligne ?", ["Oui", "Non"])
        sug = st.text_area("Vos recommandations pour améliorer ce service")

        if st.form_submit_button("ENVOYER LES RÉPONSES"):
            conn = sqlite3.connect('patient_plus_studio.db')
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email, maladie, service, hopital, attente, attitude_g, eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                      (nom, prenom, age, sexe, metier, str(dob), domicile, email, maladie, service, hopital, attente, attitude, e_inf, j_inf, e_med, j_med, rdv, sug))
            conn.commit()
            conn.close()
            nav("Success")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3 : SUCCÈS & ANALYSE ---
elif st.session_state.page == "Success":
    st.markdown("<div class='form-container' style='text-align:center;'>", unsafe_allow_html=True)
    st.header("Merci !")
    st.write("Votre audit a été enregistré avec succès.")
    
    if st.button("📊 VOIR LES DIAGRAMMES D'ANALYSE"):
        nav("Analysis")
        st.rerun()
    
    if st.button("🏠 RETOUR À L'ACCUEIL"):
        nav("Home")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 4 : ANALYSE ---
elif st.session_state.page == "Analysis":
    st.markdown("<h2 style='text-align:center; color:#673ab7;'>Analyse Descriptive des Données</h2>", unsafe_allow_html=True)
    
    conn = sqlite3.connect('patient_plus_studio.db')
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df, names='attitude_g', title="Satisfaction Globale"), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x='hopital', y='attente', title="Temps d'attente moyen"), use_container_width=True)
    
    if st.button("🏠 RETOUR À L'ACCUEIL"):
        nav("Home")
        st.rerun()
