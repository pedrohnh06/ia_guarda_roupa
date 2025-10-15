import pandas as pd
from itertools import combinations

def recomendar_looks(df):
    combinacoes = []

    for i, j in combinations(df.index, 2):
        peca1 = df.loc[i]
        peca2 = df.loc[j]
        score = 0

        cores_seguras = ['Neutro', 'Primária']
        if (peca1['COR'] == 'Neutro' and peca2['COR'] in cores_seguras) or \
           (peca2['COR'] == 'Neutro' and peca1['COR'] in cores_seguras):
            score += 5

        if peca1['ESTILO'] == peca2['ESTILO']:
            score += 3

        if peca1['COR'] == 'Estampada' and peca2['COR'] == 'Estampada':
            score -= 10

        tipos_inferiores = ['Calça', 'Saia']
        tipos_principais = ['Camiseta', 'Blazer', 'Casaco']
        if (peca1['TIPO'] in tipos_inferiores and peca2['TIPO'] in tipos_principais) or \
           (peca2['TIPO'] in tipos_inferiores and peca1['TIPO'] in tipos_principais):
            score += 2

        if peca1['STATUS_USO'] >= 3 and peca2['STATUS_USO'] >= 3:
            score -= 5

        tipos_duplicados = ['Camiseta', 'Calça', 'Blazer', 'Saia', 'Casaco']
        if peca1['TIPO'] == peca2['TIPO'] and peca1['TIPO'] in tipos_duplicados:
            score -= 10

        tipos_calcado = ['Tênis']
        tipos_inferior_valido = ['Calça', 'Saia']
        is_tenis_pair = (peca1['TIPO'] in tipos_calcado and peca2['TIPO'] in tipos_inferior_valido) or \
                        (peca2['TIPO'] in tipos_calcado and peca1['TIPO'] in tipos_inferior_valido)
        if is_tenis_pair:
            score += 4

        if score > 0:
            combinacoes.append({
                'Peça 1': peca1['ID_PECA'],
                'Peça 2': peca2['ID_PECA'],
                'Score': score
            })

    df_recomendacoes = pd.DataFrame(combinacoes)
    return df_recomendacoes.sort_values(by='Score', ascending=False).reset_index(drop=True)
