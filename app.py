# --- PAGE 1 : ACCUEIL ---
if st.session_state.page == "Accueil":
    st.markdown("<h1 style='text-align:center; font-size:60px; margin-bottom:0;'>PATIENT PLUS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px; opacity:0.9;'>Système National de Suivi des Urgences et de la Performance Hospitalière</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Titre de navigation style image
    st.markdown("<div style='text-align:center; font-weight:bold; letter-spacing:2px; border-bottom:1px solid rgba(255,255,255,0.2); padding-bottom:10px; margin-bottom:30px;'>NAVIGUER DANS L'APPLICATION</div>", unsafe_allow_html=True)

    # Conteneur des 3 colonnes
    col1, col2, col3 = st.columns(3)

    # Style CSS spécifique pour superposer le bouton invisible sur la carte HTML
    st.markdown("""
        <style>
        .stButton button {
            width: 100%;
            height: 220px; /* Même hauteur que la carte */
            background-color: transparent !important;
            color: transparent !important;
            border: none !important;
            position: absolute;
            z-index: 10;
        }
        .nav-card {
            background-color: #122a45; /* Bleu marine profond */
            border: 2px solid white;
            border-radius: 15px;
            padding: 30px 10px;
            text-align: center;
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: transform 0.2s, background-color 0.2s;
        }
        .nav-card:hover {
            background-color: #1c3d63;
            transform: scale(1.02);
        }
        .card-icon { font-size: 40px; margin-bottom: 10px; }
        .card-title { font-size: 24px; font-weight: bold; color: white; text-transform: uppercase; }
        .card-subtitle { font-size: 14px; color: #cbd5e0; margin-top: 10px; }
        </style>
    """, unsafe_allow_html=True)

    with col1:
        st.button("clic_audit", key="b1", on_click=lambda: changer_page("Audit"))
        st.markdown("""
            <div class="nav-card">
                <div class="card-icon">📝</div>
                <div class="card-title">AUDIT</div>
                <div class="card-subtitle">Participer à l'enquête</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.button("clic_admin", key="b2", on_click=lambda: changer_page("Admin"))
        st.markdown("""
            <div class="nav-card">
                <div class="card-icon">🔐</div>
                <div class="card-title">ADMIN</div>
                <div class="card-subtitle">Espace Enquêteur</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.button("clic_infos", key="b3", on_click=lambda: changer_page("Infos"))
        st.markdown("""
            <div class="nav-card">
                <div class="card-icon">ℹ️</div>
                <div class="card-title">INFOS</div>
                <div class="card-subtitle">À propos du projet</div>
            </div>
        """, unsafe_allow_html=True)
