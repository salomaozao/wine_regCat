# wine_regCat 🍷

Trabalho Prático 1 da disciplina de **Regressão para Dados Categóricos e Ordinais** (UFMG).

O objetivo do projeto é a análise e modelagem estatística da pontuação e qualidade de vinhos utilizando modelos de regressão para dados ordinais (como modelos de chances proporcionais e extensões) e comparação com abordagens binárias/binomiais.

---

## 📁 Estrutura do Repositório

```text
wine_regCat/
├── data/
│   └── wine.csv           # Base de dados de vinhos (Wine Reviews)
├── docs/
│   ├── Trabalho1.pdf      # Instruções e diretrizes do Trabalho Prático 1
│   └── slides/            # Material de apoio e notas de aula (ignorado no git)
├── R/
│   └── wine.Rmd           # Análise descritiva, ajuste de modelos e diagnósticos
├── .gitignore             # Arquivos e diretórios ignorados pelo Git
└── README.md              # Apresentação do repositório
```

---

## 📦 Pacotes e Dependências (R)

O projeto utiliza os seguintes pacotes do ecossistema R:

- `pacman` (gerenciamento de pacotes)
- `here` (gerenciamento de diretórios e caminhos relativos)
- `rio` (importação e exportação de dados)
- `tidyverse` (`dplyr`, `ggplot2`, etc., para manipulação e visualização)
- `MASS` (modelo de chances proporcionais via `polr`)
- `VGAM` (modelos de chances proporcionais parciais e razão contínua via `vglm`)
- `brant` (teste de paralelismo de Brant)
- `car` (diagnósticos de regressão)
- `broom` (organização de saídas em `tibble`/`data.frame`)

Para instalar as dependências necessárias, execute no console do R:

```r
if (!require("pacman")) install.packages("pacman")
pacman::p_load(here, rio, MASS, VGAM, brant, car, broom, tidyverse)
```

---

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/salomaozao/wine_regCat.git
   cd wine_regCat
   ```
2. Abra o arquivo `R/wine.Rmd` no RStudio.
3. Execute os chunks de código ou renderize o documento (*Knit*) para gerar o relatório em HTML.
