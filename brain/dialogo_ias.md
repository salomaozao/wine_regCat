# Diálogo e Memória Compartilhada entre IAs e Desenvolvedores

Este arquivo registra cronologicamente todas as sessões de trabalho, contexto, decisões tomadas, arquivos alterados e direcionamentos de handoff no projeto **wine_regCat**.

---

## 2026-09-22 19:10 — feat(planejamento): estruturação do plano analítico e criação da memória .brain

**Autor:** Antigravity / Gemini 3.8 Flash (High) · operador: Gabriel Nascimento

**Contexto:** Solicitação do usuário para elaborar um olhar analítico aprofundado e um plano de implementação para o TP1 da disciplina de Regressão para Dados Categóricos e Ordinais (UFMG - Prof. Cristiano de Carvalho Santos), com fundamentação teórica conectada aos slides da disciplina, divisão dos tópicos da apresentação de 20 minutos entre os 3 integrantes, e criação da pasta de governança `.brain/`.

**Feito:**
- Leitura e extração dos 3 conjuntos de slides da disciplina em `docs/slides/` e das diretrizes do trabalho em `docs/Trabalho1.pdf`.
- Elaboração do plano analítico e metodológico completo em [plano_implementacao.md](plano_implementacao.md).
- Criação da arquitetura canônica da pasta `.brain/`:
  - `README.md`: guia de governança.
  - `plano_implementacao.md`: cópia completa do plano analítico.
  - `decisoes/01_modelagem_tp1_vinhos.md`: DEC-01.
  - `pendencias/01_definicao_cortes_ordinais.md`: PEND-01.
  - `scripts/manage_brain.py`: script CLI de sincronização e auditoria.
  - `dialogo_ias.md`: este registro de sessão.

**Decisões:**
- [DEC-01](decisoes/01_modelagem_tp1_vinhos.md): Adoção do modelo de chances proporcionais via `polr`/`vglm`, com fallback para modelo parcial (PPOM), dicotomização em $\ge 90$ pontos, e respeito à regra estrita de slides limpos (apenas gráficos, tabelas e fórmulas, sem interpretação em texto).

**Pendente / atenção:**
- [PEND-01](pendencias/01_definicao_cortes_ordinais.md): Confirmação dos pontos de corte exatos da resposta ordinal e tamanho da amostra para diagnósticos do pacote `sure`.

**Próxima IA / Handoff:**
- Após o alinhamento com o usuário, iniciar a implementação das rotinas no arquivo `R/wine.Rmd`:
  1. Instalação do pacote `sure` e dependências caso necessário.
  2. Implementação do pipeline de dados com $\log(\text{price})$ e categorização ordinal/binária.
  3. Ajuste do modelo `MASS::polr` e teste de Brant.
  4. Ajuste do modelo `VGAM::vglm` com opções paralela e não-paralela.
  5. Geração dos diagnósticos com resíduos substitutos via `sure::autoplot`.
  6. Ajuste do modelo binomial logístico e comparação de parâmetros.

---

## 2026-09-22 19:15 — feat(eda): integração do shapefile global, auditoria de países e mapa coroplético de qualidade

**Autor:** Antigravity / Gemini 3.8 Flash (High) · operador: Gabriel Nascimento

**Contexto:** Solicitação do usuário para vincular a coluna geográfica com a malha espacial, auditar o casamento exato de nomes (como United States vs US) e refinar visualmente o mapa coroplético de qualidade de vinhos no R Markdown.

**Feito:**
- Auditoria minuciosa da base `wine.csv` contra as 256 feições do Shapefile (`data/world-administrative-boundaries`):
  - Identificada discrepância em nomes oficiais do shapefile: `US` -> `United States of America`, `England` -> `U.K. of Great Britain and Northern Ireland`, `Moldova` -> `Moldova, Republic of`, `Macedonia` -> `The former Yugoslav Republic of Macedonia`, `Bosnia and Herzegovina` -> `Bosnia & Herzegovina`, `South Korea` -> `Republic of Korea`.
  - Construído dicionário explícito de correspondência (`de_para_paises`), atingindo 100% de match para os 47 países com produção de vinho.
- Substituídas as linhas de teste preliminar em `R/wine.Rmd` pelo chunk `EDA-mapa-qualidade` contendo:
  - Carregamento limpo com `sf::st_read(here("data", "world-administrative-boundaries"))`.
  - Cruzamento de dados (`left_join`) com a qualidade média por país (`as.numeric(points)`).
  - Remoção da feição da Antártica e reprojeção para Projeção Robinson (`+proj=robin`), eliminando distorções das projeções planas.
  - Paleta enológica contínua customizada (Champagne `#F5EBE6` a Tinto Profundo `#4A0E17`), com países sem registros em cinza claro neutro (`#ECECED`).
  - Barra de cor estilizada e tipografia alinhada ao padrão visual do relatório.
- Atualizado `.gitignore` para ignorar zips, kmls e arquivos pesados/redundantes.

**Decisões:**
- Adoção da projeção Robinson para o mapa-múndi no relatório, conferindo aspecto visual profissional e proporções continentais equilibradas.
- Agregação no nível de país (`country`), preservando a integridade estatística global do trabalho.

**Pendente / atenção:**
- Caso o grupo deseje no futuro mapear condados/estados específicos (como Washington e Oregon da referência inicial), obter a malha específica via pacote `tigris`.
- Próximo passo analítico: Verificação da suposição de chances proporcionais (chunk `validate-assumptions`) e ajuste ordinal.

**Próxima IA / Handoff:**
- O mapa de distribuição espacial está 100% integrado, validado e renderizando sem erros no Rmd.
- Prosseguir com a verificação de chances proporcionais (teste de Brant / LRT) e ajuste do modelo ordinal nos chunks subsequentes de `R/wine.Rmd`.

---

## 2026-09-25 18:35 — docs(planejamento): reestruturacao do PI espelhando secoes do wine.qmd e resolucao da divergencia na 3.2.2

**Autor:** Antigravity / Gemini 3.8 Flash (High) · operador: Gabriel Nascimento

**Contexto:** O usuario solicitou que o Plano de Implementacao (PI) fosse totalmente reformulado para funcionar como um caderno teorico e exploratorio para ele mesmo implementar no R, espelhando fielmente os capitulos e secoes do arquivo wine.qmd, com foco teorico rigoroso e esclarecimento detalhado sobre a divergencia conceitual entre a secao 3.2.2 (ajuste binario) e 3.1 (ajuste ordinal).

**Feito:**
- Reestruturacao completa de rain/plano_implementacao.md espelhando a arvore de capitulos e secoes do wine.qmd:
  - Capitulo 1: Introducao, tratamento de variaveis no get-data e justificativa das hipoteses $ a $.
  - Capitulo 2: Pressupostos ordinais, geometria de retas paralelas, teste de Brant, LR test no VGAM e paradoxo de $ grande ( = 120.975$).
  - Capitulo 3: Modelagem em 3 frentes:
    - 3.1: Regressao ordinal acumulada (polr), selecao e diagnosticos de residuos substitutos (sure).
    - 3.2: Regressao binaria dicotomizada (glm(family = binomial)), diagnosticos e desempenho discriminatorio (ROC / AUC via pROC).
    - 3.3: Modelo Parcial (PPOM via glm(parallel = FALSE ~ log_price)), resolvendo o modelo misterioso.
    - 3.4: Tabela comparativa e integradora (compare_fits).
  - Capitulo 4: Resultados finais, deducao analitica do fator de disparidade entre OR e RR em eventos frequentes com frases equivocadas, e fundamentacao formal dos ganhos da abordagem Bayesiana.
- Resolucao teorica da divergencia na secao 3.2.2: demonstrado que o codigo atual continha uma duplicacao equivocada de glm(cumulative) da 3.1, e que a dicotomizacao exige glm(family = binomial), com explicacao aprofundada sobre a perda de eficiencia estatistica e a concordancia esperada dos betas pela variavel latente ^*$.
- Instalacao e validacao dos pacotes sure e pROC no ambiente R.
- Auditoria e sincronizacao da governanca .brain via manage_brain.py.

**Decisões:**
- Preservar o codigo em R/wine.qmd sem alteracoes diretas conforme pedido do usuario, deixando o aluno como operador ativo da implementacao.
- Adocao do PPOM na secao 3.3.2 como solucao metodologica canonica para a quebra de proporcionalidade.

**Pendente / atenção:**
- O aluno executara a implementacao bloco a bloco no R/wine.qmd seguindo o gabarito e instrucoes do PI.

**Próxima IA / Handoff:**
- Prestar suporte analitico caso o aluno tenha duvidas durante a escrita dos chunks ou quando iniciar a estruturacao dos 15 slides limpos da apresentacao.

---

## 2026-09-27 13:20 — docs(wine.qmd): inclusao dos textos teoricos e fundamentacao estatistica completa sem alteracao dos blocos de codigo

**Autor:** Antigravity / Gemini 3.8 Flash (High) · operador: Gabriel Nascimento

**Contexto:** O usuario solicitou a insercao dos textos formais e da fundamentacao estatistica rigorosa diretamente no documento wine.qmd, explicando a razao de cada modelo e tecnica adotada (modelo ordinal de logitos acumulados, derivacao por variavel latente, suposicao de chances proporcionais, testes de Brant e LRT, efeito do N grande, modelo de chances proporcionais parciais - PPOM, custos de eficiencia da dicotomizacao binaria, residuos substitutos do pacote sure, deducao formal de OR vs RR com tabela de falacias conceituais e justificativa da abordagem bayesiana), com a instrucao expressa de nao alterar nenhum bloco de codigo existente.

**Feito:**
- Insercao e expansao dos textos conceituais e teorico-metodologicos em todos os capitulos do arquivo TP1/R/wine.qmd:
  - Capitulo 1 (EDA): Contextualizacao hedônica de vinhos, natureza ordinal sensorial das avaliacoes, assimetria severa do preco e justificativa matematica/economica de log(price) por retornos marginais decrescentes; dimensao espacial e heterogeneidade de terroir (Velho Mundo vs. Novo Mundo).
  - Capitulo 2 (Pressupostos): Formulacao matematica dos logitos acumulados, derivacao formal via variavel latente continua Y*, geometria do paralelismo, convencao de sinal de Agresti (OR_{>j} = exp(beta)), procedimentos de diagnostico (Brant e LRT) e discussao aprofundada sobre a inflacao de poder em amostras massivas (N ≈ 120.000).
  - Capitulo 3 (Modelagem):
    - 3.1 Ordinal: Criterios formais de selecao aninhada (TRV, AIC, BIC), interpretacao probabilistica dos limiares e coeficientes, e fundamentacao teorica dos Residuos Substitutos (Surrogate Residuals de Liu & Zhang, 2017 via sure) superando as bandas discretas dos residuos convencionais.
    - 3.2 Binario Dicotomizado: Definicao da barreira comercial dos 90 pontos (Y_bin), trade-off teorico entre simplificacao e perda de eficiencia estatistica (descarte de variabilidade interna e inflacao de variancia amostral), concordancia latente e avaliacao preditiva por curva ROC e AUC.
    - 3.3 PPOM: Fundamentacao do Modelo de Chances Proporcionais Parciais como solucao canonica contra o risco de probabilidades negativas e hiperparametrizacao do modelo irrestrito, relaxando o paralelismo exclusivamente para log(price).
    - 3.4 Sintese Comparativa: Confronto metodologico dos tres modelos e avaliacao da estabilidade parametrica latente.
  - Capitulo 4 (Conclusoes e Extensoes):
    - Deducao algebrica detalhada da relacao OR = RR * (1-pi0)/(1-pi1), comprovacao de que o evento nao e raro (≈ 37,5% de vinhos >= 90 pts) e que o OR inflaciona severamente a percepcao de efeito em relacao ao RR, acompanhado de tabela de frases equivocadas frequentes na literatura e correcoes conceituais.
    - Fundamentacao formal dos tres ganhos da abordagem Bayesiana (priors regularizadoras contra quase-separacao completa, modelagem hierarquica multinivel natural por vinicola/terroir/pais, e inferencia exata de credibilidade HPD via MCMC sem aproximacoes de Wald).
- Auditoria de integridade: 100% dos 17 blocos de codigo (`{r ...} ... `) foram rigorosamente preservados intactos.

**Decisões:**
- Preservar rigorosamente a integridade dos blocos de codigo e focar exclusivamente no aprofundamento textual de nivel de pos-graduacao em estatistica.

**Próxima IA / Handoff:**
- O arquivo TP1/R/wine.qmd esta completamente embasado teoricamente. O grupo pode agora focar na execucao dos chunks e no desenho dos 15 slides limpos da apresentacao de 20 minutos.

---

## 2026-09-27 21:48 — feat(eda): inclusao de analise univariada descritiva e ajuste de caminhos no wine.qmd

**Autor:** Antigravity / Gemini 3.8 Flash (High) · operador: Gabriel Nascimento

**Contexto:** O usuario solicitou novo commit ('novamente') apos adicionar analises univariadas completas da resposta e covariáveis no arquivo wine.qmd.

**Feito:**
- Inclusao do chunk EDA-univariadas em R/wine.qmd com distribuicao de pontos contínuos (p_pts), classes ordinais categorizadas (p_classes), preco em escala logarítmica com contagem de missings (p_price) e funcao modular plot_top() para exploracao das covariáveis categoricas mais frequentes (country, ariety e 	aster_name).
- Configuracao explicita de 
oot.dir no knitr para garantir reproducibilidade de caminhos relativos no RStudio.
- Atualizacao do .gitignore para ignorar .vdoc*, .here e Rplots.pdf.

**Decisões:**
- Manter o historico limpo e com governanca atualizada via .brain/.
