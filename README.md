# 👗 IA Guarda-Roupa: Otimizador de Looks e Consumo Consciente (MVP)

https://iaguardaroupa-fe5d74fyanbgouc2w4yjsm.streamlit.app/

## 💡 Visão Geral do Projeto
Este projeto é um **Protótipo Mínimo Viável (MVP)** de um aplicativo de recomendação de vestuário desenvolvido para a UC HUB, com o objetivo principal de promover o **consumo consciente** e combater a indecisão ("o que vestir?").

O sistema demonstra a aplicação de **Inteligência Artificial (IA)** e **Metodologias Ágeis** (Sprints) para criar um sistema de aprendizado contínuo.

### ✨ Diferenciais Técnicos e Inovação
* **Algoritmo de Recomendação Baseado em Regras:** O sistema utiliza **6 regras de moda (IF/THEN)** para pontuar e ranquear as combinações de peças, garantindo harmonia visual.

* **Simulação de Transfer Learning:** O processo de cadastro simula a classificação de imagens (Visão Computacional) por uma arquitetura pré-treinada (como ResNet), provando a viabilidade técnica.

* **Feedback Loop Funcional (Aprendizado da IA):** O aplicativo registra explicitamente a aprovação e rejeição de looks. O sistema **aprende** ajustando o `STATUS_USO` das peças e penalizando combinações reprovadas para garantir a variedade nas sugestões.

* **Arquitetura:** Projeto modular desenvolvido com Python/Streamlit (Frontend/Interface) e Pandas para manipulação do Banco de Dados (DB).

---

## ⚙️ Arquitetura e Estrutura
| Módulo | Tecnologia | Função no Projeto | 
| :--- | :--- | :--- | 
| **Frontend/Interface** | Streamlit | Interface intuitiva (Telas de Cadastro, Inventário e Sugestão). | 
| **Backend/Lógica** | Python (`motor_recomendacao.py`) | Implementa as **6 Regras IF/THEN** e o Algoritmo de Ranqueamento. | 
| **Banco de Dados** | CSV/Pandas | Armazena o inventário de peças e o histórico de uso (`STATUS_USO`). | 

## 📊 Fluxo Funcional (Ciclos)
O funcionamento do sistema segue dois ciclos principais, mapeados em Fluxogramas (Sprint 1):

1. **Ciclo 1: Cadastro de Peça (Input da IA):** Simulação da entrada de foto e confirmação de atributos. Os dados são salvos no DB.
2. **Ciclo 2: Geração de Look (Algoritmo):** Consulta o DB, executa as Regras IF/THEN, ranqueia, e recebe o Feedback do Usuário (Aprovar/Rejeitar) para refinar a próxima sugestão.

## 🛠️ Como Executar Localmente
Se você quiser rodar o projeto localmente (e não pela URL do Streamlit Cloud), siga os passos abaixo:

1. Clone o repositório: `git clone https://github.com/pedrohnh06/ia-guarda-roupa.git`
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o aplicativo: `streamlit run app.py`
