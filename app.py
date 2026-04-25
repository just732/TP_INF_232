import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National", layout="wide")

# --- INITIALISATION NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# --- APPLICATION DU DESIGN (CSS) ---
def apply_theme():
    if st.session_state.page == "Home":
        # THEME ACCUEIL : PATIENT PLUS (Sombre / Bleu Profond)
        st.markdown("""
            <style>
            [data-testid="stSidebar"], header { display: none !important; }
            
            /* Fond d'écran global */
            .stApp {
                background: linear-gradient(135deg, #39559e 0%, #5774ba 100%);
                color: white;
            }

            /* Bannière Hero */
            .hero-container {
                padding: 60px;
                text-align: center;
                background: linear-gradient(rgba(57, 85, 158, 0.8), rgba(57, 85, 158, 0.8)), 
                            url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
                background-size: cover;
                border-radius: 40px;
                margin-bottom: 40px;
                box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            }
            .hero-title { font-size: 65px !important; font-weight: 800; color: white; margin-bottom:10px; }
            .hero-subtitle { font-size: 24px; color: #d0ced0; }

            /* Bulles d'info style "Patient Plus" */
            .bubble-card {
                background-color: white;
                border-radius: 30px;
                height: 400px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                padding: 30px;
                box-shadow: 0 12px 24px rgba(0,0,0,0.2);
                border: 2px solid #819ee5;
                margin-bottom: 20px;
                color: #333;
            }
            
            /* Images de fond pour les bulles */
            .img-pediatrie {
                background: linear-gradient(to top, white 20%, transparent), 
                            url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg');
                background-size: cover;
            }
            .img-maternite {
                background: linear-gradient(to top, white 20%, transparent), 
                            url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg');
                background-size: cover;
            }

            /* Bouton d'action Rouge (exactement comme sur l'image) */
            div.stButton > button {
                background-color: #e1395f !important;
                color: white !important;
                border-radius: 50px !important;
                padding: 20px 60px !important;
                font-size: 22px !important;
                font-weight: bold !important;
                border: none !important;
                box-shadow: 0 8px 20px rgba(225, 57, 95, 0.4) !important;
                text-transform: uppercase;
                margin-top: 30px;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        # THEME FORMULAIRE : GOOGLE FORM (Clair / Reposant)
        st.markdown("""
            <style>
            [data-testid="stSidebar"], header { display: none !important; }
            .stApp { background-color: #f0f2f6; color: #202124; }
            .form-box {
                background-color: white;
                border-radius: 12px;
                padding: 45px;
                max-width: 900px;
                margin: 30px auto;
                border-top: 12px solid #39559e;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            label { color: #39559e !important; font-weight: bold !important; font-size: 16px !important; }
            input, textarea, select { background-color: #f8f9fa !important; border-radius: 8px !important; color: black !important; }
            
            /* Bouton validation en bleu profond */
            div.stButton > button {
                background-color: #39559e !important;
                color: white !important;
                border-radius: 8px !important;
                padding: 12px 30px !important;
                border: none !important;
            }
            </style>
        """, unsafe_allow_html=True)

apply_theme()

# --- LOGIQUE BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('patient_plus_v8.db', check_same_thread=False)
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
        <div class="hero-container">
            <h1 class="hero-title">PATIENT PLUS</h1>
            <p class="hero-subtitle">Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
            <div class="bubble-card img-pediatrie">
                <h3 style="color:#39559e;">📊 Performance Hospitalière</h3>
                <p><b>Statistiques CMR :</b> Sur 172 hôpitaux publics, seuls 48% sont jugés performants.<br>
                Surcharge critique : 4 000 à 6 000 hospitalisations par an dans les services régionaux.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="bubble-card img-maternite">
                <h3 style="color:#39559e;">👶 Services Maternité</h3>
                <p><b>Urgence Sanitaire :</b> 35,9% des accouchements se font encore à domicile sans assistance médicale.<br>
                L'audit aide à cibler les réformes pour la sécurité des naissances.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("🚀 DÉMARRER L'AUDIT"):
        st.session_state.page = "Form"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif st.session_state.page == "Form":
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#39559e; text-align:center;'>Questionnaire de Satisfaction Patient</h2>", unsafe_allow_html=True)
    
    with st.form("google_form", clear_on_submit=True):
        st.subheader("1. Identification")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        age, sexe = c1.number_input("Âge", 0, 110, 25), c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier, dob = c1.text_input("Métier"), c2.date_input("Date de naissance")
        dom, mail = c1.text_input("Lieu de résidence"), c2.text_input("Email")

        st.subheader("2. Contexte du Séjour")
        hop = st.selectbox("Établissement fréquenté", ["Hôpital Général", "Hôpital Central", "Laquintinie", "Hôpital de District"])
        serv = st.text_input("Service visité (ex: Urgences)")
        mal = st.text_input("Motif de la visite / Maladie")
        
        st.subheader("3. Audit Qualité")
        att = st.slider("Temps d'attente aux urgences (min)", 0, 300, 30)
        att_g = st.selectbox("Attitude globale du personnel", ["Médiocre", "Passable", "Satisfaisante", "Excellente"])
        
        ci, cm = st.columns(2)
        e_i = ci.select_slider("Note Infirmières", options=["1","2","3","4","5"])
        j_i = ci.text_area("Justification (Infirmières)")
        e_m = cm.select_slider("Note Médecins", options=["1","2","3","4","5"])
        j_m = cm.text_area("Justification (Médecins)")

        st.subheader("4. Recommandations")
        rdv = st.radio("Souhaitez-vous des RDV en ligne avec un médecin spécifique ?", ["Oui", "Non"])
        sug = st.text_area("Comment faire pour améliorer la qualité du service ?")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = sqlite3.connect('patient_plus_v8.db')
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
    st.markdown("<h1 style='text-align:center; color:#39559e;'>Résultats de l'Analyse Descriptive</h1>", unsafe_allow_html=True)
    
    conn = sqlite3.connect('patient_plus_v8.db')
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df, names='attitude_g', title="Satisfaction Globale Accueil", color_discrete_sequence=['#5774ba', '#e1395f', '#819ee5']), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x='hopital', y='attente', title="Temps d'attente par Hôpital", color_discrete_sequence=['#39559e']), use_container_width=True)
    
    if st.button("🏠 RETOUR À L'ACCUEIL"):
        st.session_state.page = "Home"
        st.rerun()
