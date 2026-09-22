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
