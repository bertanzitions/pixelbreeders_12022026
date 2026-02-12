# Requirements
You must have Docker installed

# How to install
docker-compose up --build

# Implementation plan + requirements

## Basic setup
● Technical Stack & Setup (check)
    ○ Frontend: React with TypeScript.
    ○ Backend: Python with Flask.
    ○ Database: Postgre
● External API
    ○ Test using Postman: The Movie Database (TMDB)
● Interface planning using Figma
● Model database


## Feature checklist
● Página Principal
    ○ Barra de pesquisa: Busca na API pública do TMDB
    ○ Listagem de resultados
    ○ Estados de loading
    ○ Interação: Ao clicar em um filme, abre um modal/página do filme
● Modal/Página do filme
    ○ Informações da API pública: sinopse, data de lançamento, lista de elenco
    ○ Avaliação
        ■ Se o filme não foi avaliado: o usuário pode dar uma nota
        ■ Se o filme já foi avaliado: a nota deve ser carregada e o usuário pode
        editar ou remover a nota

    ○ Botão de fechar/voltar para a página principal
● Página "Filmes Avaliados"
    ○ Listagem dos filmes que o usuário avaliou
    ○ Além de título/pôster, deve conter a nota do usuário
    ○ Interação: Ao clicar em um filme, abre um modal/página do filme