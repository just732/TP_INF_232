import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Patient Plus - Audit National Cameroun", layout="wide")

# --- DONNÉES NATIONALES (Régions et Hôpitaux) ---
data_cameroun = {
    "Adamaoua": ["Hôpital Régional de Ngaoundéré", "Hôpital de District de Tibati", "Hôpital de District de Tignère"],
    "Centre": ["Hôpital Général de Yaoundé", "Hôpital Central de Yaoundé", "CHU de Yaoundé", "Hôpital Gynéco-Obstétrique", "Hôpital de District de Biyem-Assi"],
    "Est": ["Hôpital Régional de Bertoua", "Hôpital de District de Batouri", "Hôpital de District de Abong-Mbang"],
    "Extrême-Nord": ["Hôpital Régional de Maroua", "Hôpital de District de Kousseri", "Hôpital de District de Mokolo"],
    "Littoral": ["Hôpital Général de Douala", "Hôpital Laquintinie", "Hôpital Gynéco-Obstétrique de Douala", "Hôpital de District de Bonassama"],
    "Nord": ["Hôpital Régional de Garoua", "Hôpital de District de Guider", "Hôpital de District de Poli"],
    "Nord-Ouest": ["Hôpital Régional de Bamenda", "Hôpital de District de Wum", "Hôpital de District de Kumbo"],
    "Ouest": ["Hôpital Régional de Bafoussam", "Hôpital de District de Dschang", "Hôpital de District de Foumban"],
    "Sud": ["Hôpital Régional d'Ebolowa", "Hôpital de District de Kribi", "Hôpital de District de Sangmélima"],
    "Sud-Ouest": ["Hôpital Régional de Buea", "Hôpital Régional de Limbe", "Hôpital de District de Kumba"]
}

# --- DESIGN "PATIENT PLUS" ---
st.markdown("""
    <style>
    /* FOND D'ÉCRAN : Hôpital Général (Image 3) */
    .stApp {
        background: linear-gradient(rgba(0, 43, 92, 0.8), rgba(0, 43, 92, 0.8)), 
                    url('https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg');
        background-size: cover; background-attachment: fixed; color: white;
    }

    /* BULLES D'INFO AVEC IMAGES DE FOND */
    .bubble-pediatrie {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
                    url('https://www.social-sante.gouv.fr/IMG/jpg/pediatrie_hopital.jpg');
        background-size: cover; padding: 25px; border-radius: 20px; color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #e1395f; min-height: 300px;
    }
    .bubble-maternite {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
                    url('https://www.unicef.org/cameroon/sites/unicef.org.cameroon/files/styles/hero_desktop/public/UNI354546.jpg');
        background-size: cover; padding: 25px; border-radius: 20px; color: #1a1a1a; margin-bottom: 20px; border-left: 8px solid #39559e; min-height: 300px;
    }

    /* Style des boutons rouges */
    .stButton>button {
        background-color: #e1395f !important; color: white !important;
        border-radius: 50px !important; padding: 15px !important; width: 100%; font-weight: bold !important; border: none !important;
    }
    
    /* Conteneur Admin blanc */
    .admin-container { background-color: white; padding: 30px; border-radius: 20px; color: #1a1a1a; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES ---
def get_connection():
    return sqlite3.connect('audit_national_cameroon.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rapports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT, prenom TEXT, age INTEGER, sexe TEXT, metier TEXT, dob TEXT, 
                    region TEXT, domicile TEXT, email TEXT,
                    maladie TEXT, service TEXT, hopital TEXT, experience TEXT, attente INTEGER, 
                    eval_inf TEXT, justif_inf TEXT, eval_med TEXT, justif_med TEXT,
                    rdv_ligne TEXT, suggestions TEXT, date_soumission DATETIME)''')
    conn.commit()
    conn.close()

init_db()

# --- NAVIGATION ---
st.sidebar.title("🇨🇲 Patient Plus")
role = st.sidebar.radio("Accès :", ["Espace Patient", "Espace Administrateur"])

# --- ESPACE PATIENT ---
if role == "Espace Patient":
    menu = st.sidebar.selectbox("Section :", ["Accueil", "Remplir l'Audit"])

    if menu == "Accueil":
        st.markdown("<h1 style='text-align:center;'>PATIENT PLUS CAMEROUN</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:22px;'>Audit national pour l'amélioration de la qualité des services d'urgence et hospitaliers sur l'ensemble du territoire.</p>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="bubble-pediatrie">
                <h4>Hôpitaux et Surcharge</h4>
                <p><b>Hôpitaux Régionaux :</b> 4 000 à 6 000 hospitalisations/an. Surcharge critique.</p>
                <p><b>Performance :</b> Sur 172 hôpitaux publics au Cameroun, seuls 48% sont jugés performants.</p>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="bubble-maternite">
                <h4>Maternité et Accouchements</h4>
                <p><b>Statistiques :</b> 35,9% des accouchements se font encore à domicile sans assistance médicale.</p>
                <p>L'audit aide à comprendre pourquoi les maternités institutionnelles sont évitées.</p>
            </div>""", unsafe_allow_html=True)

    elif menu == "Remplir l'Audit":
        st.markdown("<h2>📝 Formulaire d'Audit National</h2>", unsafe_allow_html=True)
        with st.form("audit_form"):
            st.subheader("1. Identification")
            c1, c2 = st.columns(2)
            nom, prenom = c1.text_input("Nom"), c2.text_input("Prénom")
            age, sexe = c1.number_input("Âge", 0, 110, 25), c2.selectbox("Sexe", ["Masculin", "Féminin"])
            metier, email = c1.text_input("Métier"), c2.text_input("Email")
            dob = c1.date_input("Date de naissance")
            
            st.subheader("2. Localisation et Établissement")
            # --- LOGIQUE DE RÉGION ET HÔPITAL ---
            region_selected = st.selectbox("Dans quelle RÉGION vous trouvez-vous ?", list(data_cameroun.keys()))
            hopital_selected = st.selectbox("Sélectionnez l'HÔPITAL concerné :", data_cameroun[region_selected])
            domicile = st.text_input("Quartier de résidence")
            
            st.subheader("3. Motif et Évaluation")
            service, maladie = st.text_input("Service visité"), st.text_input("Maladie/Motif")
            attente = st.slider("Temps d'attente (min)", 0, 300, 30)
            
            col_inf, col_med = st.columns(2)
            e_inf = col_inf.select_slider("Note Infirmières", options=["1", "2", "3", "4", "5"])
            j_inf = col_inf.text_area("Justification Infirmières")
            e_med = col_med.select_slider("Note Médecins", options=["1", "2", "3", "4", "5"])
            j_med = col_med.text_area("Justification Médecins")

            st.subheader("4. Recommandations")
            sug = st.text_area("Comment améliorer le service dans cet établissement ?")
            rdv = st.radio("Favorable au RDV en ligne avec un médecin spécifique ?", ["Oui", "Non"])

            if st.form_submit_button("TRANSMETTRE L'AUDIT"):
                conn = get_connection()
                c = conn.cursor()
                c.execute('''INSERT INTO rapports (nom, prenom, age, sexe, metier, dob, region, domicile, email,
                            maladie, service, hopital, attente, eval_inf, justif_inf, eval_med, justif_med,
                            rdv_ligne, suggestions, date_soumission) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', 
                         (nom, prenom, age, sexe, metier, str(dob), region_selected, domicile, email, maladie, service, hopital_selected, attente, e_inf, j_inf, e_med, j_med, rdv, sug, datetime.now()))
                conn.commit()
                conn.close()
                st.success(f"✅ Merci ! Votre audit sur {hopital_selected} ({region_selected}) a été enregistré.")

# --- ESPACE ADMINISTRATEUR (ENQUÊTEUR) ---
elif role == "Espace Administrateur":
    st.markdown("<h2>🔐 Tableau de Bord de l'Enquêteur</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Mot de passe :", type="password")
    
    if pwd == "admin123":
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM rapports", conn)
        conn.close()

        if df.empty:
            st.info("En attente des premières soumissions...")
        else:
            st.markdown("<div class='admin-container'>", unsafe_allow_html=True)
            # Métriques Nationales
            m1, m2, m3 = st.columns(3)
            m1.metric("Total National d'Audits", len(df))
            m2.metric("Moyenne d'Attente (min)", round(df['attente'].mean(), 1))
            fav_perc = (len(df[df['rdv_ligne'] == "Oui"]) / len(df)) * 100
            m3.metric("Favorable RDV en ligne", f"{round(fav_perc, 1)}%")

            # Graphiques
            st.subheader("Analyse par Région")
            fig_reg = px.bar(df.groupby('region').size().reset_index(name='Nombre'), x='region', y='Nombre', title="Nombre d'audits par région")
            st.plotly_chart(fig_reg, use_container_width=True)

            st.subheader("Détails par Hôpital")
            fig_hosp = px.box(df, x="hopital", y="attente", color="region", title="Dispersion du temps d'attente par hôpital")
            st.plotly_chart(fig_hosp, use_container_width=True)
            
            st.subheader("Recommandations des Patients")
            st.dataframe(df[['region', 'hopital', 'suggestions', 'date_soumission']])
            st.markdown("</div>", unsafe_allow_html=True)
