# Caderno de Notas do Apresentador (Roteiro Oral)
## Trabalho Prático 1: Qualidade de Vinhos
**Disciplina:** Tópicos em Estatística EST171 — Regressão para Dados Categóricos e Ordinais  
**Professor:** Cristiano de Carvalho Santos  
**Equipe:** João Nogueira, Kenzo Bontempo, Gabriel Bertolucci  

> **Diretriz do Enunciado**: Os slides da apresentação oficial são estritamente visuais e quantitativos (contendo exclusivamente fórmulas, gráficos e tabelas). **Nenhum texto descritivo de resultado deve aparecer nos slides**. Toda a interpretação substantiva, contextualização metodológica e respostas a arguições devem ser apresentadas **oralmente** a partir deste caderno de notas secundário.

---

## Divisão Sugerida de Apresentação (20 Minutos / ~6–7 min por integrante)

* **Parte 1 (João Nogueira — Slides 1 a 9)**: Introdução, problema de negócio/enológico, estrutura da base e análise exploratória de dados (EDA).
* **Parte 2 (Kenzo Bontempo — Slides 10 a 19)**: Formulação do modelo de chances proporcionais, seleção de variáveis ($m_3$), variável latente $Y^*$, probabilidades preditas, verificação das chances proporcionais (Brant e colapsos) e modelo parcial (VGAM).
* **Parte 3 (Gabriel Bertolucci — Slides 20 a 31)**: Dicotomização (90+ pontos) e custo de eficiência, ROC e Youden, resíduos substitutos dos dois modelos, $\text{OR} \times \text{RR}$, exemplo do Cabernet de R$ 60, armadilhas de interpretação e extensões bayesianas.

---

# Bloco 1: Dados e Análise Exploratória (João)

### Slide 1: Capa
* **Apresentação**: "Bom dia a todos, bom dia professor Cristiano. Nosso grupo vai apresentar a modelagem sensorial e hedônica da qualidade de vinhos, contrastando modelos de regressão ordinal policotômica com abordagens binárias."

### Slide 2: Abertura — Dados (código)
* **O que falar**: "Este é o preparo da base: filtramos vinhos sem preço ou país, criamos as 5 classes ordinais, a resposta binária de 90+ pontos, o log do preço, a região e a uva. Não vamos ler o código linha a linha; ele fica disponível para consulta."

### Slide 3: Wine Enthusiast Reviews
* **O que falar**:
  * "Partimos de um banco internacional de 129.971 avaliações da revista *Wine Enthusiast*."
  * "Após a filtragem de observações sem preço registrado e inconsistências de país, consolidamos uma amostra analítica com $N = 120.916$ vinhos."
  * "A variável resposta original é uma pontuação contínua de 80 a 100 pontos. Destacamos que 37,5% dos vinhos possuem nota $\ge 90$ pontos, o patamar consagrado pelo mercado como selo de excelência."

### Slide 4: Resposta Ordinal: Cinco Classes
* **O que falar**:
  * "Para estruturar a análise ordinal, particionamos a pontuação em 5 classes: Classe 1 (80 a 85), Classe 2 (86 e 87), Classe 3 (88 e 89), Classe 4 (90 e 91) e Classe 5 (92 a 100)."
  * "Como a pontuação é discreta e cheia de empates (87 e 88 concentram cerca de 13% da amostra cada), quintis exatos não existem: escolhemos os cortes que deixam cada classe o mais perto possível de 20% (entre 16,9% e 22,7%), evitando dados esparsos nas categorias extremas (Slide 2 da disciplina). Além disso, as Classes 4 e 5 coincidem exatamente com o patamar de 90+ pontos."

### Slide 5: Covariáveis
* **O que falar**:
  * "O preço em dólar apresenta uma assimetria brutal à direita, variando de US$ 4 a US$ 3.300. Por isso, adotamos a transformação logarítmica $\log(\text{preço})$, que lineariza a relação e reflete retornos marginais decrescentes."
  * "Agrupamos a origem geográfica em três blocos de *terroir*: Novo Mundo (liderado por EUA, Chile, Argentina e Austrália), Velho Mundo (tradição europeia: França, Itália, Espanha, Portugal, Alemanha e Áustria) e Outros."

### Slide 6: Vinhos por País
* **O que falar**:
  * "Aqui está a composição de cada região. Cada painel tem sua própria escala, porque os tamanhos são muito diferentes."
  * "O Novo Mundo (55,7%) é, na prática, os Estados Unidos: são 54.265 vinhos, cerca de 80% do grupo. O Velho Mundo (42,2%) é mais equilibrado, puxado por França e Itália."
  * "'Outros' tem só 2% da amostra, espalhados por 30 países. É um grupo heterogêneo, que mistura países de tradição europeia, como Grécia e Hungria, com países das Américas, como Canadá e Uruguai. Por isso, os coeficientes de 'Outros' devem ser lidos com cautela."

### Slide 7: Preço $\times$ Classe
* **O que falar**:
  * "A inspeção bivariada revela uma forte ordenação estocástica: a mediana de preço sobe progressivamente de US$ 15 na Classe 1 para US$ 52 na Classe 5."
  * "Entretanto, há uma grande sobreposição nas caudas — existem vinhos caros de nota baixa e pechinchas premiadas, justificando um modelo probabilístico em vez de determinístico."

### Slide 8: Vinhos com 90+ Pontos por País
* **O que falar**:
  * "No mapa global, países tradicionais do Velho Mundo e certos expoentes do Novo Mundo exibem mais de 40% a 50% de seus rótulos acima da barreira de 90 pontos."

### Slide 9: Uva $\times$ Classe
* **O que falar**:
  * "A terceira candidata a covariável é a uva (variedade). Há centenas de variedades na base, então guardamos as 5 mais frequentes (Pinot Noir, Chardonnay, Cabernet Sauvignon, Red Blend e Bordeaux-style Red Blend) e juntamos as demais em 'Outras', que ficam com 61% da amostra."
  * "Cada barra é a distribuição das 5 classes dentro de uma uva. O tracejado marca a média geral: quando a fronteira entre as Classes 3 e 4 de uma uva fica à esquerda dele, ela tem mais vinhos 90+ do que a média."
  * "O Pinot Noir lidera, com 52% de vinhos 90+, contra 34% em 'Outras'. Mas atenção: o Pinot Noir também é a uva mais cara (mediana de US$ 42, contra US$ 23 em 'Outras'). Boa parte dessa vantagem pode ser só preço, e é isso que a seleção de variáveis vai testar no Slide 12."

---

# Bloco 2: Modelo Ordinal e Chances Proporcionais (Kenzo)

### Slide 10: Abertura — Modelo ordinal (código)
* **O que falar**: "Os modelos ordinais foram ajustados com a função `polr`, do pacote MASS: quatro modelos encaixados, de $m_0$ a $m_3$, comparados por TRV, AIC e BIC. O escolhido foi o $m_3$, com preço, região e uva."

### Slide 11: Modelo de Chances Proporcionais (Formulação)
* **O que falar**:
  * "Poderíamos usar um modelo multinomial nominal com categoria de referência (Slide 2, p. 12), mas ele ignora que a Classe 5 é melhor que a Classe 4, que é melhor que a 3, e assim por diante. O modelo ordinal usa essa ordem a nosso favor e é bem mais econômico: cada covariável tem um único coeficiente, válido para todos os cortes. No nosso caso, com $J = 5$ classes e $p = 8$ efeitos (1 de preço, 2 de região e 5 de uva), são 8 coeficientes contra os $(J-1)p = 32$ do modelo nominal."
  * "Modelamos os logitos acumulados $P(Y \le j \mid \mathbf{x})$, com 4 interceptos $\alpha_1 < \dots < \alpha_4$ e um vetor único de coeficientes $\boldsymbol\beta$. O preditor soma o log do preço, duas indicadoras de região (referência: Novo Mundo) e cinco de uva (referência: 'Outras')."

### Slide 12: Seleção de Variáveis
* **O que falar**:
  * "Fizemos uma seleção para frente com modelos encaixados: cada modelo acrescenta um bloco ao anterior. $m_0$ só tem os 4 interceptos; $m_1$ acrescenta $\log(\text{preço})$; $m_2$, a região (2 indicadoras); e $m_3$, a uva (5 indicadoras). A coluna gl é o número de parâmetros."
  * "Cada passo é avaliado pelo TRV contra o anterior, por AIC e BIC, e pela redução de deviance em relação ao nulo."
  * "Todos os blocos são significativos, e o $m_3$ tem o menor AIC e o menor BIC. Por isso ficamos com ele."
  * "Uma ressalva honesta: com 121 mil vinhos, o ganho prático de cada bloco novo é pequeno. O preço sozinho explica 13,6% da deviance, a região acrescenta 0,2 ponto e a uva 0,1 ponto. Mas a uva muda a leitura da região: o OR do Velho Mundo cai de 1,32 no $m_2$ para 1,25 no $m_3$, porque parte do 'prêmio europeu' era, na verdade, composição de uvas."

### Slide 13: Modelo Ajustado ($m_3$)
* **O que falar**:
  * "O coeficiente do log-preço é $\hat\beta_1 = 2,184$ ($z = 204,8$). Como a variável está em log, o efeito de dobrar o preço é $2^{\hat\beta_1} \approx 4,54$ (IC 95%: 4,48 a 4,61): mantendo região e uva, dobrar o preço multiplica por 4,54 a chance de o vinho estar acima de qualquer corte."
  * "Região: o Velho Mundo tem OR = 1,25 e 'Outros países' OR = 1,18 em relação ao Novo Mundo, com preço e uva iguais. Esses valores são médias entre os cortes; no Slide 18 veremos que não são uniformes."
  * "Uva: todas as cinco têm OR abaixo de 1 em relação a 'Outras'. O Cabernet Sauvignon é o caso mais forte (OR = 0,66, chance 34% menor); Chardonnay e Pinot Noir ficam em 0,90. Isso contrasta com o Slide 9, onde o Pinot Noir liderava: as uvas famosas são mais caras, e, a preço igual, não pontuam mais do que as outras."

### Slide 14: Mecânica da Variável Latente $Y^*$ e Limiares
* **Ponto Central de Didática e Intuição (Slide 2 do professor, págs. 63 a 68 / Agresti, 2010)**:
  * "Com o $m_3$ ajustado, vejam na tela o que o modelo faz por dentro: a classe observada, de 1 a 5, vem de uma variável latente contínua $Y^* = \mathbf{x}^\top\boldsymbol\beta + \varepsilon$, com erro logístico padrão."
  * **Aponte para as linhas vermelhas tracejadas**: "Os quatro limiares estimados ($\hat\alpha_1 = 5,13$, $\hat\alpha_2 = 6,61$, $\hat\alpha_3 = 7,86$ e $\hat\alpha_4 = 9,34$) dividem a reta em cinco intervalos, um por classe. Eles são os mesmos nos dois painéis: não dependem do vinho."
  * **Aponte para a comparação entre os dois painéis** (os dois são vinhos do Novo Mundo, de uva 'Outras'; as porcentagens no topo são as áreas de cada classe):
    - "No painel de cima, um vinho de US$ 15 tem preditor 5,91, e a curva fica à esquerda. Dois terços da área caem abaixo de $\alpha_2$ (31% na Classe 1 e 35% na Classe 2), e só 12% passam de $\alpha_3$, ou seja, 90+ pontos."
    - "No painel de baixo, a US$ 80, o preditor sobe para 9,57. A curva é a mesma, só deslocada para a direita, com a mesma forma. É exatamente essa a hipótese de chances proporcionais. Agora 85% da área passa de $\alpha_3$ (29% na Classe 4 e 56% na Classe 5)."
  * **Propriedade de Agresti**: "Se o modelo latente vale, o $\boldsymbol\beta$ não depende de onde cortamos a escala: discretizar em 3 ou 7 classes estima o mesmo $\boldsymbol\beta$, e só os limiares mudam. Vimos isso na prática: ao trocar os quintis empíricos pelas classes atuais, o coeficiente do log-preço no $m_2$ quase não mudou (2,151 para 2,143)."

### Slide 15: Probabilidades Preditas
* **O que falar**:
  * "Para desenhar $\hat P(Y = j)$, precisamos fixar todas as covariáveis: o preço fica no eixo horizontal, cada painel é uma região, e a uva está fixada em 'Outras', a referência, que tem 61% da amostra."
  * "Os três painéis são quase iguais porque o efeito da região é pequeno perto do preço: ser do Velho Mundo equivale a um vinho cerca de 11% mais caro ($\exp(0,223/2,184) \approx 1,11$)."
  * "Notem a transição: abaixo de US$ 20 dominam as Classes 1 e 2; por volta de US$ 30 a Classe 3 atinge o pico (30%); entre US$ 40 e 50 lidera a Classe 4; e a partir de US$ 60 a Classe 5 assume a liderança."

### Slide 16: Abertura — Chances proporcionais (código)
* **O que falar**: "Agora verificamos a suposição central do modelo em três passos: o teste de Brant diz se há desvio; os colapsos binários mostram onde ele está; e o modelo parcial do VGAM o acomoda. Pacotes `brant`, `stats` e `VGAM`."

### Slide 17: Teste de Brant (Chances Proporcionais)
* **O que falar**:
  * "O teste de Brant tem como hipótese nula que cada coeficiente é o mesmo nos 4 logitos acumulados ($H_0: \boldsymbol\beta_1 = \dots = \boldsymbol\beta_4$)."
  * "O teste global rejeita com folga ($\chi^2 = 1.602,7$ com 24 gl, $p < 0,001$), e os oito testes por coeficiente também."
  * "Mas, com $N \approx 121$ mil, o teste rejeita até desvios pequenos. A rejeição diz que existe desvio, não onde está nem se importa. Os maiores $\chi^2$ são do Velho Mundo (530,8) e do preço (181,1), seguidos de Pinot Noir (143,8) e Chardonnay (120,3). No próximo slide vasculhamos cada coeficiente."

### Slide 18: Colapsamentos Binários Sucessivos
* **Como ler**:
  * "Ajustamos 4 regressões logísticas separadas, uma por corte ($Y > 1$ a $Y > 4$), com as mesmas covariáveis do $m_3$. Cada painel é um coeficiente. Os pontos são as estimativas por corte, as barras são o IC de 95%, e o tracejado é o coeficiente único do $m_3$, que também aparece no título. Se as chances fossem proporcionais, os 4 pontos cairiam sobre o tracejado."
  * "Atenção: cada painel tem sua própria escala vertical. Compare a distância até o tracejado com o tamanho das barras, e não a altura entre painéis."
* **O que observamos**:
  * "**Preço:** o efeito cresce de 2,09 para 2,42. Dobrar o preço multiplica a chance por 4,3 no corte mais baixo e por 5,4 no mais alto: o preço pesa mais para separar os excelentes. O desvio existe, mas é moderado, e o sinal e a ordem de grandeza não mudam."
  * "**Velho Mundo:** cai de 0,54 para 0,00. É um **efeito de piso**: dado o preço e a uva, o vinho europeu evita a Classe 1, mas não tem mais chance de chegar à Classe 5."
  * "**Outros países:** troca de sinal, de +0,43 para −0,55. Escapam da base, mas raramente chegam ao topo. Lembrando: é um grupo pequeno (2%) e heterogêneo, de 30 países (Slide 6)."
  * "**Uvas:** o Cabernet Sauvignon é o mais estável (entre −0,35 e −0,54), perto do tracejado. Chardonnay e Pinot Noir trocam de sinal (de −0,24 e −0,27 para +0,15 e +0,09): aparecem mais na base, mas no topo empatam com 'Outras' ou as superam. O Red Blend faz o contrário: nenhuma diferença na base e penalidade no topo (−0,46)."
* **Implicações**:
  1. "Para o preço, a suposição de chances proporcionais é uma aproximação aceitável."
  2. "Para região e uva, o OR único do $m_3$ é uma média que não descreve nenhum corte. Para o Velho Mundo, 1,25 exagera no topo; para Chardonnay e Pinot Noir, o sinal no topo sai até invertido."
  3. "Por isso, a rejeição do Brant não é só superpoder: para região e uva, o desvio muda a interpretação. É a situação que pede o modelo parcial."
  4. "Isso afeta o Bloco 3: o modelo binário de 90+ é o corte $Y > 3$, onde o Velho Mundo vale só 0,08. A dicotomização preserva o efeito do preço, não o da região."
* **Resumo**: "O preço age de forma quase proporcional em toda a escala. Região e uva não: o Velho Mundo protege contra notas baixas sem garantir notas altas, e algumas uvas mudam de lado entre a base e o topo. Por isso precisamos do modelo parcial."

### Slide 19: Chances Proporcionais Parciais (PPOM via VGAM)
* **O que falar**:
  * "No modelo parcial (Peterson & Harrell, 1990), ajustado com `vglm` do pacote VGAM, o preço mantém um coeficiente único (2,205), e região e uva ganham um coeficiente por corte."
  * "Na tabela de cima comparamos três versões. Soltar região e uva custa 21 parâmetros a mais (33 contra 12), melhora o ajuste (TRV = 1.414,0 com 21 gl, $p < 0,001$; AIC cai de 333.349 para 331.977) e não gera probabilidades negativas."
  * "Também testamos soltar o preço, e esse modelo falha. Com uma inclinação diferente por corte, as curvas acumuladas se cruzam nos vinhos caros: para 47 vinhos acima de cerca de US$ 685, o modelo dá $\hat P(Y = 4) < 0$. Com probabilidade negativa, a verossimilhança não existe, e o AIC fica indefinido. É um defeito conhecido dos modelos cumulativos não paralelos, e mais um motivo para manter o preço com efeito único."
  * "A tabela de baixo reproduz o que vimos nos colapsos: o Velho Mundo vai de 0,56 a 0,03, 'Outros países' de 0,41 a −0,50, e Chardonnay e Pinot Noir passam de negativos a +0,09 no último corte."

---

# Bloco 3: Modelo Binário, Diagnóstico e Conclusões (Gabriel)

### Slide 20: Abertura — Modelo binário (código)
* **O que falar**: "Aqui ajustamos o logito binário para 90+ pontos com `glm`, com as mesmas covariáveis do $m_3$, e comparamos a discriminação dele com a do modelo ordinal usando curvas ROC do pacote pROC."

### Slide 21: Dicotomização (90+ Pontos) e Custo de Eficiência
* **O que falar (Conexão Slide 1 e Slide 2 do professor)**:
  * "Dicotomizamos a resposta em $Y_{\text{bin}} = 1$ para 90+ pontos (Classes 4 e 5) e ajustamos uma regressão logística comum."
  * "Para o preço, os dois modelos concordam: $\hat\beta_{\text{bin}} = 2,24$ contra $\hat\beta_{\text{ord}} = 2,18$. O mesmo vale para o Cabernet (−0,48 contra −0,42)."
  * "Para a região, não: o Velho Mundo vale 0,08 no binário e 0,22 no ordinal. Isso é coerente com os colapsos: o binário mede o efeito só no corte de 90, e a coluna 'Parcial $\hat\beta_3$' mostra que o modelo parcial, nesse mesmo corte, dá 0,03. O ordinal faz uma média entre os cortes."
  * "Agora o custo: a última coluna, $\text{EP}^2_{\text{bin}}/\text{EP}^2_{\text{ord}}$, varia de 1,55 a 1,95. Ao dicotomizar, o analista precisaria de 55% a 95% mais vinhos para ter a mesma precisão. Em outras palavras, joga fora de 35% a 49% da informação dos dados."

### Slide 22: Discriminação e Calibração (ROC e Youden)
* **O que falar (Slide 1 do professor, págs. 79 a 88)**:
  * "Comparamos a discriminação da probabilidade do modelo binário com a de $P(Y \ge 4)$ tirada do modelo ordinal. Os dois alcançam $\text{AUC} = 0,814$: o ordinal não perde nada ao ser usado para a pergunta binária."
  * "Para transformar a probabilidade prevista em uma decisão (prever 90+ ou não), escolhemos um limiar $c$: o vinho é classificado como 90+ quando $\hat P \ge c$."
  * "**Sensibilidade** é a proporção de vinhos que de fato têm 90+ e que o modelo acerta: $P(\hat P \ge c \mid 90+)$. **Especificidade** é a proporção de vinhos abaixo de 90 que o modelo descarta corretamente: $P(\hat P < c \mid \text{abaixo de } 90)$. Subir o limiar ganha especificidade e perde sensibilidade; a curva ROC mostra essa troca para todos os limiares."
  * "O **índice de Youden** é $J = \text{sensibilidade} + \text{especificidade} - 1$, a distância vertical entre a curva ROC e a diagonal do acaso. O limiar de Youden é o que maximiza $J$, ou seja, o melhor equilíbrio entre os dois erros quando eles pesam igual."
  * "No nosso caso, o limiar ótimo é 0,336, com sensibilidade de 76,3% e especificidade de 70,8% ($J = 0,47$; é o ponto laranja no gráfico). Na prática: dos vinhos 90+, o modelo reconhece 3 em cada 4; dos vinhos abaixo de 90, 29% viram alarme falso. O limiar fica abaixo de 0,5 porque só 37,5% dos vinhos têm 90+."

### Slide 23: Abertura — Diagnóstico (código)
* **O que falar**: "Com os dois modelos ajustados, verificamos ambos com resíduos substitutos. Para o ordinal usamos o pacote `sure`; para o binário, que o `sure` não cobre, implementamos a mesma construção com $J = 2$ categorias. É o código na tela."

### Slide 24: Resíduos Substitutos: Ordinal (Liu & Zhang, 2018)

!!! Talvez tirar, não vamos saber mto bem explicar

* **A ideia em uma frase**: "Não observamos $Y^*$, só a classe. Então sorteamos um valor de $Y^*$ compatível com a classe observada, dentro do intervalo $(\hat\alpha_{j-1}, \hat\alpha_j)$, e subtraímos o preditor. Se o modelo estiver certo, esse resíduo se comporta como uma logística padrão, e dá para usar os gráficos de resíduo de sempre."
* **Por que não o resíduo comum**: "Com resposta ordinal, resíduos comuns são discretos e formam faixas paralelas que não dizem nada (Slide 3 do professor, p. 12-13)."
* **O que falar sobre cada painel** (amostra aleatória de 5.000 vinhos):
  1. **QQ**: "Os pontos seguem a reta teórica logística, então a ligação logito é adequada."
  2. **Resíduo × ajustado**: "Nuvem centrada em zero, sem funil. A curva vermelha só cai um pouco à direita, nos vinhos de preditor alto, onde há poucos dados."
  3. **Resíduo × log(preço)**: "Mesmo padrão: plana em quase todo o intervalo, com leve queda nos vinhos mais caros. É coerente com o que vimos nos colapsos, em que o efeito do preço cresce no topo, mas não pede um termo quadrático."
  4. **Resíduo × região e × uva**: "Caixas centradas em zero e com dispersão parecida: não sobra efeito médio de região nem de uva."

### Slide 25: Resíduos Substitutos: Binário
* **O que falar**:
  * "É a mesma construção com $J = 2$. No logito binário, $Y = 1$ quando $Y^* > 0$. Se o vinho é 90+, sorteamos $Y^*$ acima de zero; se não é, abaixo. O resíduo é o valor sorteado menos o preditor."
  * "Os painéis se leem como no slide anterior: o QQ segue a reta logística, e as nuvens e caixas ficam centradas em zero, sem tendência. O modelo binário também está bem especificado."

### Slide 26: Abertura — Conclusão (código)
* **O que falar**: "Para fechar, traduzimos o modelo em números concretos: probabilidade, chance, risco relativo e razão de chances. O código mostra o exemplo de um Cabernet de R$ 60."

### Slide 27: Razão de Chances ($\text{OR}$) $\times$ Risco Relativo ($\text{RR}$)
* **O que falar (Slide 1 do professor, págs. 19 a 26)**:
  * "A Razão de Chances só se aproxima do Risco Relativo quando o desfecho é raro ($\pi \to 0$). Como 37,5% da nossa base tem 90+ pontos, o desfecho **não é raro**, e $\text{OR} = \text{RR} \times \frac{1-\pi_0}{1-\pi_1}$."
  * "Para um vinho do Novo Mundo, de uva 'Outras', que passa de US$ 20 para US$ 40, a probabilidade de 90+ sobe de 21,2% para 55,8%. O Risco Relativo é $\text{RR} = 2,64$; a Razão de Chances é $\text{OR} = 4,71$. Chamar o OR de 'vezes mais probabilidade' exageraria o efeito em quase 80%."

### Slide 28: Exemplo: Cabernet Sauvignon de R$ 60
* **O que falar**:
  * "Um exemplo concreto: um Cabernet Sauvignon de R$ 60. Com o dólar a R$ 5,16 (fechamento de 30/09/2026), são cerca de US$ 11,60. Usamos o modelo ordinal $m_3$ e lemos 'nota maior que 90' como 90+, ou seja, Classes 4 e 5."
  * "Um Cabernet do Novo Mundo a esse preço tem só 5,1% de chance de 90+ (chance de 0,054). É a linha de referência."
  * "Cada linha abaixo muda uma coisa e mostra o OR contra a referência:"
    - "Pagar o dobro (R$ 120): a probabilidade vai a 19,7%, e o OR é 4,54, exatamente $2^{\hat\beta_1}$."
    - "Mesmo vinho do Velho Mundo: 6,3%, OR de 1,25, que é $\exp(\hat\beta_{\text{VM}})$."
    - "Mesmo vinho de 'Outros países': 6,0%, OR de 1,18. É aqui que o Brasil cai na nossa classificação: há 47 vinhos brasileiros na base, e o Brasil não está na lista do Novo Mundo."
    - "Outra uva, mesmo preço e região: 7,6%, OR de 1,52. O Cabernet é a uva com o maior 'desconto' a preço igual."
  * "No modelo de chances proporcionais, o OR entre dois vinhos é $\exp\{(\mathbf{x}_1 - \mathbf{x}_0)^\top\hat{\boldsymbol\beta}\}$ e é o mesmo para qualquer corte: vale para 90+ e também para 88+. Ressalva do Slide 18: para a região, esse OR é uma média. No corte de 90, o modelo parcial dá ao Velho Mundo um OR próximo de 1,03, e não 1,25."

### Slide 29: Frases Equivocadas (Armadilhas Interpretativas)
* **O que falar**:
  * "Compilamos quatro frases corriqueiras que reprovam em concursos e relatórios técnicos e que devem ser combatidas:"
    1. Confundir OR com RR ("tem 4,7 vezes mais probabilidade"; o certo é 2,6).
    2. Ler o OR como diferença de proporções ("8% a mais deles têm 90+ pontos").
    3. Tratar $\exp(\hat\beta)$ genericamente como risco relativo.
    4. Tratar a escala ordinal como quantitativa ("o vinho fica 4,5 vezes melhor").

### Slide 30: Abordagem Bayesiana
* **O que falar**:
  * "Como extensões futuras apontadas na literatura recente, a inferência Bayesiana oferece três grandes vantagens práticas:"
    1. *Prioris regularizadoras* (como Ridge/Normal) para uvas raras e pequenos produtores, prevenindo separação quase-completa via *shrinkage*.
    2. *Modelos hierárquicos com efeitos aleatórios* para modelar os avaliadores individuais (`taster_name`), isolando o rigor ou generosidade do crítico.
    3. Obtenção direta da distribuição posterior exata de quantidades não-lineares, como o Risco Relativo e probabilidades preditas por MCMC, sem depender de aproximações de primeira ordem (método Delta).

### Slide 31: Referências
* **O que falar**:
  * "Nossa base teórica ancora-se nos três grandes clássicos recomendados pelo professor: Alan Agresti (2010), o artigo seminal de Brant (1990) para o teste de paralelismo, Peterson & Harrell (1990) para o modelo parcial, e a metodologia de resíduos substitutos de Liu & Zhang (2018, JASA) e Greenwell et al. (2018, *The R Journal*). Muito obrigado, estamos abertos a perguntas da banca."

