import pandas as pd
from itertools import product, combinations

# A função agora recebe o parâmetro 'temperatura_usuario' e gera looks de 4 peças
def recomendar_looks(df, temperatura_usuario):
    
    # 1. IMPLEMENTAÇÃO DO FILTRO DE TEMPERATURA
    if temperatura_usuario not in ['Frio', 'Calor']:
        df_filtrado = df
    else:
        # Filtra as peças que são ideais para a temperatura OU são Neutras
        df_filtrado = df[
            (df['TEMPERATURA_IDEAL'] == temperatura_usuario) | 
            (df['TEMPERATURA_IDEAL'] == 'Neutro')
        ].reset_index(drop=True)

    if df_filtrado.empty:
        return pd.DataFrame([{'Mensagem': f'Nenhuma peça disponível para a temperatura: {temperatura_usuario}.'}])
    
    # 2. SEPARAÇÃO DO DATAFRAME POR CATEGORIA FUNCIONAL
    # Usamos itertuples() para acesso mais rápido aos dados (em vez de .loc)
    df_superior = df_filtrado[df_filtrado['TIPO'].isin(['Camiseta', 'Regata', 'Blusa', 'Camisa'])]
    df_inferior = df_filtrado[df_filtrado['TIPO'].isin(['Calça', 'Saia', 'Bermuda', 'Short'])]
    df_calcado = df_filtrado[df_filtrado['TIPO'].isin(['Tênis', 'Sapato', 'Bota'])]
    
    # PEÇA DE COBERTURA: Frio ou Neutro (Sempre disponível, mas será "NENHUM" se não houver peça real)
    df_cobertura_filtrado = df_filtrado[df_filtrado['TIPO'].isin(['Casaco', 'Blazer', 'Jaqueta', 'Cardigã'])]
    
    # PEÇA NENHUM (Placeholder para quando não há cobertura ou não é necessário)
    df_cobertura = pd.concat([
        df_cobertura_filtrado, 
        pd.DataFrame([{'ID_PECA': 'NENHUM', 'TIPO': 'NENHUM', 'COR': 'NENHUM', 'ESTILO': 'NENHUM', 'STATUS_USO': 0, 'IMAGEM_LINK': 'NENHUM', 'TEMPERATURA_IDEAL': 'NENHUM'}])
    ], ignore_index=True)
    
    # Verificação de segurança (apenas para as peças obrigatórias)
    if df_superior.empty or df_inferior.empty or df_calcado.empty:
         return pd.DataFrame([{'Mensagem': 'Não há peças suficientes em todas as categorias (Superior, Inferior, Calçado) para montar looks completos.'}])

    looks_completos = []

    # 3. GERAÇÃO DE LOOKS DE 4 PEÇAS (Superior, Inferior, Calçado, Cobertura)
    # Usamos .itertuples() para acesso direto às linhas do DataFrame
    for sup_row, inf_row, calc_row, cob_row in product(df_superior.itertuples(), df_inferior.itertuples(), df_calcado.itertuples(), df_cobertura.itertuples()):
        
        pecas_do_look = [
            sup_row, # Superior
            inf_row, # Inferior
            calc_row, # Calçado
            cob_row # Cobertura
        ]
        
        total_score = 0
        
        # 4. LOOP PARA PONTUAR TODAS as duplas DENTRO DESTE LOOK
        # Filtra a peça "NENHUM" para o scoring
        pecas_validas = [p for p in pecas_do_look if p.ID_PECA != 'NENHUM']

        for peca1, peca2 in combinations(pecas_validas, 2):
            
            # ********** REGRAS DE PONTUAÇÃO ORIGINAIS **********

            # Regra de Cores Seguras (Neutro com Primária)
            cores_seguras = ['Neutro', 'Primária']
            if (peca1.COR == 'Neutro' and peca2.COR in cores_seguras) or \
               (peca2.COR == 'Neutro' and peca1.COR in cores_seguras):
                total_score += 5

            # Regra de Estilo Correspondente
            if peca1.ESTILO == peca2.ESTILO:
                total_score += 3

            # Regra de Penalidade por Estampas Duplas
            if peca1.COR == 'Estampada' and peca2.COR == 'Estampada':
                total_score -= 10

            # Regra de Combinação de Tipos (Bônus por Superior-Inferior funcional)
            tipos_inferiores = ['Calça', 'Saia', 'Bermuda', 'Short']
            tipos_principais = ['Camiseta', 'Regata', 'Blusa', 'Camisa']
            if (peca1.TIPO in tipos_inferiores and peca2.TIPO in tipos_principais) or \
               (peca2.TIPO in tipos_inferiores and peca1.TIPO in tipos_principais):
                total_score += 2 

            # Regra de Penalidade por Status de Uso Alto (Muitas Vezes Usada)
            if peca1.STATUS_USO >= 3 and peca2.STATUS_USO >= 3:
                total_score -= 5

            # Regra de Penalidade por Tipos Duplicados
            tipos_duplicados = ['Camiseta', 'Calça', 'Blazer', 'Saia', 'Casaco']
            if peca1.TIPO == peca2.TIPO and peca1.TIPO in tipos_duplicados:
                total_score -= 10

            # Regra de Bônus para Combinação de Tênis com Inferior Válido
            tipos_calcado_check = ['Tênis']
            tipos_inferior_valido = ['Calça', 'Saia', 'Bermuda', 'Short']
            is_tenis_pair = (peca1.TIPO in tipos_calcado_check and peca2.TIPO in tipos_inferior_valido) or \
                            (peca2.TIPO in tipos_calcado_check and peca1.TIPO in tipos_inferior_valido)
            if is_tenis_pair:
                total_score += 4
                
            # ********** FIM DAS REGRAS ORIGINAIS **********

        if total_score > 0:
            looks_completos.append({
                'Superior': sup_row.ID_PECA,
                'Inferior': inf_row.ID_PECA,
                'Calçado': calc_row.ID_PECA,
                'Cobertura': cob_row.ID_PECA,
                'Score': total_score
            })

    df_looks = pd.DataFrame(looks_completos)
    return df_looks.sort_values(by='Score', ascending=False).reset_index(drop=True)
