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
- Billboars
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

### Pegar dados do Spotify

1. Copiar arquivo [end.example.json](env.example.json) para `env.json`
2. Atualizar os dados do JSON
   1. Colocar sua chave da API do Spotify ([instruções](https://developer.spotify.com/documentation/web-api/quick-start/))
3. Rodar o script 
