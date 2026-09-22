---
id: DEC-01
titulo: Estrutura Metodológica e Teórica do TP1 (Qualidade de Vinhos)
modulo_afetado: [analise_descritiva, modelo_ordinal, modelo_binario, diagnosticos, apresentacao]
data_decisao: 2026-09-22
status: ativo
---

# DEC-01: Estrutura Metodológica e Teórica do TP1

## Contexto
O Trabalho Prático 1 da disciplina de Regressão para Dados Categóricos e Ordinais (UFMG) exige o ajuste de modelos ordinais, teste de proporcionalidade, colapsamento binário, diagnósticos com resíduos substitutos, contraste entre Razão de Chances (OR) e Risco Relativo (RR), e ganhos da abordagem Bayesiana, culminando em apresentação de 20 minutos com slides limpos (sem interpretação escrita nos slides).

## Decisão
1. **Variável Resposta**: A pontuação de vinhos (`points`) será analisada sob duas óticas:
   - Ordinal: 4 ou 5 classes de qualidade baseadas na escala enológica / quantis empíricos.
   - Binária: Dicotomização em $Y_{bin} = 1$ para $\ge 90$ pontos ("A barreira dos 90 pontos / Vinho Premium") e $Y_{bin} = 0$ para $< 90$ pontos.
2. **Covariáveis**:
   - `price`: Transformação em $\log(\text{price})$ para acomodar assimetria e retornos marginais decrescentes.
   - `country`: Agrupamento em Top 6 países produtores + "Outros", com contraste conceitual entre Velho Mundo e Novo Mundo.
   - `variety`: Agrupamento nas castas mais representativas para evitar esparsidade.
3. **Modelos**:
   - Modelo de Chances Proporcionais via `MASS::polr` e `VGAM::vglm`.
   - Modelo Parcial (PPOM) caso haja rejeição de paralelismo no teste de Brant / LRT.
   - Diagnósticos de resíduos substitutos via pacote `sure` (Liu & Zhang, 2017).
   - Regressão Logística Binária via `glm(family = binomial)` para comparação com o modelo ordinal.
4. **Apresentação**:
   - 15 slides para 20 minutos ($\approx 5$ slides por integrante).
   - Slides limpos: exclusivamente gráficos, fórmulas e tabelas, com interpretações estritamente orais.

## Consequências
- Alinhamento rigoroso com as instruções do trabalho e com os 3 conjuntos de slides do Prof. Cristiano Santos.
- Maior eficiência computacional e facilidade de apresentação oral pelo grupo.

