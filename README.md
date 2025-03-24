# Chatbot

Este projeto consiste em um chatbot construído em Python e utiliza Docker Compose para facilitar a configuração e execução do ambiente.

## Pré-requisitos

Antes de começar, certifique-se de que você tem o Docker e o Docker Compose instalados em sua máquina. Você pode encontrar instruções de instalação nos links abaixo:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Como Executar o Chatbot com Docker Compose

Siga os passos abaixo para executar o chatbot usando Docker Compose:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/mateushlsilva/chatbot-fastfood.git
    cd chatbot-fastfood
    ```
2.  **Execute o Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    * Este comando irá construir as imagens Docker e iniciar os containers definidos no arquivo `docker-compose.yml`.

3.  **Acesse o Chatbot:**

    * Após a inicialização dos containers, o chatbot estará disponível em `http://localhost:8000` (ou na porta definida no arquivo `docker-compose.yml`).
