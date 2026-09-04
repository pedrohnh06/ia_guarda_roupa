import streamlit as st
import api_client

# ══════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SmartWardrobe",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════
# CSS PREMIUM - VERSÃO CORRIGIDA
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ─── Google Fonts ─── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* ─── Reset e Base ─── */
    .stApp {
        background-color: #0A0A0A;
        color: #E8E4DF;
    }

    /* ─── Sidebar ─── */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid rgba(212, 175, 55, 0.15);
    }

    section[data-testid="stSidebar"] .stMarkdown h1 {
        font-family: 'Playfair Display', serif !important;
        color: #D4AF37 !important;
        font-weight: 600;
        letter-spacing: 2px;
        font-size: 1.6rem !important;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(212, 175, 55, 0.3);
        padding-bottom: 15px;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 400;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        color: #9A9590 !important;
        transition: color 0.3s ease;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        color: #D4AF37 !important;
    }

    /* ─── ESCONDE O BOTÃO DE COLLAPSE DA SIDEBAR (keyboard_double_arrow) ─── */
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"],
    button[kind="header"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Esconde qualquer tooltip residual da sidebar */
    section[data-testid="stSidebar"] button[title],
    .stSidebarCollapseButton {
        display: none !important;
    }

    /* ─── SIDEBAR FIXA (não redimensionável) ─── */
    section[data-testid="stSidebar"] {
        width: 280px !important;
        min-width: 280px !important;
        max-width: 280px !important;
    }
    
    section[data-testid="stSidebar"] > div {
        width: 280px !important;
    }
    
    /* Fix para o mouse mover quando deixa na linha */
    [data-testid="stSidebarResizeHandle"],
    .stSidebarResizer {
        display: none !important;
        pointer-events: none !important;
        width: 0 !important;
        cursor: default !important;
    }

    /* ─── Tipografia ─── */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #E8E4DF !important;
        font-weight: 500;
    }

    h1 { letter-spacing: 3px; text-transform: uppercase; font-size: 2rem !important; }
    h2 { letter-spacing: 2px; font-size: 1.4rem !important; color: #C4B89A !important; }
    h3 { letter-spacing: 1px; font-size: 1.1rem !important; }

    p, span, label, .stMarkdown, .stText {
        font-family: 'Inter', sans-serif !important;
        color: #B8B2A8 !important;
    }

    /* ─── Inputs ─── */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #1A1A1A !important;
        border: 1px solid #2A2A2A !important;
        color: #E8E4DF !important;
        font-family: 'Inter', sans-serif !important;
        border-radius: 4px !important;
        transition: border-color 0.3s ease;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 0 1px rgba(212, 175, 55, 0.2) !important;
    }

    /* ─── FIX: Botão de visibilidade da senha (remove palavra, adiciona olhinho) ─── */
    [data-testid="stTextInput"] button,
    [data-testid="stPasswordInputVisibilityToggle"] {
        background: transparent !important;
        border: none !important;
        padding: 4px !important;
        font-size: 0px !important; /* Esconde a palavra */
        color: transparent !important; /* Esconde a palavra */
    }

    [data-testid="stTextInput"] button:hover {
        background: transparent !important;
    }

    [data-testid="stTextInput"] button svg {
        width: 16px !important;
        height: 16px !important;
        color: #7A7570 !important;
        visibility: visible !important;
    }

    [data-testid="stTextInput"] button:hover svg {
        color: #D4AF37 !important;
    }

    /* ─── Botões - CORRIGIDO CONTRASTE E TAMANHO ─── */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.7rem !important;
        border-radius: 2px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease;
        border: 1px solid #333 !important;
        background-color: #1A1A1A !important;
        color: #E8E4DF !important;
    }

    .stButton > button:hover {
        background-color: #D4AF37 !important;
        color: #0A0A0A !important;
        border-color: #D4AF37 !important;
    }

    /* FIX: Botões primários (Entrar/Criar) - texto BRANCO em fundo dourado escuro */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"],
    .stFormSubmitButton > button {
        background-color: #8B7425 !important;
        color: #FFFFFF !important;
        border-color: #8B7425 !important;
        font-weight: 600;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover,
    .stFormSubmitButton > button:hover {
        background-color: #A68B2E !important;
        color: #FFFFFF !important;
        border-color: #A68B2E !important;
    }

    /* FIX: Diminuir fonte e padding apenas dos botões Login e Cadastro na Sidebar */
    section[data-testid="stSidebar"] .stButton > button {
        padding: 6px 4px !important;
        font-size: 0.6rem !important;
        letter-spacing: 1px !important;
    }

    /* ─── Divider ─── */
    hr {
        border-color: rgba(212, 175, 55, 0.15) !important;
    }

    /* ─── Expander ─── */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-size: 0.8rem !important;
        color: #C4B89A !important;
        background-color: #111111 !important;
        border: 1px solid #222 !important;
        border-radius: 4px !important;
    }

    /* ─── Alerts ─── */
    .stAlert { border-radius: 4px !important; }

    /* ─── Cards customizados ─── */
    .fashion-card {
        background: linear-gradient(145deg, #141414, #1A1A1A);
        border: 1px solid #222;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 8px;
        transition: all 0.3s ease;
    }

    .fashion-card:hover {
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }

    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        color: #E8E4DF;
        margin-bottom: 8px;
        font-weight: 500;
    }

    .card-detail {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #7A7570;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .card-badge {
        display: inline-block;
        background-color: rgba(212, 175, 55, 0.15);
        color: #D4AF37;
        padding: 3px 10px;
        border-radius: 20px;
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-right: 6px;
        margin-top: 6px;
    }

    .hero-text {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        color: #E8E4DF;
        font-weight: 400;
        line-height: 1.2;
        letter-spacing: 2px;
    }

    .hero-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #7A7570;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 12px;
    }

    .look-piece {
        background: linear-gradient(145deg, #141414, #1C1C1C);
        border-left: 3px solid #D4AF37;
        padding: 14px 18px;
        margin-bottom: 8px;
        border-radius: 0 6px 6px 0;
    }

    .look-category {
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        color: #D4AF37;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2px;
    }

    .look-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.05rem;
        color: #E8E4DF;
    }

    .look-meta {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        color: #6A6560;
        letter-spacing: 0.5px;
    }

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        border-bottom: 1px solid #222;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.7rem !important;
        color: #7A7570 !important;
        padding: 12px 24px !important;
    }

    .stTabs [aria-selected="true"] {
        color: #D4AF37 !important;
        border-bottom: 2px solid #D4AF37 !important;
    }

    /* ─── FIX: File Uploader - Sem duplicação de texto ─── */
    .stFileUploader {
        border: 1px dashed #333 !important;
        border-radius: 6px;
    }

    .stFileUploader label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        color: #7A7570 !important;
        letter-spacing: 1px !important;
    }

    .stFileUploader section > button {
        font-size: 0.7rem !important;
        letter-spacing: 1px !important;
        color: #B8B2A8 !important;
        background: #1A1A1A !important;
        border: 1px solid #333 !important;
    }

    /* Esconde TODOS os textos duplicados do file uploader */
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }
    
    .stFileUploader small {
        display: none !important;
    }

    /* ─── Hide Streamlit Branding ─── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════
if "token" not in st.session_state:
    st.session_state["token"] = None
if "editing_id" not in st.session_state:
    st.session_state["editing_id"] = None
if "confirm_delete" not in st.session_state:
    st.session_state["confirm_delete"] = None
if "auth_page" not in st.session_state:
    st.session_state["auth_page"] = "Login"

BASE_URL = "http://localhost:8000"

# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.title("SmartWardrobe")

    if st.session_state["token"] is None:
        st.markdown("""
        <div style="font-family: Inter; font-size: 0.7rem; color: #5A5550; letter-spacing: 1.5px; text-transform: uppercase; margin: 16px 0 8px 0;">
            Acesse sua conta
        </div>
        """, unsafe_allow_html=True)

        # Botões estilizados em vez de radio para Login/Cadastro
        col_l, col_c = st.columns(2)
        with col_l:
            if st.button("Login", key="sidebar_login", use_container_width=True):
                st.session_state["auth_page"] = "Login"
                st.rerun()
        with col_c:
            if st.button("Cadastro", key="sidebar_cadastro", use_container_width=True):
                st.session_state["auth_page"] = "Cadastro"
                st.rerun()

        selected_menu = st.session_state["auth_page"]
    else:
        st.markdown('<p style="font-family: Inter; font-size: 0.7rem; color: #D4AF37; letter-spacing: 1.5px;">● CONECTADO</p>', unsafe_allow_html=True)
        selected_menu = st.radio("Menu", ["Meu Guarda-Roupa", "Gerar Look", "Configurações"], label_visibility="collapsed")

        st.markdown("---")
        if st.button("Encerrar Sessão", use_container_width=True):
            st.session_state["token"] = None
            st.session_state["editing_id"] = None
            st.session_state["confirm_delete"] = None
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# TELAS DE AUTENTICAÇÃO
# ══════════════════════════════════════════════════════════════════════
if selected_menu == "Cadastro":
    col_spacer1, col_form, col_spacer2 = st.columns([1, 2, 1])
    with col_form:
        st.markdown("")
        st.markdown('<div class="hero-text">Criar Conta</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Junte-se ao SmartWardrobe</div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown("")

        # Uso de st.form para garantir que o Enter/click no botão funcionem 100%
        with st.form("form_cadastro", border=False):
            email_cad = st.text_input("E-mail", placeholder="seu@email.com")
            password_cad = st.text_input("Senha", type="password", placeholder="Mínimo 6 caracteres")

            st.markdown("")
            submitted = st.form_submit_button("Criar Conta", use_container_width=True, type="primary")
            
            if submitted:
                if not email_cad or not password_cad:
                    st.warning("Preencha todos os campos.")
                else:
                    response = api_client.register(email_cad, password_cad)
                    if "email" in response:
                        st.success("Conta criada! Clique em 'Login' na barra lateral para entrar.")
                    else:
                        st.error(f"Erro: {response.get('detail', 'Falha desconhecida')}")

elif selected_menu == "Login":
    col_spacer1, col_form, col_spacer2 = st.columns([1, 2, 1])
    with col_form:
        st.markdown("")
        st.markdown('<div class="hero-text">Bem-vindo</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Acesse seu guarda-roupa inteligente</div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown("")

        # Uso de st.form para o Login também
        with st.form("form_login", border=False):
            email_login = st.text_input("E-mail", placeholder="seu@email.com")
            password_login = st.text_input("Senha", type="password", placeholder="Sua senha")

            st.markdown("")
            submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")
            
            if submitted:
                if not email_login or not password_login:
                    st.warning("Preencha todos os campos.")
                else:
                    response = api_client.login(email_login, password_login)
                    if "access_token" in response:
                        st.session_state["token"] = response["access_token"]
                        st.rerun()
                    else:
                        st.error(f"Erro: {response.get('detail', 'Credenciais inválidas')}")

# ══════════════════════════════════════════════════════════════════════
# GERAR LOOK
# ══════════════════════════════════════════════════════════════════════
elif selected_menu == "Gerar Look":
    st.markdown("")
    st.markdown('<div class="hero-text">Look do Dia</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Inteligência artificial aplicada ao seu estilo</div>', unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")

    col1, col2 = st.columns([3, 1])
    with col1:
        city = st.text_input("Cidade", placeholder="Ex: São Paulo, Curitiba, Ushuaia...", label_visibility="collapsed")
    with col2:
        btn_recommend = st.button("Gerar Look", use_container_width=True, type="primary")

    if btn_recommend:
        if not city:
            st.warning("Digite o nome da sua cidade.")
        else:
            with st.spinner("Analisando clima e montando combinações..."):
                look = api_client.get_recommendation(st.session_state["token"], city)

                if look and isinstance(look, list) and len(look) > 0:
                    st.markdown("")
                    st.markdown("---")
                    st.markdown("")

                    icons = {
                        "Superior": "👕", "Inferior": "👖",
                        "Calcado": "👟", "Cobertura": "🧥"
                    }

                    for part in look:
                        icon = icons.get(part['category'], "👔")
                        st.markdown(f"""
                        <div class="look-piece">
                            <div class="look-category">{part['category']}</div>
                            <div class="look-name">{icon} {part['name']}</div>
                            <div class="look-meta">{part['color']} · {part['style']} · {part['weather']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                else:
                    st.markdown("")
                    st.info("Não há peças suficientes para montar um look para o clima atual. Cadastre mais roupas no seu guarda-roupa!")

# ══════════════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ══════════════════════════════════════════════════════════════════════
elif selected_menu == "Configurações":
    col_spacer1, col_form, col_spacer2 = st.columns([1, 2, 1])
    with col_form:
        st.markdown("")
        st.markdown('<div class="hero-text">Configurações</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-sub">Personalize como a IA entende o seu conforto térmico</div>', unsafe_allow_html=True)
        st.markdown("")
        st.markdown("")

        st.markdown("""
        <div style="font-family: Inter; font-size: 0.75rem; color: #7A7570; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 8px;">
            Limiar de temperatura (ºC)
        </div>
        <div style="font-family: Inter; font-size: 0.8rem; color: #9A9590; margin-bottom: 16px;">
            Abaixo deste valor, a IA considerará o clima como <strong style="color: #6CB4EE;">Frio</strong>. 
            Acima, será considerado <strong style="color: #E07A5F;">Calor</strong>.
        </div>
        """, unsafe_allow_html=True)

        threshold = st.slider("Limiar", min_value=5, max_value=40, value=22, label_visibility="collapsed")

        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <span style="font-family: 'Playfair Display'; font-size: 3rem; color: #E8E4DF;">{threshold}°</span>
            <br>
            <span style="font-family: Inter; font-size: 0.7rem; color: #7A7570; letter-spacing: 2px;">GRAUS CELSIUS</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Salvar Preferência", use_container_width=True, type="primary"):
            api_client.update_settings(st.session_state["token"], threshold)
            st.success(f"Preferência salva. Temperaturas abaixo de {threshold}°C serão classificadas como Frio.")

# ══════════════════════════════════════════════════════════════════════
# MEU GUARDA-ROUPA
# ══════════════════════════════════════════════════════════════════════
elif selected_menu == "Meu Guarda-Roupa":
    st.markdown("")
    st.markdown('<div class="hero-text">Meu Guarda-Roupa</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Gerencie sua coleção pessoal</div>', unsafe_allow_html=True)
    st.markdown("")

    tab_colecao, tab_adicionar = st.tabs(["COLEÇÃO", "ADICIONAR PEÇA"])

    # ═══════════════════════════════════════
    # TAB: ADICIONAR PEÇA
    # ═══════════════════════════════════════
    with tab_adicionar:
        st.markdown("")
        col_spacer1, col_form, col_spacer2 = st.columns([1, 3, 1])
        with col_form:
            nome = st.text_input("Nome da Peça", placeholder="Ex: Camiseta Oversized Preta")

            col1, col2 = st.columns(2)
            with col1:
                categoria = st.selectbox("Categoria", ["Superior", "Inferior", "Calcado", "Cobertura"])
                cor = st.selectbox("Cor", ["Neutro", "Primaria", "Estampada"])
            with col2:
                clima = st.selectbox("Clima Ideal", ["Neutro", "Frio", "Calor"])
                estilo = st.selectbox("Estilo", ["Casual", "Social", "Esportivo"])

            st.markdown("")
            foto = st.file_uploader("Foto da peça (opcional)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

            st.markdown("")
            if st.button("Adicionar ao Guarda-Roupa", use_container_width=True, type="primary"):
                if not nome:
                    st.warning("Dê um nome para sua peça.")
                else:
                    image_url = None
                    if foto is not None:
                        res_foto = api_client.upload_image(st.session_state["token"], foto.getvalue(), foto.name)
                        image_url = res_foto.get("image_url")

                    dados = {
                        "name": nome, "category": categoria, "weather": clima,
                        "color": cor, "style": estilo, "image_url": image_url
                    }
                    api_client.create_clothing(st.session_state["token"], dados)
                    st.success(f"'{nome}' adicionada com sucesso!")
                    st.rerun()

    # ═══════════════════════════════════════
    # TAB: COLEÇÃO
    # ═══════════════════════════════════════
    with tab_colecao:
        st.markdown("")
        roupas = api_client.get_clothes(st.session_state["token"])

        if not roupas:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <div style="font-family: 'Playfair Display'; font-size: 1.5rem; color: #4A4540; margin-bottom: 12px;">
                    Seu guarda-roupa está vazio
                </div>
                <div style="font-family: Inter; font-size: 0.8rem; color: #3A3530; letter-spacing: 1px;">
                    Acesse a aba "ADICIONAR PEÇA" para começar sua coleção.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            total = len(roupas)
            cats = {}
            for r in roupas:
                cats[r['category']] = cats.get(r['category'], 0) + 1

            resumo_items = " · ".join([f"{v} {k}" for k, v in sorted(cats.items())])
            st.markdown(f"""
            <div style="font-family: Inter; font-size: 0.7rem; color: #5A5550; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px;">
                {total} PEÇAS — {resumo_items}
            </div>
            """, unsafe_allow_html=True)

            cols = st.columns(3)

            for idx, r in enumerate(roupas):
                with cols[idx % 3]:

                    # ── Modo edição ──
                    if st.session_state["editing_id"] == r['id']:
                        with st.container(border=True):
                            st.markdown(f"**Editando: {r['name']}**")
                            edit_name = st.text_input("Nome", value=r['name'], key=f"ename_{r['id']}")

                            ec1, ec2 = st.columns(2)
                            with ec1:
                                cat_options = ["Superior", "Inferior", "Calcado", "Cobertura"]
                                edit_cat = st.selectbox("Categoria", cat_options, index=cat_options.index(r['category']) if r['category'] in cat_options else 0, key=f"ecat_{r['id']}")
                                cor_options = ["Neutro", "Primaria", "Estampada"]
                                edit_cor = st.selectbox("Cor", cor_options, index=cor_options.index(r['color']) if r['color'] in cor_options else 0, key=f"ecor_{r['id']}")
                            with ec2:
                                cli_options = ["Neutro", "Frio", "Calor"]
                                edit_clima = st.selectbox("Clima", cli_options, index=cli_options.index(r['weather']) if r['weather'] in cli_options else 0, key=f"ecli_{r['id']}")
                                sty_options = ["Casual", "Social", "Esportivo"]
                                edit_estilo = st.selectbox("Estilo", sty_options, index=sty_options.index(r['style']) if r['style'] in sty_options else 0, key=f"esty_{r['id']}")

                            edit_foto = st.file_uploader("Nova foto", type=["jpg", "jpeg", "png"], key=f"efoto_{r['id']}", label_visibility="collapsed")

                            bc1, bc2 = st.columns(2)
                            with bc1:
                                if st.button("Salvar", key=f"save_{r['id']}", use_container_width=True, type="primary"):
                                    update_data = {
                                        "name": edit_name, "category": edit_cat, "weather": edit_clima,
                                        "color": edit_cor, "style": edit_estilo
                                    }
                                    if edit_foto is not None:
                                        res_foto = api_client.upload_image(st.session_state["token"], edit_foto.getvalue(), edit_foto.name)
                                        update_data["image_url"] = res_foto.get("image_url")

                                    api_client.update_clothing(st.session_state["token"], r['id'], update_data)
                                    st.session_state["editing_id"] = None
                                    st.rerun()
                            with bc2:
                                if st.button("Cancelar", key=f"cancel_{r['id']}", use_container_width=True):
                                    st.session_state["editing_id"] = None
                                    st.rerun()

                    # ── Card normal ──
                    else:
                        if r.get("image_url"):
                            try:
                                st.image(f"{BASE_URL}/{r['image_url']}", use_container_width=True)
                            except:
                                pass

                        icons = {"Superior": "👕", "Inferior": "👖", "Calcado": "👟", "Cobertura": "🧥"}
                        icon = icons.get(r['category'], "👔")

                        st.markdown(f"""
                        <div class="fashion-card">
                            <div class="card-detail">{r['category']}</div>
                            <div class="card-title">{icon} {r['name']}</div>
                            <div>
                                <span class="card-badge">{r['color']}</span>
                                <span class="card-badge">{r['style']}</span>
                                <span class="card-badge">{r['weather']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            if st.button("✏️ Editar", key=f"edit_{r['id']}", use_container_width=True):
                                st.session_state["editing_id"] = r['id']
                                st.session_state["confirm_delete"] = None
                                st.rerun()
                        with btn_col2:
                            if st.session_state["confirm_delete"] == r['id']:
                                if st.button("⚠ Confirmar", key=f"cdel_{r['id']}", use_container_width=True):
                                    api_client.delete_clothing(st.session_state["token"], r['id'])
                                    st.session_state["confirm_delete"] = None
                                    st.rerun()
                            else:
                                if st.button("🗑 Excluir", key=f"del_{r['id']}", use_container_width=True):
                                    st.session_state["confirm_delete"] = r['id']
                                    st.rerun()
