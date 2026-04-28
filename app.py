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

# --- STYLE CSS (BLEU NUIT & DESIGN WEB EN BULLES) ---
st.markdown("""
    <style>
    /* Global - Midnight Blue */
    .stApp {
        background-color: #001122;
        color: #e0e0e0;
    }
    
    /* Navigation */
    .nav-bar {
        background-color: #001a33;
        padding: 10px 5%;
        border-bottom: 2px solid #00d4ff;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Bulles / Cartes d'information */
    .info-bubble {
        background: rgba(0, 212, 255, 0.08);
        border: 1px solid #00d4ff;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        transition: 0.3s;
        height: 100%;
    }
    .info-bubble:hover {
        background: rgba(0, 212, 255, 0.15);
        transform: translateY(-5px);
    }
    
    h1, h2, h3, h4 { color: #00d4ff !important; font-weight: bold !important; }
    
    .stButton>button {
        background-color: #00d4ff !important; color: #001122 !important;
        font-weight: bold !important; border-radius: 25px !important;
        border: none !important; width: 100% !important;
    }

    input, textarea, .stSelectbox, .stDateInput { 
        background-color: white !important; 
        color: black !important; 
        border-radius: 10px !important; 
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = "Accueil"
if 'user_connecte' not in st.session_state: st.session_state.user_connecte = None

def naviguer(nom_page):
    st.session_state.page = nom_page

# --- BARRE DE NAVIGATION (FONCTIONNELLE) ---
cols = st.columns([2, 1, 1, 1, 1])
with cols[0]: st.markdown("<h2 style='margin:0;'>PATIENT <span style='color:white;'>PLUS</span></h2>", unsafe_allow_html=True)
if cols[1].button("ACCUEIL"): naviguer("Accueil")
if cols[2].button("SERVICES"): naviguer("Services")
if cols[3].button("STATS"): naviguer("Stats")
if st.session_state.user_connecte:
    if cols[4].button("DÉCONNEXION"): st.session_state.user_connecte = None; naviguer("Accueil")
else:
    if cols[4].button("S'IDENTIFIER"): naviguer("Auth")

# ==========================================
# PAGE D'ACCUEIL : DESIGN SITE WEB (BULLES)
# ==========================================
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center;'>Votre expérience est la clé d'une santé d'excellence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>Rejoignez la plateforme Patient Plus et aidez-nous à transformer nos hôpitaux avec confiance et sécurité.</p>", unsafe_allow_html=True)
    
    # --- RANGÉE DE BULLES 1 : LE BUT ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class="info-bubble">
            <h3>🛡️ But de la Plateforme</h3>
            <p><b>Patient Plus</b> est une initiative nationale pour collecter des données réelles sur la qualité de service hospitalier. 
            En partageant votre parcours, vous permettez aux autorités d'identifier précisément où agir (délais, hygiène, accueil).</p>
            <p><i>"Votre voix n'est plus perdue, elle devient un outil de gestion."</i></p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="info-bubble">
            <h3>📈 Statistiques & Performance</h3>
            <ul>
                <li><b>48% :</b> Score moyen d'efficience des hôpitaux publics.</li>
                <li><b>94% :</b> Part des frais de santé supportée directement par les familles.</li>
                <li><b>Objectif :</b> Réduire les coûts et améliorer la prise en charge maternelle.</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    # --- RANGÉE DE BULLES 2 : TOPOGRAPHIE DES HÔPITAUX ---
    st.markdown("<h2>Nos établissements de référence</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="info-bubble"><h4>HGY / HGD</h4><p>Hôpitaux Généraux (Yaoundé/Douala). Référence en oncologie, chirurgie et dialyse.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="info-bubble"><h4>Laquintinie / HCY</h4><p>Hôpitaux Centraux. Centres névralgiques pour les urgences traumatiques et la proximité.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="info-bubble"><h4>HGOPY / D</h4><p>Hôpitaux Gynéco-Obstétriques. Priorité absolue à la santé de la mère et de l\'enfant.</p></div>', unsafe_allow_html=True)

    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6a/H%C3%B4pital_G%C3%A9n%C3%A9ral_de_Yaound%C3%A9.jpg", use_column_width=True)
    
    st.markdown("<center>", unsafe_allow_html=True)
    if not st.session_state.user_connecte:
        if st.button("✨ CRÉER MON COMPTE ET CONTRIBUER MAINTENANT"): naviguer("Auth")
    st.markdown("</center>", unsafe_allow_html=True)

# ==========================================
# PAGE STATISTIQUES (DIAGRAMMES)
# ==========================================
elif st.session_state.page == "Stats":
    st.title("📊 Baromètre National de la Qualité")
    conn = sqlite3.connect('patient_plus_final.db'); df = pd.read_sql_query("SELECT * FROM formulaires", conn); conn.close()
    if df.empty: st.info("Les données s'afficheront après les premiers formulaires.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(df.groupby('hopital')['note'].mean().reset_index(), x='hopital', y='note', title="Note de satisfaction / 5", template="plotly_dark", color_discrete_sequence=['#00d4ff'])
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.pie(df, names='service', title="Répartition par Pôle Médical", hole=0.4, template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)

# ==========================================
# AUTHENTIFICATION
# ==========================================
elif st.session_state.page == "Auth":
    st.title("🔐 Espace Sécurisé")
    choix = st.radio("Action :", ["Se connecter", "Créer un compte"])
    u = st.text_input("Identifiant (Email/Téléphone)")
    p = st.text_input("Mot de passe", type="password")
    if st.button("VALIDER"):
        if choix == "Créer un compte":
            nom = st.text_input("Nom"); prenom = st.text_input("Prénom")
            conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
            try: c.execute('INSERT INTO utilisateurs VALUES (?,?,?,?)', (u, hasher_mdp(p), u, "")); conn.commit(); st.success("Compte créé avec succès !")
            except: st.error("Erreur : Identifiant déjà utilisé.")
            conn.close()
        else:
            conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
            c.execute('SELECT * FROM utilisateurs WHERE username=? AND password=?', (u, hasher_mdp(p)))
            if c.fetchone(): st.session_state.user_connecte = u; naviguer("Formulaire"); st.rerun()
            else: st.error("Identifiants incorrects.")
            conn.close()

# ==========================================
# PAGE FORMULAIRE : INTERACTIF ET DYNAMIQUE
# ==========================================
elif st.session_state.page == "Formulaire":
    if not st.session_state.user_connecte: naviguer("Auth"); st.rerun()

    st.title("📝 Remplir mon formulaire de satisfaction")
    
    # 1. Identification
    st.subheader("1. Identification")
    c_id1, c_id2 = st.columns(2)
    nom_f = c_id1.text_input("Nom")
    prenom_f = c_id2.text_input("Prénom")
    
    # CALENDRIER 1915 À 2026
    dob_f = c_id1.date_input("Date de naissance", 
                               min_value=datetime(1915, 1, 1), 
                               max_value=datetime(2026, 12, 31),
                               value=datetime(1995, 1, 1))
    contact_f = c_id2.text_input("Numéro de téléphone / Email")

    # 2. Localisation
    st.subheader("2. Détails de la visite")
    hopital_saisi = st.text_input("Saisissez le nom complet de l'hôpital consulté")
    
    # IMPORTANT : Le sélecteur de service est HORS du formulaire pour l'interactivité
    service_f = st.selectbox("Sélectionnez le service que vous avez fréquenté", 
                            ["Services d'Urgence et Diagnostic", 
                             "Services de Médecine", 
                             "Chirurgie et Soins Intensifs", 
                             "Services Supports et Techniques"])

    st.divider()

    # 3. Questionnaire dynamique (Dans le Formulaire pour la validation)
    with st.form("audit_form_content"):
        st.subheader(f"📊 Questions spécifiques : {service_f}")
        
        if service_f == "Services d'Urgence et Diagnostic":
            st.radio("Triage : Le temps d'attente avant le premier examen infirmier était-il inférieur à 15 min ?", ["Oui", "Non", "Ne sais pas"])
            st.radio("Technique : Les équipements d'imagerie (Radio/Scanner) étaient-ils fonctionnels ?", ["Oui", "Non", "En panne"])
            st.radio("Communication : Avez-vous été informé du délai estimé avant la prise en charge médicale ?", ["Oui", "Non"])
            st.radio("Sécurité : Votre identité a-t-elle été vérifiée avant tout prélèvement ?", ["Oui", "Non"])
            st.radio("Orientation : Votre transfert vers un service ou la sortie a-t-il été fluide ?", ["Oui", "Non"])

        elif service_f == "Services de Médecine":
            st.radio("Douleur : Votre douleur était-elle réévaluée après chaque administration de traitement ?", ["Oui", "Non", "Parfois"])
            st.radio("Information : Le médecin a-t-il expliqué le diagnostic de façon compréhensible ?", ["Très clair", "Partiellement", "Pas du tout"])
            st.radio("Hygiène : Le personnel a-t-il désinfecté ses mains avant et après vous avoir touché ?", ["Toujours", "Souvent", "Jamais remarqué"])
            st.radio("Alimentation : La qualité et la température des repas étaient-elles satisfaisantes ?", ["Satisfaisant", "Passable", "Médiocre"])
            st.radio("Dossier : Vos constantes (tension, température) étaient-elles relevées 3 fois par jour ?", ["Oui", "Non", "Ne sais pas"])

        elif service_f == "Chirurgie et Soins Intensifs":
            st.radio("Check-list : La check-list 'Sécurité du patient' a-t-elle été remplie pour l'intervention ?", ["Oui", "Non", "Ne sais pas"])
            st.radio("Consentement : Le formulaire de consentement éclairé était-il signé avant l'anesthésie ?", ["Oui", "Non"])
            st.radio("Surveillance : Le nombre d'infirmiers permettait-il une surveillance constante ?", ["Oui", "Non", "Moyen"])
            st.radio("Stérilisation : La traçabilité de la stérilisation a-t-elle été vérifiée avant l'ouverture des boîtes ?", ["Oui", "Non"])
            st.radio("Infections : Existe-t-il un suivi des infections après l'intervention ?", ["Oui", "Non", "Je ne sais pas"])

        elif service_f == "Services Supports et Techniques":
            st.radio("Pharmacie : La disponibilité des médicaments essentiels était-elle supérieure à 90% ?", ["Oui", "Non, ruptures"])
            st.radio("Maintenance : Les groupes électrogènes et réserves d'eau sont-ils fonctionnels ?", ["Oui", "Non", "Ne sais pas"])
            st.markdown("Propreté : Les sanitaires étaient-ils nettoyés au moins deux fois par jour ?")
            st.radio("Réponse :", ["Propre", "Passable", "Sale"], key="clean")
            st.radio("Facturation : La facture était-elle détaillée et expliquée de manière transparente ?", ["Oui", "Non", "Partiellement"])
            st.radio("Confidentialité : Le personnel garantit-il la discrétion de vos données à l'admission ?", ["Oui", "Non"])

        st.divider()
        note_f = st.select_slider("Note globale de satisfaction pour cette visite (1 à 5)", options=[1, 2, 3, 4, 5])
        avis_f = st.text_area("Des suggestions pour cet hôpital ?")

        if st.form_submit_button("VALIDER ET ENVOYER LE FORMULAIRE"):
            if not hopital_saisi:
                st.error("Veuillez saisir le nom de l'établissement.")
            else:
                conn = sqlite3.connect('patient_plus_final.db'); c = conn.cursor()
                c.execute('INSERT INTO formulaires (user, hopital, service, note, date) VALUES (?,?,?,?,?)', 
                          (st.session_state.user_connecte, hopital_saisi, service_f, note_f, datetime.now().strftime("%Y-%m-%d")))
                conn.commit(); conn.close()
                st.success("Formulaire transmis avec succès ! Merci pour votre contribution.")
                st.balloons()
                naviguer("Stats"); st.rerun()
