import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime
import hashlib

# --- CONFIGURATION ---
st.set_page_config(page_title="Patient Plus", layout="wide", initial_sidebar_state="collapsed")

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

# --- SÉCURITÉ ---
def hasher_mdp(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# --- STYLE CSS (BLEU NUIT) ---
st.markdown("""
    <style>
    .stApp { background-color: #001122; color: #e0e0e0; }
    h1, h2, h3, h4 { color: #00d4ff !important; }
    .stButton>button {
        background-color: #00d4ff !important; color: #001122 !important;
        font-weight: bold !important; border-radius: 25px !important; width: 100% !important;
    }
    input, textarea { background-color: white !important; color: black !important; border-radius: 10px !important; }
    .question-box { background-color: rgba(0, 212, 255, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #00d4ff; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'user_connecte' not in st.session_state: st.session_state.user_connecte = None

def naviguer(nom_page):
    st.session_state.page = nom_page

# --- BARRE DE NAVIGATION ---
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
cols = st.columns([2, 1, 1, 1, 1])
with cols[0]: st.markdown("<h2 style='margin:0;'>PATIENT <span style='color:white;'>PLUS</span></h2>", unsafe_allow_html=True)
if cols[1].button("ACCUEIL"): naviguer("Accueil")
if cols[2].button("SERVICES"): naviguer("Services")
if cols[3].button("STATISTIQUES"): naviguer("Stats")
if st.session_state.user_connecte:
    if cols[4].button("DÉCONNEXION"): st.session_state.user_connecte = None; naviguer("Accueil")
else:
    if cols[4].button("S'IDENTIFIER"): naviguer("Auth")

# ==========================================
# PAGES ACCUEIL, SERVICES ET STATS (Identiques au précédent)
# ==========================================
if st.session_state.page == "Accueil":
    st.title("Qualité de service hospitalier au Cameroun")
    st.write("Plateforme de collecte de données pour l'amélioration du système de santé.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg", use_column_width=True)
    if not st.session_state.user_connecte:
        if st.button("CRÉER UN COMPTE POUR REMPLIR UN FORMULAIRE"): naviguer("Auth")

elif st.session_state.page == "Services":
    st.title("Nos Domaines d'Évaluation")
    st.write("Nous évaluons 4 blocs majeurs pour garantir votre sécurité.")

elif st.session_state.page == "Stats":
    st.title("📊 Statistiques Nationales")
    conn = sqlite3.connect('patient_plus_final.db')
    df = pd.read_sql_query("SELECT * FROM formulaires", conn)
    conn.close()
    if df.empty: st.info("Aucune donnée disponible.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(df.groupby('hopital')['note'].mean().reset_index(), x='hopital', y='note', title="Moyenne de satisfaction", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            fig2 = px.pie(df, names='service', title="Répartition par Pôle", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

elif st.session_state.page == "Auth":
    st.title("🔐 Espace Personnel")
    choix = st.radio("Action :", ["Se connecter", "Créer un compte"])
    u = st.text_input("Identifiant")
    p = st.text_input("Mot de passe", type="password")
    if st.button("VALIDER"):
        if choix == "Créer un compte":
            conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
            try: c.execute('INSERT INTO utilisateurs VALUES (?,?,?,?)', (u, hasher_mdp(p), u, "")); conn.commit(); st.success("Compte créé !")
            except: st.error("Identifiant déjà pris.")
            conn.close()
        else:
            conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
            c.execute('SELECT * FROM utilisateurs WHERE username=? AND password=?', (u, hasher_mdp(p)))
            if c.fetchone(): st.session_state.user_connecte = u; naviguer("Formulaire"); st.rerun()
            else: st.error("Erreur d'identifiants.")
            conn.close()

# ==========================================
# PAGE FORMULAIRE (DYNAMIQUE ET SPÉCIFIQUE)
# ==========================================
elif st.session_state.page == "Formulaire":
    if not st.session_state.user_connecte: naviguer("Auth"); st.rerun()

    st.title("📝 Remplir un formulaire de satisfaction")
    
    with st.form("main_form"):
        # --- ÉTAPE 1 : IDENTITÉ ---
        st.subheader("1. Informations du Patient")
        col1, col2 = st.columns(2)
        nom_f = col1.text_input("Nom")
        pre_f = col2.text_input("Prénom")
        dob_f = col1.date_input("Date de naissance", min_value=datetime(1915, 1, 1), max_value=datetime(2026, 12, 31), value=datetime(1995, 1, 1))
        
        # --- ÉTAPE 2 : HÔPITAL ---
        st.subheader("2. Établissement consulté")
        hopital_saisi = st.text_input("Saisissez le nom de l'hôpital")
        service_f = st.selectbox("Sélectionnez le pôle médical fréquenté", 
                                ["Urgences & Diagnostic", "Médecine & Chirurgie", "Pharmacie & Logistique"])

        st.divider()

        # --- ÉTAPE 3 : QUESTIONS SPÉCIFIQUES ---
        st.subheader(f"3. Questions spécifiques : {service_f}")
        
        if service_f == "Urgences & Diagnostic":
            st.markdown('<div class="question-box">Quel a été votre délai d\'attente avant le premier triage infirmier ?</div>', unsafe_allow_html=True)
            q1 = st.radio("Réponse :", ["Moins de 15 min", "15 à 30 min", "Plus de 30 min", "Plus d'une heure"], key="q1")
            
            st.markdown('<div class="question-box">Le protocole d\'accueil des urgences vitales est-il affiché et visible ?</div>', unsafe_allow_html=True)
            q2 = st.radio("Réponse :", ["Oui", "Non", "Je n'ai pas fait attention"], key="q2")
            
            st.markdown('<div class="question-box">Imagerie/Laboratoire : Le personnel a-t-il vérifié l\'étiquetage de vos prélèvements devant vous ?</div>', unsafe_allow_html=True)
            q3 = st.radio("Réponse :", ["Oui, systématiquement", "Non", "Pas pour tous les examens"], key="q3")

        elif service_f == "Médecine & Chirurgie":
            st.markdown('<div class="question-box">Sécurité : Le personnel a-t-il vérifié votre identité avant chaque administration de médicament ?</div>', unsafe_allow_html=True)
            q1 = st.radio("Réponse :", ["Oui (Règle des 5B respectée)", "Non", "Parfois"], key="q4")
            
            st.markdown('<div class="question-box">Hygiène : Avez-vous observé les soignants se désinfecter les mains avant de vous toucher ?</div>', unsafe_allow_html=True)
            q2 = st.radio("Réponse :", ["Toujours", "Souvent", "Rarement", "Jamais"], key="q5")
            
            st.markdown('<div class="question-box">Dossier : Votre dossier médical a-t-il été mis à jour à votre chevet (temps réel) ?</div>', unsafe_allow_html=True)
            q3 = st.radio("Réponse :", ["Oui", "Non", "Je ne sais pas"], key="q6")

        elif service_f == "Pharmacie & Logistique":
            st.markdown('<div class="question-box">Pharmacie : Avez-vous rencontré une rupture de stock sur les médicaments prescrits ?</div>', unsafe_allow_html=True)
            q1 = st.radio("Réponse :", ["Aucune rupture", "Certains médicaments manquants", "Rupture totale"], key="q7")
            
            st.markdown('<div class="question-box">Logistique : Le système d\'appel-malade (sonnette) dans votre chambre fonctionnait-il ?</div>', unsafe_allow_html=True)
            q2 = st.radio("Réponse :", ["Oui, parfaitement", "Non, défectueux", "Pas de système d'appel"], key="q8")

        st.divider()

        # --- ÉTAPE 4 : EXPÉRIENCE TRANSVERSALE ---
        st.subheader("4. Évaluation de l'Expérience Patient")
        
        st.markdown('<div class="question-box">Le personnel s\'est-il identifié (nom/fonction) lors de la prise en charge ?</div>', unsafe_allow_html=True)
        t1 = st.radio("Réponse :", ["Oui", "Non", "Certains seulement"], key="t1")
        
        st.markdown('<div class="question-box">Avez-vous reçu des explications claires sur votre traitement et son coût ?</div>', unsafe_allow_html=True)
        t2 = st.radio("Réponse :", ["Très claires", "Passables", "Inexistantes"], key="t2")
        
        st.markdown('<div class="question-box">Votre douleur a-t-elle été évaluée régulièrement (utilisation d\'une échelle) ?</div>', unsafe_allow_html=True)
        t3 = st.radio("Réponse :", ["Oui, très souvent", "Rarement", "Jamais"], key="t3")
        
        note_f = st.select_slider("Quelle note de satisfaction globale donnez-vous ? (1 à 5)", options=[1, 2, 3, 4, 5])

        if st.form_submit_button("ENVOYER LE FORMULAIRE FINAL"):
            if not hopital_saisi:
                st.error("Veuillez saisir le nom de l'hôpital.")
            else:
                conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
                c.execute('INSERT INTO formulaires (user, hopital, service, note, date) VALUES (?,?,?,?,?)', 
                          (st.session_state.user_connecte, hopital_saisi, service_f, note_f, datetime.now().strftime("%Y-%m-%d")))
                conn.commit(); conn.close()
                st.success("Merci ! Vos réponses ont été transmises confidentiellement.")
                st.balloons()
                naviguer("Stats"); st.rerun()
