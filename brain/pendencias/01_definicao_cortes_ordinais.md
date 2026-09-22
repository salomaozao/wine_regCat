---
id: PEND-01
titulo: Alinhamento final sobre os pontos de corte da resposta ordinal e subamostragem do sure
modulo_afetado: [dados, modelo_ordinal, diagnosticos]
criticidade: media
status: aberto
responsavel: Grupo
data_resolucao: ""
---

# PEND-01: Definição dos Cortes da Resposta Ordinal e Amostragem dos Resíduos

## Descrição
Definir se a resposta ordinal adotará:
1. *Opção A*: 4 categorias enológicas de mercado: Regular (80-84), Bom/Muito Bom (85-87), Excelente (88-91) e Superior/Excepcional (92-100).
2. *Opção B*: Quantis empíricos de 5 classes ($K=5$). [VAMOS LEVAR ESTE]

Além disso, validar se os gráficos de resíduos substitutos com `sure` utilizarão uma amostra estratificada ($n = 5.000$ a $10.000$) para viabilizar as simulações estocásticas de Monte Carlo ($nsim = 100$).

