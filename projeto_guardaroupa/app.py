import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import base64 

# Garante que o motor de recomendação (backend) possa ser importado
# Assumimos que 'motor_recomendacao.py' está no mesmo diretório
sys.path.append(str(Path(__file__).resolve().parent))

# Importa o coração da IA
from motor_recomendacao import recomendar_looks

# --- Configuração Inicial ---
st.set_page_config(page_title="IA Guarda-Roupa", page_icon="👗", layout="wide")
st.title("🧠 IA Guarda-Roupa: Seu Estilista Pessoal")

# --- Variáveis de Estado (Simulação do Banco de Dados/Histórico) ---
if "df" not in st.session_state:
    st.session_state.df = None
if "rejeitados" not in st.session_state:
    st.session_state.rejeitados = []
# NOVA LISTA: Temporariamente armazena o look aprovado para forçar a variedade no próximo clique
if "approved_temp_blacklist" not in st.session_state: 
    st.session_state.approved_temp_blacklist = []
if "cadastro_key" not in st.session_state:
    st.session_state.cadastro_key = 0 # Adiciona uma chave para forçar a limpeza do formulário
if "feedback_status" not in st.session_state:
    st.session_state.feedback_status = None # Mensagens de sucesso/erro unificadas
# NOVO: Variável para controlar se o botão de feedback foi clicado
if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = False


# --- Funções de Lógica ---

def gerar_look():
    """Chama o motor de IA e aplica o filtro de rejeição."""
    if st.session_state.df is None:
        st.error("Por favor, carregue um inventário CSV primeiro.")
        return None
        
    looks = recomendar_looks(st.session_state.df.copy())
    
    # Prepara a lista total de looks a serem excluídos (rejeitados + aprovado temporário)
    looks_to_filter = st.session_state.rejeitados + st.session_state.approved_temp_blacklist

    # Aplica o filtro R5 do feedback: ignora looks rejeitados na sessão E looks aprovados recentemente
    if looks_to_filter:
        looks = looks[~looks.apply(lambda x: tuple(sorted([x['Peça 1'], x['Peça 2']])) in looks_to_filter, axis=1)]

    if not looks.empty:
        return looks.iloc[0]
    else:
        return None

# FUNÇÃO CADASTRAR PEÇA ATUALIZADA
def cadastrar_peca(tipo, cor, estilo, imagem_data_url=None):
    """Simula o Ciclo 1: Adiciona uma nova peça ao DataFrame, usando Data URL se houver upload."""
    novo_id = f"P{len(st.session_state.df) + 1}"
    
    # Define o link da imagem: usa a URL Base64 da imagem se fornecida, caso contrário usa o placeholder padrão.
    image_link_to_save = imagem_data_url if imagem_data_url else f"https://placehold.co/150x150/1d4ed8/ffffff?text={tipo.replace(' ', '+')}"
    
    nova_peca = pd.DataFrame({
        'ID_PECA': [novo_id], 
        'TIPO': [tipo], 
        'COR': [cor], 
        'ESTILO': [estilo], 
        'STATUS_USO': [0],
        'IMAGEM_LINK': [image_link_to_save] # Usa o link/data URL gerado
    })
    
    st.session_state.df = pd.concat([st.session_state.df, nova_peca], ignore_index=True)
    
    # --- NOVIDADE: Feedback na Tela ---
    st.session_state.feedback_status = f"Peça '{tipo} {cor}' cadastrada com sucesso! (ID: {novo_id})"
    
    # Reinicia o formulário
    st.session_state.cadastro_key += 1
    
    # Força a atualização da página inteira para recarregar o contador da sidebar
    st.rerun() 

# NOVA FUNÇÃO: ATUALIZAR IMAGEM DE PEÇA EXISTENTE
def atualizar_peca_imagem(peca_id, imagem_data_url):
    """Atualiza o link de imagem (Data URL) de uma peça existente."""
    if st.session_state.df is not None and peca_id in st.session_state.df['ID_PECA'].values:
        st.session_state.df.loc[st.session_state.df['ID_PECA'] == peca_id, 'IMAGEM_LINK'] = imagem_data_url
        st.session_state.feedback_status = f"Imagem da peça {peca_id} atualizada com sucesso!"
        st.rerun()
    else:
        st.session_state.feedback_status = f"Erro: Peça {peca_id} não encontrada."


# --- Fluxo Principal do Aplicativo (Layout) ---

# 1. Carregamento do Inventário (Visível em ambas as abas)
uploaded_file = st.sidebar.file_uploader(
    "1. Carregar Inventário (CSV)",
    type="csv",
    help="Carregue o arquivo inventario.csv para iniciar o sistema."
)

if uploaded_file and st.session_state.df is None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"{len(st.session_state.df)} peças carregadas!")

# Se o inventário estiver carregado, mostra os detalhes na barra lateral
if st.session_state.df is not None:
    st.sidebar.markdown(f"**Inventário Atual:** {len(st.session_state.df)} Peças")
    with st.sidebar.expander("Ver Detalhes do Inventário"):
        # Mostra o ID, TIPO e se a IMAGEM_LINK está preenchida (para visualização do progresso)
        df_display = st.session_state.df[['ID_PECA', 'TIPO', 'COR', 'STATUS_USO', 'IMAGEM_LINK']].copy()
        df_display['IMAGEM_LINK'] = df_display['IMAGEM_LINK'].apply(lambda x: 'SIM' if (x and 'data:image' in x) else 'NÃO')
        st.dataframe(df_display, use_container_width=True)

# Define as abas
tab1, tab2 = st.tabs(["2. 👗 Recomendar Look", "3. 📝 Cadastro de Peças (Simulação IA)"])

# --- TABELA 1: RECOMENDAÇÃO DE LOOK (FLUXOGRAMA CICLO 2) ---
with tab1:
    st.header("Seu Estilo, Nossas Regras")
    
    # Exibir feedback de sucesso/rejeição
    if st.session_state.feedback_status:
        if "aprovado" in st.session_state.feedback_status.lower() or "registrado" in st.session_state.feedback_status.lower():
            st.success(st.session_state.feedback_status)
        elif "rejeição" in st.session_state.feedback_status.lower():
            st.warning(st.session_state.feedback_status)
        # Limpa o status para que não apareça no próximo clique
        st.session_state.feedback_status = None


    if st.session_state.df is None:
        st.warning("Por favor, carregue o inventário na barra lateral para começar.")
    else:
        # CORREÇÃO CRÍTICA: Se o usuário clicar no botão, limpamos a blacklist temporária de aprovados
        if st.button("✨ Gerar Look Ideal", type="primary"):
            # 1. Limpa a blacklist temporária para permitir que o look aprovado volte
            st.session_state.approved_temp_blacklist = [] 
            # 2. Gera o look
            st.session_state.melhor_look = gerar_look()
            # 3. Garante que o feedback seja processado apenas PELO BOTÃO
            st.session_state.feedback_submitted = False 


        if "melhor_look" in st.session_state and st.session_state.melhor_look is not None:
            melhor_look = st.session_state.melhor_look

            st.subheader("✅ Look Recomendado pela IA")
            st.markdown(f"**Score de Combinação:** `{melhor_look['Score']}`")
            
            # Recupera as informações das peças
            peca1_id = melhor_look['Peça 1']
            peca2_id = melhor_look['Peça 2']
            
            # Usa placeholder para imagens não encontradas
            placeholder = "https://placehold.co/150x150/cccccc/333333?text=N/D"

            peca1_data = st.session_state.df[st.session_state.df['ID_PECA'] == peca1_id].iloc[0]
            peca2_data = st.session_state.df[st.session_state.df['ID_PECA'] == peca2_id].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                st.image(peca1_data.get('IMAGEM_LINK', placeholder), 
                         caption=f"{peca1_data['TIPO']} ({peca1_data['COR']})", width=250)
            with col2:
                st.image(peca2_data.get('IMAGEM_LINK', placeholder), 
                         caption=f"{peca2_data['TIPO']} ({peca2_data['COR']})", width=250)

            # Justificativa da IA (Demonstração da lógica)
            st.markdown("---")
            st.markdown("##### Justificativa da IA (Regras Aplicadas):")
            st.info("Esta combinação obteve alta pontuação por atender às **Regras R1 (Segurança: Neutro + Colorido)** e **R2 (Consistência de Estilo)**.")


            # --- Feedback Loop (Aprender com o Usuário) ---
            st.subheader("🔁 Feedback da Combinação")
            
            # O rádio apenas define a escolha, mas não aciona o fluxo
            feedback = st.radio("Você aprova este look?", ["Aprovar 😍", "Rejeitar 😐"], key='feedback_radio')
            
            # Novo: O bloco de feedback agora só é processado após o clique no botão
            if st.button("Registrar Feedback e Continuar"):
                
                # Seta a variável de controle
                st.session_state.feedback_submitted = True
                
                # A lógica agora está aqui dentro
                current_look_tuple = tuple(sorted([peca1_id, peca2_id]))

                if feedback == "Aprovar 😍":
                    # MANTÉM: Ajusta STATUS_USO para baixo quando aprovado
                    st.session_state.df.loc[st.session_state.df['ID_PECA'].isin([peca1_id, peca2_id]), 'STATUS_USO'] -= 1
                    
                    # 1. Feedback de Sucesso
                    st.session_state.feedback_status = "Aprovado! Look salvo no histórico. Pontuação das peças ajustada."
                    
                    # 2. Adiciona à blacklist temporária para forçar a variedade no próximo clique
                    st.session_state.approved_temp_blacklist.append(current_look_tuple)

                    # 3. Reset da Interface
                    if 'melhor_look' in st.session_state:
                         del st.session_state.melhor_look # Remove o look da memória

                    # 4. Força o recarregamento para limpar a tela
                    st.rerun() 

                else: # Rejeitar 😐
                    # 1. Penaliza STATUS_USO (Regra R5)
                    st.session_state.df.loc[st.session_state.df['ID_PECA'].isin([peca1_id, peca2_id]), 'STATUS_USO'] += 2
                    
                    # 2. Marca look como rejeitado para não ser sugerido NOVAMENTE nesta sessão
                    st.session_state.rejeitados.append(current_look_tuple)
                    
                    # --- CORREÇÃO: Remove o look antigo da memória ---
                    if 'melhor_look' in st.session_state:
                         del st.session_state.melhor_look
                    # --- FIM DA CORREÇÃO ---

                    # 3. Tenta gerar um novo look Imediatamente
                    st.session_state.melhor_look = gerar_look()
                    
                    if st.session_state.melhor_look is None:
                        st.session_state.feedback_status = "Nenhum look válido disponível após os feedbacks."
                    else:
                        # Limpa o feedback_status para evitar que a mensagem de sucesso da aba de aprovação apareça aqui
                        st.session_state.feedback_status = None 
                        st.session_state.feedback_status = "Rejeição registrada! A IA está buscando o próximo melhor look..." # Esta mensagem aparece no próximo rerun

                    # 4. Força o recarregamento para exibir a nova sugestão imediatamente
                    st.rerun()

# --- TABELA 2: CADASTRO DE PEÇAS (FLUXOGRAMA CICLO 1 SIMULADO) ---
with tab2:
    st.header("Cadastro e Gerenciamento de Peças")
    
    # Exibe a mensagem de feedback unificada
    if st.session_state.feedback_status:
        if "sucesso" in st.session_state.feedback_status.lower() or "registrado" in st.session_state.feedback_status.lower():
            st.success(st.session_state.feedback_status)
        elif "erro" in st.session_state.feedback_status.lower():
            st.error(st.session_state.feedback_status)
        # Limpa o status após exibir (Será limpo após o st.rerun se não houver um novo status)
        # Manter st.session_state.feedback_status = None apenas para o caso de aprovação no tab2

    if st.session_state.df is None:
        st.warning("Carregue o inventário na barra lateral para habilitar o cadastro.")
    else:
        # --- SUB-SEÇÃO 1: CADASTRAR NOVA PEÇA ---
        st.subheader("1. Cadastrar Nova Peça")
        st.markdown("**(Simulação da IA)** Use esta seção para simular o cadastro de uma peça nova, com classificação automática.")
        
        with st.form(key=f"form_cadastro_peca_{st.session_state.cadastro_key}"): 
            colA, colB = st.columns(2)
            
            uploaded_file_obj = None
            
            with colA:
                st.caption("Simulação da Classificação da Imagem:")
                uploaded_file_obj = st.file_uploader("Upload da Foto (Input):", type=['jpg', 'png'], key=f"uploader_{st.session_state.cadastro_key}") 
                
                # Campos de seleção (O resultado que a IA real retornaria)
                novo_tipo = st.selectbox("1. Tipo de Peça:", options=['Calça', 'Camiseta', 'Blazer', 'Saia', 'Casaco', 'Vestido', 'Tênis'], index=0, key=f"tipo_{st.session_state.cadastro_key}")
            
            with colB:
                st.caption("Atributos Retornados:")
                # Baseado nos grupos da sua Regra IF/THEN
                nova_cor = st.selectbox("2. Cor (Classificação IA):", options=['Neutro', 'Primária', 'Estampada'], index=0, key=f"cor_{st.session_state.cadastro_key}")
                novo_estilo = st.selectbox("3. Estilo (Classificação IA):", options=['Casual', 'Formal', 'Básica', 'Jeans'], index=0, key=f"estilo_{st.session_state.cadastro_key}")
                
            submitted = st.form_submit_button("➕ Cadastrar Nova Peça (Salvar no DB)", type="primary")

            if submitted:
                imagem_data_url = None
                if uploaded_file_obj is not None:
                    try:
                        bytes_data = uploaded_file_obj.getvalue()
                        base64_encoded_data = base64.b64encode(bytes_data).decode()
                        mime_type = uploaded_file_obj.type
                        imagem_data_url = f"data:{mime_type};base64,{base64_encoded_data}"
                    except Exception as e:
                        st.session_state.feedback_status = f"Erro ao processar a imagem: {e}"
                
                if st.session_state.feedback_status is None or "Erro" not in st.session_state.feedback_status:
                    cadastrar_peca(novo_tipo, nova_cor, novo_estilo, imagem_data_url)
                    # st.rerun() chamado dentro de cadastrar_peca
        
        # --- SUB-SEÇÃO 2: ATUALIZAR IMAGEM DE PEÇA EXISTENTE (A SOLUÇÃO PARA A SUA PERGUNTA) ---
        st.markdown("---")
        st.subheader("2. Atualizar Imagem de Peça Existente")
        st.markdown("Use esta seção para adicionar fotos às peças que você carregou no CSV, como P01, P02, etc.")

        with st.form(key=f"form_atualizar_peca"):
            peca_ids = st.session_state.df['ID_PECA'].tolist()
            
            colC, colD = st.columns(2)

            with colC:
                peca_selecionada = st.selectbox(
                    "Selecione o ID da Peça para Atualizar:", 
                    options=peca_ids,
                    index=0,
                    key="peca_selecionada_update"
                )

            with colD:
                uploaded_update_file_obj = st.file_uploader(
                    "Upload da Nova Foto:", 
                    type=['jpg', 'png'], 
                    key="uploader_update_img"
                )

            submitted_update = st.form_submit_button("🖼️ Aplicar Nova Imagem", type="secondary")

            if submitted_update:
                if uploaded_update_file_obj is not None:
                    try:
                        bytes_data = uploaded_update_file_obj.getvalue()
                        base64_encoded_data = base64.b64encode(bytes_data).decode()
                        mime_type = uploaded_update_file_obj.type
                        imagem_data_url = f"data:{mime_type};base64,{base64_encoded_data}"
                        
                        atualizar_peca_imagem(peca_selecionada, imagem_data_url)
                        # st.rerun() chamado dentro de atualizar_peca_imagem
                    except Exception as e:
                        st.session_state.feedback_status = f"Erro ao processar a imagem: {e}"
                else:
                    st.session_state.feedback_status = "Por favor, faça o upload de uma imagem."
                    st.rerun() # Para exibir a mensagem de erro/aviso imediatamente
