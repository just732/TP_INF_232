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

# --- LOGIQUE CSS (IMAGES DE FOND) ---
def apply_styles():
    if st.session_state.page == "Home":
        # THEME STUDIO PLEY (Sombre / Néon / Images)
        st.markdown("""
            <style>
            [data-testid="stSidebar"], header { display: none !important; }
            
            /* IMAGE DE FOND ACCUEIL (Hôpital Général) */
            .stApp {
                background: linear-gradient(rgba(15, 12, 41, 0.8), rgba(15, 12, 41, 0.8)), 
                            url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
                background-size: cover;
                background-attachment: fixed;
                color: white;
            }

            /* BULLES NEON AVEC IMAGES DE FOND */
            .neon-card {
                padding: 30px;
                border-radius: 25px;
                height: 450px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
                border: 1px solid rgba(255, 255, 255, 0.2);
                margin-bottom: 20px;
            }
            
            /* Bulle 1 : Image Pédiatrie */
            .bubble-pediatrie {
                background: linear-gradient(to top, #0f0c29 30%, transparent), 
                            url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg');
                background-size: cover;
                background-position: center;
            }

            /* Bulle 2 : Image Maternité */
            .bubble-maternite {
                background: linear-gradient(to top, #0f0c29 30%, transparent), 
                            url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg');
                background-size: cover;
                background-position: center;
            }

            .hero-title { font-size: 70px !important; font-weight: 800; color: #ff00ff; text-shadow: 0 0 20px #ff00ff; }
            
            /* Bouton Studio */
            div.stButton > button {
                background: linear-gradient(90deg, #ff00ff, #00ffff) !important;
                color: white !important;
                border-radius: 50px !important;
                padding: 20px 60px !important;
                font-size: 22px !important;
                font-weight: bold !important;
                width: 100%;
                border: none !important;
                box-shadow: 0 0 20px rgba(255, 0, 255, 0.5) !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        # THEME CLAIR STYLE GOOGLE FORM
        st.markdown("""
            <style>
            [data-testid="stSidebar"], header { display: none !important; }
            .stApp { background-color: #f0ebf8; color: #202124; background-image: none; }
            .form-container {
                background-color: white;
                border-radius: 12px;
                padding: 40px;
                max-width: 900px;
                margin: 20px auto;
                border-top: 10px solid #673ab7;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            label { color: #202124 !important; font-weight: bold !important; }
            input { background-color: #f8f9fa !important; color: black !important; }
            </style>
        """, unsafe_allow_html=True)

apply_styles()

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('patient_plus_final_db.db', check_same_thread=False)
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

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Home":
    st.markdown("""
        <div style="padding-top:50px;">
            <h1 class="hero-title">PATIENT PLUS</h1>
            <p style="font-size:26px; font-weight:500;">Améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du Cameroun.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="neon-card bubble-pediatrie">
                <h3 style="color:#00ffff;">Hôpitaux et Performance</h3>
                <p><b>Statistiques :</b> 172 hôpitaux publics audités.<br>
                Seuls 48% remplissent les critères de performance.<br>
                Flux annuel : 4 000 à 6 000 hospitalisations par site régional.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="neon-card bubble-maternite">
                <h3 style="color:#ff00ff;">Maternité et Accouchements</h3>
                <p><b>Alerte Santé :</b> 35,9% des accouchements se font à domicile sans assistance médicale.<br>
                L'audit permet d'orienter les réformes vers la sécurité néonatale.</p>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🚀 LANCER L'AUDIT"):
        st.session_state.page = "Form"
        st.rerun()

# --- PAGE 2 : FORMULAIRE (GOOGLE FORM STYLE) ---
elif st.session_state.page == "Form":
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#673ab7; text-align:center;'>Questionnaire de Satisfaction</h2>", unsafe_allow_html=True)
    
    with st.form("google_form", clear_on_submit=True):
        st.markdown("### 1. Votre Identité")
        c1, c2 = st.columns(2)
        nom = c1.text_input("Nom")
        prenom = c2.text_input("Prénom")
        age = c1.number_input("Âge", 0, 110, 25)
        sexe = c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier = c1.text_input("Métier")
        dob = c2.date_input("Date de naissance")
        dom = c1.text_input("Lieu de résidence")
        mail = c2.text_input("Adresse Email")

        st.markdown("### 2. Détails de la Visite")
        hop = st.selectbox("Hôpital audité", ["Hôpital Général", "Hôpital Central", "Laquintinie", "Hôpital de District"])
        serv = st.text_input("Service (Urgences, Pédiatrie, etc.)")
        mal = st.text_input("Maladie ou motif de présence")
        
        st.markdown("### 3. Évaluation du Personnel")
        att = st.slider("Attente aux urgences (min)", 0, 300, 30)
        att_g = st.selectbox("Attitude globale", ["Insuffisante", "Passable", "Satisfaisante", "Excellente"])
        
        c_i, c_m = st.columns(2)
        e_i = c_i.select_slider("Note Infirmières", options=["1","2","3","4","5"])
        j_i = c_i.text_area("Justifiez la note (Infirmières)")
        e_m = c_m.select_slider("Note Médecins", options=["1","2","3","4","5"])
        j_m = c_m.text_area("Justifiez la note (Médecins)")

        st.markdown("### 4. Suggestions de Réforme")
        rdv = st.radio("Souhaitez-vous des RDV en ligne avec un médecin spécifique ?", ["Oui", "Non"])
        sug = st.text_area("Comment améliorer la qualité du service selon vous ?")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = sqlite3.connect('patient_plus_final_db.db')
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom,prenom,age,sexe,metier,dob,domicile,email,maladie,service,hopital,attente,attitude_g,eval_inf,justif_inf,eval_med,justif_med,rdv_ligne,suggestions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                      (nom, prenom, age, sexe, metier, str(dob), dom, mail, mal, serv, hop, att, att_g, e_i, j_i, e_m, j_m, rdv, sug))
            conn.commit()
            conn.close()
            st.session_state.page = "Analysis"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3 : ANALYSE ---
elif st.session_state.page == "Analysis":
    st.markdown("<h1 style='text-align:center; color:#673ab7;'>Résultats de l'Analyse Descriptive</h1>", unsafe_allow_html=True)
    
    conn = sqlite3.connect('patient_plus_final_db.db')
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df, names='attitude_g', title="Satisfaction Accueil"), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x='hopital', y='attente', title="Attente par Établissement"), use_container_width=True)
    
    if st.button("🏠 RETOUR À L'ACCUEIL"):
        st.session_state.page = "Home"
        st.rerun()
