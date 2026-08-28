from itertools import product, combinations

class PecaDeRoupa:

    def __init__(self, id_peca, tipo, cor, estilo, status_uso, TEMPERATURA_IDEAL):
        self.id_peca = id_peca
        self.tipo = tipo
        self.cor = cor
        self.estilo = estilo
        self.status_uso = status_uso
        self.temperatura_ideal = TEMPERATURA_IDEAL
    
    def __repr__(self):
        return f"{self.tipo} {self.cor} {self.id_peca}"

class GuardaRoupa: 

    def __init__(self):
        self.catalogo = []

    def adicionar_peca(self, nova_peca):
        self.catalogo.append(nova_peca)

    def temperatura_usuario(self, temperatura):

        roupas_filtradas = []

        for c in self.catalogo:
            if c.temperatura_ideal == temperatura or c.temperatura_ideal == 'Neutro':
                roupas_filtradas.append(c)

        return roupas_filtradas

    def separar_por_categoria(self, lista_de_pecas):

        categorias = {"Superior": [], "Inferior": [], "Calcado": [], "Cobertura": []}

        for g in lista_de_pecas:
            if g.tipo in ['Camiseta', 'Regata', 'Blusa', 'Camisa']:
                categorias['Superior'].append(g)
            elif g.tipo in ['Calça', 'Saia', 'Bermuda', 'Short']:
                categorias['Inferior'].append(g)
            elif g.tipo in ['Tênis', 'Sapato', 'Bota']:
                categorias['Calcado'].append(g)
            elif g.tipo in ['Casaco', 'Blazer', 'Jaqueta']:
                categorias['Cobertura'].append(g)
        
        return categorias

class MotorDeRecomendacao:

    def __init__(self, categorias_separadas):
        self.categorias = categorias_separadas

    def gerar_looks_possiveis(self):
        sup = self.categorias['Superior']
        inf = self.categorias['Inferior']
        calc = self.categorias['Calcado']
        cob = self.categorias['Cobertura']

        if len(cob) == 0:
            peca_invisivel = PecaDeRoupa("NENHUM", "NENHUM", "NENHUM", "NENHUM", 0, "NENHUM")
            cob.append(peca_invisivel) 

        todos_os_looks = []

        for combinacao in product(sup, inf, calc, cob):
            todos_os_looks.append(combinacao)

        return todos_os_looks

    def avaliar_look(self, look_completo):
        score = 0
        pecas_validas = []
        cores_seguras = ['Neutro', 'Primaria']
        tipos_superiores = ['Camiseta', 'Regata', 'Blusa', 'Camisa']
        tipos_inferiores = ['Calça', 'Saia', 'Bermuda', 'Short']
        tipos_duplicados = ['Camiseta', 'Calça', 'Blazer', 'Saia', 'Casaco']

        for c in look_completo:
            if c.id_peca != "NENHUM":
                    pecas_validas.append(c)

        for peca1, peca2 in combinations(pecas_validas, 2):
            
            # Regra de estilo
            if peca1.estilo == peca2.estilo:
                    score += 3
            
            # Penalidade de estampa
            if peca1.cor == 'Estampada' and peca2.cor == 'Estampada':
                score -= 10

            # Penalidade de status de uso
            if peca1.status_uso >= 3 and peca2.status_uso >= 3:
                score -= 5

            # Penalidade de Tipos Duplicados 
            if peca1.tipo == peca2.tipo and peca1.tipo in tipos_duplicados:
                score -= 10
            
            # Regra de cores seguras
            if peca1.cor == 'Neutro' and peca2.cor in cores_seguras:
                score += 5

            # Bônus superior/inferior
            if peca1.tipo in tipos_inferiores and peca2.tipo in tipos_superiores or \
                 peca1.tipo in tipos_superiores and peca2.tipo in tipos_inferiores :
                score += 2
            
            # Bônus de Tênis
            if peca1.tipo in 'Tênis' and peca2.tipo in tipos_inferiores or \
                peca1.tipo in tipos_inferiores and peca2.tipo in 'Tênis':
                score += 4

        return score

    def recomendar(self):

        todos_os_looks = self.gerar_looks_possiveis()
        looks_aprovados = []

        for look in todos_os_looks:
            nota_do_look = self.avaliar_look(look)
            if nota_do_look > 0:
                looks_aprovados.append({'pecas': look, 'nota': nota_do_look})
        
        looks_aprovados.sort(key=lambda x: x['nota'], reverse=True)

        return looks_aprovados


import pandas as pd 

def recomendar_looks(df, temperatura):
    
    #Criamos o nosso guarda-roupa vazio
    meu_armario = GuardaRoupa()
    
    for index, row in df.iterrows():
        peca = PecaDeRoupa(
            id_peca=row['ID_PECA'],
            tipo=row['TIPO'],
            cor=row['COR'],
            estilo=row['ESTILO'],
            status_uso=row['STATUS_USO'],
            TEMPERATURA_IDEAL=row['TEMPERATURA_IDEAL']
        )
        meu_armario.adicionar_peca(peca)
        
    roupas_filtradas = meu_armario.temperatura_usuario(temperatura)
    gavetas_organizadas = meu_armario.separar_por_categoria(roupas_filtradas)
    motor = MotorDeRecomendacao(gavetas_organizadas)
    looks_gerados = motor.recomendar()
    
    if not looks_gerados:
        return pd.DataFrame([{'Mensagem': 'Nenhum look válido encontrado para esta temperatura ou regras.'}])
        
    dados_para_tela = []
    
    for resultado in looks_gerados:

        look_tupla = resultado['pecas']
        
        linha = {
            'Superior': look_tupla[0].id_peca,
            'Inferior': look_tupla[1].id_peca,
            'Calçado': look_tupla[2].id_peca, 
            'Cobertura': look_tupla[3].id_peca,
            'Score': resultado['nota']
        }
        dados_para_tela.append(linha)
        
    return pd.DataFrame(dados_para_tela)