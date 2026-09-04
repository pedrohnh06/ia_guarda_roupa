# 👔 SmartWardrobe: Seu Estilista Pessoal com IA

O **SmartWardrobe** é uma aplicação completa (Frontend + Backend) que utiliza Inteligência Artificial baseada em regras de negócio para gerar recomendações inteligentes de looks. Ele considera o clima atual da sua cidade, o seu limiar de temperatura pessoal (sensação térmica) e regras avançadas de estilo e combinação de cores.

## 🚀 Tecnologias Utilizadas

**Frontend:**
- **[Streamlit](https://streamlit.io/)**: Interface premium e reativa, com injeção de CSS personalizado para uma experiência de luxo inspirada em grandes sites de moda.
- Arquitetura baseada em Sessão (Stateless API Client) com suporte a Token JWT.

**Backend:**
- **[FastAPI](https://fastapi.tiangolo.com/)**: Motor de alta performance para a API.
- **SQLAlchemy (SQLite)**: ORM robusto para o banco de dados (estruturado para facilitar futura migração para PostgreSQL).
- **JWT (JSON Web Tokens)**: Autenticação segura de usuários.
- Integração com a API de clima **wttr.in** em tempo real.

## ✨ Principais Funcionalidades

- **Autenticação e Sessão**: Criação de conta e login seguro. Cada usuário tem seu próprio guarda-roupa isolado no banco de dados.
- **Gerenciamento de Inventário (CRUD)**: Adicione, edite e exclua roupas informando Categoria, Cor, Estilo, Clima e anexando uma Foto (Upload local).
- **Motor de Recomendação Inteligente (IA)**: 
  - Gera um look completo cruzando **Superior + Inferior + Calçado + Cobertura**.
  - **Filtro de Temperatura Dinâmico**: Lê o clima atual da cidade do usuário e compara com o limiar configurado (ex: abaixo de 22ºC = Frio).
  - **Pontuação de Look**: Penaliza misturas de estampas, bonifica combinações de peças neutras e prioriza coerência de estilo.
- **Configurações Pessoais**: Ajuste dinâmico de limiar de temperatura.

## ⚙️ Estrutura do Projeto

O repositório foi modularizado nas seguintes pastas:

- \/frontend/\: Contém o \pp.py\ (Interface Streamlit) e o \pi_client.py\ (Responsável pelas chamadas HTTP para o backend).
- \/backend/\: Contém toda a infraestrutura FastAPI.
  - \/app/main.py\: Ponto de entrada da API.
  - \/app/clothes.py\ & \/app/auth.py\: Rotas (Endpoints).
  - \/app/services.py\: Cérebro da Inteligência Artificial de Combinação e consumo de API de tempo.
  - \/app/models.py\ & \/app/schemas.py\: Estrutura do Banco de Dados.

## 💻 Como Executar o Projeto Localmente

Você precisará iniciar o Backend e o Frontend separadamente.

### 1. Backend (FastAPI)
Abra um terminal, navegue até a pasta raiz do projeto e execute:
\\\ash
cd backend
uvicorn app.main:app --reload
\\\
A API estará rodando em \http://localhost:8000\. Você pode ver a documentação do Swagger acessando \http://localhost:8000/docs\.

### 2. Frontend (Streamlit)
Abra um segundo terminal, navegue até a pasta do projeto e execute:
\\\ash
cd frontend
streamlit run app.py
\\\
O aplicativo será aberto automaticamente no seu navegador (geralmente em \http://localhost:8501\).

## 🛡️ Git e Versionamento
O projeto conta com um \.gitignore\ configurado para evitar envios acidentais de arquivos sensíveis como:
- O banco de dados SQLite local (\*.db\)
- A pasta de uploads de imagens dos usuários
- O ambiente virtual Python (\.venv\) e arquivos de cache.
