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
if "approved_temp_blacklist" not in st.session_state: 
    st.session_state.approved_temp_blacklist = []
if "cadastro_key" not in st.session_state:
    st.session_state.cadastro_key = 0
if "feedback_status" not in st.session_state:
    st.session_state.feedback_status = None
if "melhor_look" not in st.session_state:
    st.session_state.melhor_look = None
if "uploaded_file_obj" not in st.session_state:
    st.session_state.uploaded_file_obj = None


# --- Funções Auxiliares ---

def carregar_csv(uploaded_file):
    """Carrega o CSV e inicializa/reseta o DataFrame."""
    try:
        df = pd.read_csv(uploaded_file)
        
        # Garante a existência e o tipo correto das colunas
        for col, default_val, dtype in [
            ('TEMPERATURA_IDEAL', 'Neutro', str), 
            ('IMAGEM_LINK', "https://placehold.co/150x150/cccccc/333333?text=N/D", str),
            ('STATUS_USO', 0, int)
        ]:
            if col not in df.columns:
                # Se a coluna faltar, adiciona com valor padrão
                st.warning(f"Coluna '{col}' não encontrada. Adicionando com valor padrão.")
                df[col] = default_val
            elif dtype == int:
                 # Converte para numérico de forma segura
                 df[col] = pd.to_numeric(df[col], errors='coerce').fillna(default_val).astype(int)
            elif dtype == str:
                 df[col] = df[col].astype(str)

        st.session_state.df = df
        st.session_state.feedback_status = "CSV carregado com sucesso! Pronto para uso."
        st.session_state.rejeitados = [] 
        st.session_state.approved_temp_blacklist = []
        st.session_state.melhor_look = None
        
        return True
    except Exception as e:
        st.session_state.feedback_status = f"Erro ao carregar o arquivo CSV: {e}"
        return False


def atualizar_peca_imagem(peca_id, nova_imagem_link):
    """Atualiza o link da imagem para uma peça específica."""
    if st.session_state.df is not None:
        try:
            index_to_update = st.session_state.df[st.session_state.df['ID_PECA'] == peca_id].index
            
            if not index_to_update.empty:
                st.session_state.df.loc[index_to_update, 'IMAGEM_LINK'] = nova_imagem_link
                st.session_state.feedback_status = f"Imagem para a peça {peca_id} atualizada com sucesso!"
            else:
                st.session_state.feedback_status = f"Peça com ID {peca_id} não encontrada."
        except Exception as e:
            st.session_state.feedback_status = f"Erro ao atualizar a imagem: {e}"

    st.rerun()


# --- Sidebar: Inventário e Configurações ---
with st.sidebar:
    st.header("Inventário e Configurações")
    
    # 1. Carregar CSV (Chave adicionada para uploader)
    uploaded_file = st.file_uploader(
        "Carregar Arquivo CSV de Roupas", 
        type=['csv'],
        key="csv_uploader_unique"
    )
    
    st.session_state.uploaded_file_obj = uploaded_file

    # O contador de peças DEVE SER LIDO AQUI, SEMPRE NA SIDEBAR
    if st.session_state.df is not None:
        st.success("Inventário carregado!")
        
        # ATUALIZAÇÃO DO CONTADOR: Usa markdown para evitar bugs de cache do st.metric
        st.markdown(f"**Total de Peças no Inventário:** **{len(st.session_state.df)}**")
        
        # 2. Baixar Inventário
        csv = st.session_state.df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar Inventário Atualizado (CSV)",
            data=csv,
            file_name='inventario_guarda_roupa.csv',
            mime='text/csv',
        )
    
    # O botão SÓ aparece se um arquivo FOI CARREGADO e o DF AINDA NÃO EXISTE
    if st.session_state.uploaded_file_obj is not None and st.session_state.df is None:
        if st.button("Clique para Carregar Inventário", key="load_inventory_button"):
            if carregar_csv(st.session_state.uploaded_file_obj):
                st.rerun() 


# --- Abas Principais ---
tab1, tab2, tab3 = st.tabs(["✨ Recomendação", "➕ Cadastro de Peças", "📋 Ver Inventário"])


# --- TABELA 1: RECOMENDAÇÃO DE LOOK ---
with tab1:
    st.header("✨ Obtenha o Look do Dia") 
    
    # Exibir feedback de sucesso/rejeição
    if st.session_state.feedback_status:
        if "sucesso" in st.session_state.feedback_status.lower() or "registrado" in st.session_state.feedback_status.lower() or "aprovado" in st.session_state.feedback_status.lower():
            st.success(st.session_state.feedback_status)
        elif "erro" in st.session_state.feedback_status.lower() or "rejeição" in st.session_state.feedback_status.lower() or "nenhum" in st.session_state.feedback_status.lower():
            st.warning(st.session_state.feedback_status)
        st.session_state.feedback_status = None


    if st.session_state.df is None or st.session_state.df.empty:
        st.warning("⚠️ Não há dados! Por favor, carregue o CSV na barra lateral ou cadastre peças para começar a usar a IA.")
    else:
        
        # --- BLOCO: SELEÇÃO DE TEMPERATURA E BOTÃO DE GERAÇÃO ---
        with st.form(key="form_temp_selector_unique"):
            
            # 1. INPUT: Seleção de Temperatura
            temperatura_selecionada = st.radio(
                "Selecione a condição climática atual:",
                ('Frio', 'Calor'),
                index=0, 
                horizontal=True
            )

            # Botão de Geração de Look
            submitted_look = st.form_submit_button("🔥 Gerar Look Perfeito", type="primary")

            if submitted_look:
                st.session_state.approved_temp_blacklist = [] 
                
                # 2. Gera o look (CHAMADA DO BACKEND)
                try:
                    all_looks = recomendar_looks(st.session_state.df.copy(), temperatura_selecionada)
                    
                    if 'Mensagem' in all_looks.columns:
                        st.session_state.melhor_look = None
                        st.session_state.feedback_status = all_looks['Mensagem'].iloc[0]
                    else:
                        def create_look_tuple(row):
                            pecas = [row['Superior'], row['Inferior'], row['Calçado'], row['Cobertura']]
                            validas = [p for p in pecas if p != 'NENHUM']
                            return tuple(sorted(validas))

                        looks_to_filter = st.session_state.rejeitados + st.session_state.approved_temp_blacklist
                        
                        all_looks['look_tuple'] = all_looks.apply(create_look_tuple, axis=1)

                        all_looks = all_looks[~all_looks['look_tuple'].isin(looks_to_filter)]
                        
                        if not all_looks.empty:
                            # Pega a primeira recomendação e a converte para dicionário, descartando a coluna auxiliar
                            st.session_state.melhor_look = all_looks.iloc[0].drop(labels=['look_tuple']).to_dict() 
                        else:
                            st.session_state.melhor_look = None
                            st.session_state.feedback_status = "Nenhum look válido disponível após a filtragem de histórico. Tente aprovar/rejeitar novamente."
                
                except Exception as e:
                    print(f"Erro detalhado no motor de recomendação: {e}")
                    st.session_state.melhor_look = None
                    st.session_state.feedback_status = f"Erro no motor de recomendação: {e}. Por favor, verifique o terminal para detalhes."

                st.rerun()


        # --- EXIBIÇÃO DO LOOK (4 PEÇAS) ---
        if "melhor_look" in st.session_state and st.session_state.melhor_look is not None:
            melhor_look = st.session_state.melhor_look

            st.subheader("✅ Look Recomendado pela IA")
            st.markdown(f"**Score de Combinação:** `{melhor_look['Score']}`")
            
            # 1. RECUPERAÇÃO DAS INFORMAÇÕES DAS PEÇAS (4 IDs)
            peca_ids = [melhor_look['Superior'], melhor_look['Inferior'], melhor_look['Calçado'], melhor_look['Cobertura']]
            pecas_data = {}
            placeholder_url = "https://placehold.co/150x150/cccccc/333333?text=N/D"
            
            for id_peca in peca_ids:
                if id_peca == 'NENHUM':
                    pecas_data['NENHUM'] = {'TIPO': 'Sem Cobertura', 'COR': 'N/A', 'ESTILO': 'N/A', 'IMAGEM_LINK': placeholder_url}
                else:
                    pecas_data[id_peca] = st.session_state.df[st.session_state.df['ID_PECA'] == id_peca].iloc[0].to_dict()


            # 2. EXIBIÇÃO EM 4 COLUNAS
            col_sup, col_inf, col_calc, col_cob = st.columns(4)

            with col_sup:
                info_sup = pecas_data[melhor_look['Superior']]
                st.markdown("**Superior**")
                st.image(info_sup.get('IMAGEM_LINK', placeholder_url), 
                         caption=f"{info_sup['TIPO']} ({info_sup['COR']})", width=200)
                st.markdown(f"**Estilo:** {info_sup['ESTILO']}")

            with col_inf:
                info_inf = pecas_data[melhor_look['Inferior']]
                st.markdown("**Inferior**")
                st.image(info_inf.get('IMAGEM_LINK', placeholder_url), 
                         caption=f"{info_inf['TIPO']} ({info_inf['COR']})", width=200)
                st.markdown(f"**Estilo:** {info_inf['ESTILO']}")

            with col_calc:
                info_calc = pecas_data[melhor_look['Calçado']]
                st.markdown("**Calçado**")
                st.image(info_calc.get('IMAGEM_LINK', placeholder_url), 
                         caption=f"{info_calc['TIPO']} ({info_calc['COR']})", width=200)
                st.markdown(f"**Estilo:** {info_calc['ESTILO']}")

            with col_cob:
                info_cob = pecas_data[melhor_look['Cobertura']]
                st.markdown("**Cobertura**")
                caption_text = f"{info_cob['TIPO']} ({info_cob['COR']})" if info_cob['TIPO'] != 'Sem Cobertura' else 'Sem Cobertura'
                st.image(info_cob.get('IMAGEM_LINK', placeholder_url), 
                         caption=caption_text, width=200)
                if info_cob['TIPO'] != 'Sem Cobertura':
                    st.markdown(f"**Estilo:** {info_cob['ESTILO']}")


            # Justificativa da IA
            st.markdown("---")
            st.markdown("##### Justificativa da IA (Regras Aplicadas):")
            st.info("Esta combinação obteve alta pontuação por atender às regras de **Consistência de Categoria (Superior + Inferior + Calçado + Cobertura)** e às suas regras de **Estilo** e **Cores**. O filtro de **Temperatura** foi aplicado.")


            # --- Feedback Loop (Aprender com o Usuário) ---
            st.subheader("🔁 Feedback da Combinação")
            
            feedback = st.radio("Você aprova este look?", ["Aprovar 😍", "Rejeitar 😐"], key='feedback_radio')
            
            if st.button("Registrar Feedback e Continuar"):
                
                pecas_ids_list = [melhor_look['Superior'], melhor_look['Inferior'], melhor_look['Calçado'], melhor_look['Cobertura']]
                pecas_ids_validas = [pid for pid in pecas_ids_list if pid != 'NENHUM']
                current_look_tuple = tuple(sorted(pecas_ids_validas))


                if feedback == "Aprovar 😍":
                    st.session_state.df.loc[st.session_state.df['ID_PECA'].isin(pecas_ids_validas), 'STATUS_USO'] -= 1
                    st.session_state.feedback_status = "Aprovado! Look salvo no histórico. Pontuação das peças ajustada."
                    st.session_state.approved_temp_blacklist.append(current_look_tuple)

                else: # Rejeitar 😐
                    st.session_state.df.loc[st.session_state.df['ID_PECA'].isin(pecas_ids_validas), 'STATUS_USO'] += 2
                    st.session_state.rejeitados.append(current_look_tuple)
                    st.session_state.feedback_status = "Rejeição registrada! A IA buscará a próxima melhor opção..."
                
                if 'melhor_look' in st.session_state:
                     del st.session_state.melhor_look
                st.rerun()


# --- TABELA 2: CADASTRO DE PEÇAS ---
with tab2:
    st.header("➕ Cadastrar Nova Peça")
    
    if st.session_state.df is None:
        st.warning("Carregue o inventário primeiro para começar a cadastrar.")
    else:
        # CORRIGIDO: Removido o primeiro argumento posicional (o "label")
        with st.form(key=f"cadastro_form_{st.session_state.cadastro_key}"):
            
            peca_ids = st.session_state.df['ID_PECA'].tolist()
            novo_id = f"P{len(peca_ids) + 1:02d}"
            
            st.markdown(f"**ID da Peça:** `{novo_id}` (Gerado Automaticamente)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                tipo = st.selectbox("Tipo da Peça:", ('Camiseta', 'Calça', 'Saia', 'Tênis', 'Blazer', 'Casaco', 'Vestido', 'Regata', 'Blusa', 'Bermuda', 'Short', 'Sapato', 'Bota', 'Jaqueta', 'Cardigã'), key="tipo_cadastro")
            with col2:
                cor = st.selectbox("Cor / Padrão:", ('Neutro', 'Primária', 'Estampada', 'Secundária'), key="cor_cadastro")
            with col3:
                estilo = st.selectbox("Estilo:", ('Casual', 'Formal', 'Esportivo', 'Jeans'), key="estilo_cadastro")
                
            temperatura = st.selectbox("Temperatura Ideal:", ('Neutro', 'Frio', 'Calor'), key="temp_cadastro")
            
            ocasiao = st.multiselect("Ocasião (Pode selecionar várias):", ('Casual', 'Trabalho', 'Festa', 'Esporte'), default=['Casual'], key="ocasiao_cadastro")
            status_uso = st.number_input("Status de Uso (0 = Nunca usado, 5 = Muito usado):", min_value=0, max_value=5, value=0, key="status_cadastro")
            
            uploaded_file_obj = st.file_uploader("Upload da Foto da Peça:", type=['jpg', 'png'], key="uploader_img")
            
            submitted = st.form_submit_button("💾 Salvar Nova Peça", type="primary")

            if submitted:
                imagem_data_url = "https://placehold.co/150x150/cccccc/333333?text=N/D"
                
                if uploaded_file_obj is not None:
                    try:
                        bytes_data = uploaded_file_obj.getvalue()
                        base64_encoded_data = base64.b64encode(bytes_data).decode()
                        mime_type = uploaded_file_obj.type
                        imagem_data_url = f"data:{mime_type};base64,{base64_encoded_data}"
                    except Exception as e:
                        st.error(f"Erro ao processar a imagem: {e}")
                        st.stop()
                
                nova_peca = pd.DataFrame([{
                    'ID_PECA': novo_id,
                    'TIPO': tipo,
                    'COR': cor,
                    'ESTILO': estilo,
                    'STATUS_USO': status_uso,
                    'IMAGEM_LINK': imagem_data_url,
                    'TEMPERATURA_IDEAL': temperatura, 
                    'OCASIAO': ', '.join(ocasiao)
                }])
                
                st.session_state.df = pd.concat([st.session_state.df, nova_peca], ignore_index=True)
                
                # REFORÇO NO FEEDBACK E ATUALIZAÇÃO DA CHAVE
                st.info(f"Peça {novo_id} cadastrada! Total de peças atualizado para {len(st.session_state.df)}.")
                st.session_state.feedback_status = f"Peça {novo_id} cadastrada com sucesso."
                st.session_state.cadastro_key += 1
                st.rerun() 
        
        # --- Atualização de Imagem de Peça Existente (Restaurado) ---
        st.markdown("---")
        st.subheader("🖼️ Atualizar Imagem de Peça Existente")
        if not st.session_state.df.empty:
            peca_ids = st.session_state.df['ID_PECA'].tolist()
            
            with st.form(key="form_update_img_unique"): # Chave única
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
                        except Exception as e:
                            st.session_state.feedback_status = f"Erro ao processar a imagem: {e}"
                    else:
                        st.session_state.feedback_status = "Por favor, faça o upload de uma imagem."
                        st.rerun()
        else:
            st.warning("Nenhuma peça cadastrada para atualizar.")


# --- TABELA 3: VER INVENTÁRIO ---
with tab3:
    st.header("📋 Inventário Completo")
    if st.session_state.df is not None:
        cols_display = ['ID_PECA', 'TIPO', 'COR', 'ESTILO', 'TEMPERATURA_IDEAL', 'OCASIAO', 'STATUS_USO', 'IMAGEM_LINK']
        df_display = st.session_state.df.reindex(columns=[c for c in cols_display if c in st.session_state.df.columns])
        st.dataframe(df_display)
    else:
        st.info("O inventário está vazio.")