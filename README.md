🧠 IA Guarda-Roupa: Seu Estilista Pessoal

Este projeto foi desenvolvido como parte do componente curricular UC HUB e visa utilizar inteligência artificial (IA) baseada em regras de negócio para auxiliar o usuário na escolha de looks, otimizando o uso do guarda-roupa e incorporando o contexto de temperatura e histórico de uso.

O aplicativo é construído em Python, utilizando a biblioteca Streamlit para a interface web e Pandas para o motor de dados (simulando um banco de dados via CSV).

🔗 Acesse a Aplicação Online (Streamlit Cloud)

Você pode acessar a versão mais recente do aplicativo diretamente, sem precisar instalar nada, através do link de deploy:

https://iaguardaroupa-ko9lyvj2fmhfhuxvljddbf.streamlit.app/

Para usar:

Baixe o arquivo roupas.csv de exemplo deste repositório.

Acesse o link acima.

Carregue o roupas.csv na barra lateral para iniciar o inventário e a IA.

✨ Funcionalidades Principais

Motor de Recomendação Inteligente (4 Peças): Gera looks completos (Superior, Inferior, Calçado e Cobertura) baseado em regras de estilo, cor e compatibilidade de peças.

Filtro de Temperatura Dinâmico (NOVO): Permite ao usuário selecionar "Frio" ou "Calor", ativando um filtro que garante que apenas peças adequadas e neutras sejam consideradas. Inclui automaticamente peças de Cobertura (Casacos/Blazers) no filtro "Frio".

Aprendizado Contínuo (Feedback Loop): O usuário pode Aprovar ou Rejeitar os looks sugeridos.

Aprovação: Diminui a penalidade de uso das peças.

Rejeição: Aumenta a penalidade de uso das peças e remove o look do histórico de sugestões da sessão.

Gerenciamento de Inventário: Permite carregar um arquivo CSV como base de dados e cadastrar novas peças dinamicamente.

🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para rodar a aplicação em seu ambiente local.

Pré-requisitos

Você precisa ter o Python (versão 3.8+) instalado em seu sistema.

Instale as bibliotecas necessárias:

pip install -r requirements.txt


Estrutura de Arquivos

Certifique-se de ter os seguintes arquivos no mesmo diretório:

app.py (Interface do Streamlit)

motor_recomendacao.py (Lógica da IA)

roupas.csv (Base de Dados Inicial)

requirements.txt (Lista de dependências)

Inicialização

Abra o terminal ou prompt de comando no diretório do projeto.

Execute o comando:

streamlit run app.py


O aplicativo será aberto automaticamente no seu navegador (geralmente em http://localhost:8501).
