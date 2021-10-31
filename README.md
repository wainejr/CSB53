# Grammy: fatores determinantes para indicação de melhor álbum do ano

## Equipe: Donda

## Descrição:

Analisar os fatores determinantes para indicação de melhor álbum no Grammy Awards.

### Motivação
É muito comum ouvir críticas acerca do Grammy e suas indicações para melhor música e álbum do ano, alegando que os álbuns são indicados não pela qualidade, mas sim porque foram populares ou sucesso de vendas. 
Uma análise criteriosa dos dados de álbuns, como nota da crítica, número de vendas/ouvintes do álbum, deve ajudar a checar os argumentos dessa discussão e seu respaldo na realidade.

### Objetivos
- Definir métricas para popularidade e qualidade/relevância de um álbum
- Definição dos dados a serem coletados (relacionados às métricas)
- Coleta de dados dos álbuns de cada ano (álbuns indicados e de maior relevância)
- Construção do modelo para análise dos dados
- Definir modo de apresentação e visualização dos dados
- Concluir sobre os resultados obtidos

### Fontes de dados
- Kaggle
- Billboard
- Metacritic
- LastFM
- Fontes alternativas p/ retirar dados à mão

### Desafios
- Definição das métricas de qualidade e popularidade de um álbum
- Coleta dos dados
- Visualização dos dados

## Membros:

Waine Barbosa de Oliveira Junior, 1905120, jr_waine, waine@alunos.utfpr.edu.br, Eng. Comp., UTFPR

Eduardo Yoshio da Rocha, 1508733, eduardo2798, eduardo.yoshio@outlook.com, Eng. Comp., UTFPR


## Estrutura de pastas

### Pastas com código:
- `grammy`: código comum para vários scripts e notebooks
- `scripts`: pasta com scripts para serem rodados, usualmente para download de páginas web, scrapping ou tratamento de dados
- `notebooks`: Jupyter notebooks, utilizados para visualização de dados.

### Pastas com dados
- `downloads`: Páginas webs baixadas para scrapping
- `data`: dados obtidos para processamento, seja por salvamento manual ou por scrapping

## Instruções

### Obter melhores álbuns do ano do metacritic

Rodar os seguintes comandos (a partir da pasta raiz do projeto)

```bash
# Script para baixar as páginas de melhores álbuns
python -m scripts.metacritic_best_albums_download
# Script para extrair os melhores álbuns das páginas baixados
python -m scripts.metacritic_best_albums_extract
```

### Obter melhores álbuns do ano da Billboard

Rodar os seguintes comandos (a partir da pasta raiz do projeto)

```bash
# Script para baixar as páginas de melhores álbuns
python -m scripts.billboard_best_albums_download
# Script para extrair os álbuns das páginas baixados
python -m scripts.billboard_best_albums_extract
```

### Obter dados dos álbuns do Grammy no Metacritic

Rodar os seguintes comandos (a partir da pasta raiz do projeto)

```bash
# Script para gerar as urls para baixar
python -m scripts.grammy_albums_metacritic_save_url
```

Após isso, o arquivo gerado (`data/metacritic/grammies_url.csv`) deve  movido para `data/metacritic/grammies_url_treated.csv` e então deve ser tratado, corrigindo as URLs erradas.

```bash
# Script para baixar as páginas dos álbuns
python -m scripts.grammy_albums_metacritic_download
# Script para extrair os dados das páginas
python -m scripts.grammy_albums_metacritic_extract
```

### Obter dados do Spotify

1. Copiar arquivo [end.example.json](env.example.json) para `env.json`
2. Atualizar os dados do JSON
   1. Colocar sua chave da API do Spotify ([instruções](https://developer.spotify.com/documentation/web-api/quick-start/))
3. Rodar o script ...

TODO