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

# --- DESIGN CSS (BASÉ SUR VOTRE PALETTE DE COULEURS) ---
st.markdown(f"""
    <style>
    /* Masquage menu latéral */
    [data-testid="stSidebar"], header {{ display: none !important; }}
    
    /* Variables de couleurs de votre image */
    :root {{
        --gray: #d0ced0;
        --sky-blue: #819ee5;
        --medium-blue: #5774ba;
        --deep-blue: #39559e;
        --accent-red: #e1395f;
    }}

    /* Fond d'écran Accueil (Image 3) */
    .stApp {{
        background: linear-gradient(rgba(57, 85, 158, 0.8), rgba(57, 85, 158, 0.8)), 
                    url('https://leconomiste.cm/wp-content/uploads/2022/08/Hôpital-général-de-Yaoundé.jpg');
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Bulles d'informations avec images en fond */
    .bubble-container {{
        display: flex; gap: 25px; justify-content: center; flex-wrap: wrap; margin-top: 40px;
    }}
    .bubble {{
        width: 45%; min-width: 320px; height: 350px; border-radius: 30px;
        padding: 30px; color: white; box-shadow: 0 15px 30px rgba(0,0,0,0.4);
        display: flex; flex-direction: column; justify-content: flex-end;
        border: 2px solid var(--gray);
    }}
    .bubble-1 {{
        background: linear-gradient(to top, var(--deep-blue), rgba(0,0,0,0.1)), 
                    url('https://www.stopblablacam.com/images/k2/items/cache/f7f7b1f1b9f7a7d9a1f1b9f7a7d9a1f1_XL.jpg');
        background-size: cover;
    }}
    .bubble-2 {{
        background: linear-gradient(to top, var(--deep-blue), rgba(0,0,0,0.1)), 
                    url('https://static.atlantico.fr/sites/default/files/styles/image_744x422/public/images/2013/05/bebe_couveuse.jpg');
        background-size: cover;
    }}

    /* Style du texte */
    .hero-text {{
        text-align: center; font-size: 28px; font-weight: bold; color: white;
        margin: 40px auto; max-width: 900px; line-height: 1.4;
    }}

    /* Bouton Rouge Patient Plus */
    div.stButton > button {{
        background-color: var(--accent-red) !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 18px 50px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(225, 57, 95, 0.4) !important;
    }}

    /* Formulaire Blanc Propre */
    .form-box {{
        background: white; padding: 40px; border-radius: 25px; color: #333;
        max-width: 950px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }}
    label {{ color: var(--deep-blue) !important; font-weight: bold !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('patient_plus_final.db', check_same_thread=False)
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
def nav_to(page_name):
    st.session_state.page = page_name

# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:65px; color:white;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    
    st.markdown("""<div class='hero-text'>
        Cette application a pour but d'améliorer la qualité du traitement de service dans nos services d'urgence et hospitaliers du pays.
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="bubble-container">
            <div class="bubble bubble-1">
                <h3>🇨🇲 Indicateurs Hospitaliers</h3>
                <p><b>Performance :</b> Seuls 48% des 172 hôpitaux publics remplissent les critères de bonne performance.<br>
                <b>Surcharge :</b> Les hôpitaux régionaux enregistrent entre 4 000 et 6 000 hospitalisations annuelles.</p>
            </div>
            <div class="bubble bubble-2">
                <h3>👶 Maternité et Naissance</h3>
                <p><b>Alerte :</b> 35,9% des accouchements se font encore sans assistance médicale.<br>
                L'audit de ces services est une priorité nationale pour la sécurité des nouveau-nés.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; margin-top:50px;'>", unsafe_allow_html=True)
    if st.button("🚀 DÉMARRER L'AUDIT"):
        nav_to("Formulaire")
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 2 : FORMULAIRE ---
elif st.session_state.page == "Formulaire":
    st.markdown("<div style='text-align:center;'><h1 style='color:white;'>Audit de Qualité</h1></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='form-box'>", unsafe_allow_html=True)
    with st.form("audit_form", clear_on_submit=True):
        st.subheader("I. Informations Personnelles")
        c1, c2 = st.columns(2)
        nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
        age, sexe = c1.number_input("Âge", 0, 110, 30), c2.selectbox("Sexe", ["Masculin", "Féminin"])
        metier, dob = c1.text_input("Métier"), c2.date_input("Date de naissance")
        domicile, email = c1.text_input("Lieu de résidence"), c2.text_input("Email")

        st.subheader("II. Détails du Séjour")
        hopital = st.selectbox("Hôpital visité", ["Hôpital Général", "Hôpital Central", "Laquintinie", "Hôpital de District"])
        service, maladie = st.text_input("Service (ex: Urgences)"), st.text_input("Maladie / Motif")

        st.subheader("III. Évaluation")
        attente = st.slider("Attente (min)", 0, 300, 45)
        attitude = st.selectbox("Attitude globale", ["Insuffisante", "Moyenne", "Satisfaisante", "Excellente"])
        
        ci, cm = st.columns(2)
        e_inf, j_inf = ci.select_slider("Note Infirmières", options=["1","2","3","4","5"]), ci.text_area("Justif. Infirmières")
        e_med, j_med = cm.select_slider("Note Médecins", options=["1","2","3","4","5"]), cm.text_area("Justif. Médecins")

        st.subheader("IV. Suggestions")
        rdv = st.radio("Favorable aux RDV en ligne ?", ["Oui", "Non"])
        sug = st.text_area("Vos recommandations pour améliorer le service")

        if st.form_submit_button("VALIDER L'AUDIT"):
            conn = sqlite3.connect('patient_plus_final.db')
            c = conn.cursor()
            c.execute("INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, domicile, email, maladie, service, hopital, attente, attitude_g, eval_inf, justif_inf, eval_med, justif_med, rdv_ligne, suggestions) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                      (nom, prenom, age, sexe, metier, str(dob), domicile, email, maladie, service, hopital, attente, attitude, e_inf, j_inf, e_med, j_med, rdv, sug))
            conn.commit()
            conn.close()
            st.success("✅ Audit enregistré !")
            nav_to("Succès")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 3 : SUCCÈS & ACCÈS ANALYSE ---
elif st.session_state.page == "Succès":
    st.markdown("<div class='form-box' style='text-align:center;'>", unsafe_allow_html=True)
    st.header("Merci pour votre contribution !")
    st.write("Vos données ont été intégrées à l'analyse quantitative nationale.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📊 VOIR LES DIAGRAMMES D'ANALYSE"):
        nav_to("Analyse")
        st.rerun()
    
    if st.button("⬅ Retourner à l'accueil"):
        nav_to("Accueil")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- PAGE 4 : ANALYSE (DIAGRAMMES) ---
elif st.session_state.page == "Analyse":
    st.markdown("<h1 style='color:white; text-align:center;'>Diagrammes d'Analyse Descriptive</h1>", unsafe_allow_html=True)
    
    conn = sqlite3.connect('patient_plus_final.db')
    df = pd.read_sql_query("SELECT * FROM rapports", conn)
    conn.close()

    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df, names='attitude_g', title="Attitude Globale du Personnel", color_discrete_sequence=['#5774ba', '#e1395f', '#819ee5']), use_container_width=True)
        with c2:
            st.plotly_chart(px.bar(df, x='hopital', y='attente', color='hopital', title="Temps d'attente par Hôpital"), use_container_width=True)
        
        st.plotly_chart(px.histogram(df, x='eval_med', title="Distribution des notes Médecins"), use_container_width=True)
    
    if st.button("🏠 Retour à l'accueil"):
        nav_to("Accueil")
        st.rerun()
