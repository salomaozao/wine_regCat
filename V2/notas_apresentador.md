# Caderno de Notas do Apresentador (Roteiro Oral)
## Trabalho Prático 1: Qualidade de Vinhos
**Disciplina:** Tópicos em Estatística EST171 — Regressão para Dados Categóricos e Ordinais  
**Professor:** Cristiano de Carvalho Santos  
**Equipe:** João Nogueira, Kenzo Bontempo, Gabriel Bertolucci  

> **Diretriz do Enunciado**: Os slides da apresentação oficial são estritamente visuais e quantitativos (contendo exclusivamente fórmulas, gráficos e tabelas). **Nenhum texto descritivo de resultado deve aparecer nos slides**. Toda a interpretação substantiva, contextualização metodológica e respostas a arguições devem ser apresentadas **oralmente** a partir deste caderno de notas secundário.

---

## Divisão Sugerida de Apresentação (20 Minutos / ~6–7 min por integrante)

* **Parte 1 (João Nogueira — Slides 1 a 6)**: Introdução, problema de negócio/enológico, estrutura da base e análise exploratória de dados (EDA).
* **Parte 2 (Kenzo Bontempo — Slides 7 a 15)**: Formulação do modelo de chances proporcionais, mecânica gráfica da variável latente $Y^*$, ajuste do modelo, probabilidades preditas, diagnóstico de paralelismo (Brant e colapsos), modelo parcial (PPOM) e diagnóstico com resíduos substitutos (Liu & Zhang, 2018 / Slide 3 do professor).
* **Parte 3 (Gabriel Bertolucci — Slides 16 a 21)**: Dicotomização comercial (90+ pontos), custo da perda de eficiência estatística ($\text{EP}^2_{\text{bin}}/\text{EP}^2_{\text{ord}}$), curvas ROC e índice de Youden, distinção formal $\text{OR} \times \text{RR}$, armadilhas de interpretação e extensões Bayesianas.

---

# Bloco 1: Dados e Análise Exploratória (João)

### Slide 1: Capa
* **Apresentação**: "Bom dia a todos, bom dia professor Cristiano. Nosso grupo vai apresentar a modelagem sensorial e hedônica da qualidade de vinhos, contrastando modelos de regressão ordinal policotômica com abordagens binárias."

### Slide 2: Wine Enthusiast Reviews
* **O que falar**:
  * "Partimos de um banco internacional de 129.971 avaliações da revista *Wine Enthusiast*."
  * "Após a filtragem de observações sem preço registrado e inconsistências de país, consolidamos uma amostra analítica com $N = 120.916$ vinhos."
  * "A variável resposta original é uma pontuação contínua de 80 a 100 pontos. Destacamos que 37,5% dos vinhos possuem nota $\ge 90$ pontos, o patamar consagrado pelo mercado como selo de excelência."

### Slide 3: Resposta Ordinal: Quintis Empíricos
* **O que falar**:
  * "Para estruturar a análise ordinal, particionamos a pontuação em 5 classes balanceadas baseadas em quantis empíricos: Classe 1 (80 a 86), Classe 2 (87 e 88), Classe 3 (89), Classe 4 (90 e 91) e Classe 5 (92 a 100)."
  * "Dessa forma, cada classe detém aproximadamente 20% da amostra, evitando o problema de dados esparsos em categorias extremas discutido no Slide 2 da disciplina."

### Slide 4: Covariáveis
* **O que falar**:
  * "O preço em dólar apresenta uma assimetria brutal à direita, variando de US$ 4 a US$ 3.300. Por isso, adotamos a transformação logarítmica $\log(\text{preço})$, que lineariza a relação e reflete retornos marginais decrescentes."
  * "Agrupamos a origem geográfica em três blocos de *terroir*: Novo Mundo (liderado por EUA, Chile, Argentina e Austrália), Velho Mundo (tradição europeia: França, Itália, Espanha, Portugal, Alemanha e Áustria) e Outros."

### Slide 5: Preço $\times$ Classe
* **O que falar**:
  * "A inspeção bivariada revela uma forte ordenação estocástica: a mediana de preço sobe progressivamente de US$ 15 na Classe 1 para US$ 65 na Classe 5."
  * "Entretanto, há uma grande sobreposição nas caudas — existem vinhos caros de nota baixa e pechinchas premiadas, justificando um modelo probabilístico em vez de determinístico."

### Slide 6: Vinhos com 90+ Pontos por País
* **O que falar**:
  * "No mapa global, países tradicionais do Velho Mundo e certos expoentes do Novo Mundo exibem mais de 40% a 50% de seus rótulos acima da barreira de 90 pontos."

---

# Bloco 2: Modelo Ordinal, Variável Latente e Diagnósticos (Kenzo)

### Slide 7: Modelo de Chances Proporcionais (Formulação)
* **O que falar**:
  * "Por que adotar um modelo ordinal em vez de um modelo multinomial nominal de categoria de referência (Slide 2, p. 12)? Porque a modelagem ordinal é parcimoniosa: consome apenas $p$ parâmetros de efeito para as covariáveis, enquanto a nominal gastaria $(J-1)p$, além de respeitar a ordenação natural da escala."
  * "Modelamos os logitos acumulados $P(Y \le j \mid \mathbf{x})$, com 4 interceptos $\alpha_1 < \dots < \alpha_4$ e um vetor único de coeficientes $\boldsymbol\beta$."

### Slide 8: Mecânica da Variável Latente $Y^*$ e Limiares
* **Ponto Central de Didática e Intuição (Slide 2 do professor, págs. 63 a 68 / Agresti, 2010)**:
  * "Vejam na tela a intuição visual do que o modelo realmente faz: assumimos que a pontuação discreta de 1 a 5 decorre de uma variável latente contínua inobservada $Y^* = \mathbf{x}^\top\boldsymbol\beta + \varepsilon$, onde o erro $\varepsilon$ segue distribuição logística padrão."
  * **Aponte para as linhas vermelhas**: "Os quatro pontos de corte estimados pelo modelo ($\hat\alpha_1 = 5,84$, $\hat\alpha_2 = 7,32$, $\hat\alpha_3 = 7,85$ e $\hat\alpha_4 = 9,32$) particionam a reta real em cinco intervalos disjuntos. Esses limiares são fixos e não mudam com o preço ou a região."
  * **Aponte para a comparação entre os dois painéis**:
    - "No painel de cima, para um vinho popular de US$ 15, o preditor linear $\mathbf{x}^\top\boldsymbol\beta$ desloca a curva para a esquerda. A quase totalidade da área sob a curva fica concentrada abaixo de $\alpha_2$, resultando em alta probabilidade de Classes 1 e 2."
    - "No painel de baixo, quando o vinho custa US$ 80, o preditor linear 'empurra' a densidade inteira para a direita por translação pura, mantendo idêntica a sua dispersão e forma (é exatamente essa a hipótese de paralelismo!). Agora, quase toda a massa de probabilidade ultrapassa $\alpha_3$ e $\alpha_4$, caindo nas Classes 4 e 5 ($\ge 90$ pontos)."
  * **Propriedade de Agresti**: "Como demonstrado nos slides da disciplina, os parâmetros $\boldsymbol\beta$ são invariantes à escolha dos cortes: se tivéssemos discretizado em 3 ou 7 classes, os $\beta$ seriam rigorosamente os mesmos, mudando apenas os limiares $\alpha$."

### Slide 9: Seleção de Variáveis
* **O que falar**:
  * "Comparamos os modelos $m_0$ (nulo), $m_1$ (apenas preço), $m_2$ (+ região) e $m_3$ (+ casta da uva)."
  * "O modelo $m_2$ reduz 14,1% da deviance inicial com apenas 7 graus de liberdade, apresentando o melhor balanço de parcimônia por BIC antes que o acréscimo de dezenas de uvas esparsas sobrecarregue o modelo."

### Slide 10: Modelo Ajustado ($m_2$)
* **O que falar**:
  * "O coeficiente do log-preço é $\hat\beta_1 = 2,151$ ($z = 204,9$, $p < 0,001$)."
  * "Como a variável é logarítmica, interpretamos o efeito de dobrar o preço via $2^{\hat\beta_1} = 2^{2,151} \approx 4,44$. Ou seja: mantendo a região constante, dobrar o preço de um vinho multiplica por 4,44 a chance de ele atingir qualquer faixa superior de qualidade."
  * "O Velho Mundo apresenta um prêmio de reputação estatisticamente significativo: $\text{OR} = \exp(0,261) \approx 1,30$ (chances 30% maiores de categorias mais altas em relação ao Novo Mundo, com preço idêntico)."

### Slide 11: Probabilidades Preditas
* **O que falar**:
  * "O gráfico traça as curvas de probabilidade $\hat P(Y = j)$ ao longo do continuum de preço para cada terroir."
  * "Notem a transição suave: vinhos abaixo de US$ 20 são dominados pelas curvas azul-clara (Classes 1 e 2); em US$ 30 a 50 a Classe 3 atinge seu pico; e acima de US$ 60 a Classe 5 assume a liderança."

### Slide 12: Teste de Brant (Chances Proporcionais)
* **O que falar**:
  * "O teste de Brant testa a hipótese nula de que os coeficientes são idênticos em todos os $J-1$ logitos acumulados ($H_0: \boldsymbol\beta_1 = \boldsymbol\beta_2 = \dots$)."
  * "O teste omnibus rejeita $H_0$ com $\chi^2 = 932,1$ ($p < 0,001$). Porém, como alertado nas aulas e no Slide 2 da disciplina, com $N \approx 121.000$ observações, o teste tem superpoder estatístico e detecta desvios infinitesimais sem relevância prática. Precisamos investigar visualmente onde está o desvio."

### Slide 13: Colapsamentos Binários Sucessivos
* **O que falar**:
  * "Ajustamos 4 modelos logísticos binários independentes para $Y > 1, Y > 2, Y > 3$ e $Y > 4$ e plotamos as estimativas pontuais e intervalos contra a reta tracejada do modelo de chances proporcionais."
  * "Vejam que para o $\log(\text{preço})$, a reta tracejada passa quase no centro de todos os intervalos — o efeito do preço é notavelmente proporcional e estável! A rejeição do Brant é puxada quase exclusivamente pela covariável de região, cujo efeito se dissipa nas categorias mais extremas."

### Slide 14: Chances Proporcionais Parciais (PPOM via VGAM)
* **O que falar**:
  * "Para acomodar essa divergência, ajustamos o Modelo de Chances Proporcionais Parciais (PPOM) via pacote `VGAM` (Peterson & Harrell, 1990), mantendo o preço com efeito paralelo comum e relaxando os coeficientes da região para variarem a cada corte."
  * "O TRV confirma melhora significativa com 6 graus de liberdade adicionais ($\chi^2 = 867,4$, $p < 0,001$), sem gerar probabilidades preditas negativas."

### Slide 15: Diagnóstico: Resíduos Substitutos (Liu & Zhang, 2018)
* **Ponto Central Metodológico (Slide 3 do professor / Greenwell et al., 2018)**:
  * "Em modelos ordinais, resíduos comuns ou resíduos baseados em sinal (SBS; Li & Shepherd, 2012) são discretos e formam bandas paralelas artificiais que impedem o diagnóstico visual (Slide 3, p. 12-13)."
  * "Aplicamos a metodologia inovadora de **Liu & Zhang (2018, JASA)** e do pacote `sure` (Greenwell et al., 2018): amostramos uma variável substituta contínua $S$ a partir da distribuição logística truncada no intervalo $(\hat\alpha_{j-1}, \hat\alpha_j)$ correspondente à categoria observada."
  * "O resíduo substituto $R_S = S - \mathbf{x}^\top\hat{\boldsymbol\beta}$ recupera as propriedades ideais contínuas:"
    1. **QQ-plot**: Mostra excelente aderência dos resíduos à diagonal teórica logística dentro dos envelopes de bootstrap, comprovando que a função de ligação logit é adequada.
    2. **Resíduo $\times$ Ajustado**: Dispersão uniforme em torno de zero, sem funil de heterocedasticidade.
    3. **Resíduo $\times \log(\text{preço})$**: A curva LOESS (linha vermelha) é estritamente plana e horizontal em zero. Isso prova que a especificação linear de $\log(\text{preço})$ está correta e que termos quadráticos seriam redundantes (exatamente o diagnóstico do Slide 3, p. 28-32).
    4. **Resíduo $\times$ Região**: Dispersão e variância homogêneas entre Novo Mundo, Velho Mundo e Outros.

---

# Bloco 3: Modelo Binário, Eficiência e Conclusões (Gabriel)

### Slide 16: Dicotomização (90+ Pontos) e Custo de Eficiência
* **O que falar (Conexão Slide 1 e Slide 2 do professor)**:
  * "Dicotomizamos a resposta comercialmente em $Y_{\text{bin}} = 1$ para $\ge 90$ pontos (Classes 4 e 5) e ajustamos um modelo logístico binomial clássico via `glm(family = binomial)`."
  * "Vejam o resultado fundamental da tabela: os coeficientes estimados preservam a direção e a magnitude relativa ($\hat\beta_{\text{bin}} \approx 2,178$ vs. $\hat\beta_{\text{ord}} \approx 2,151$)."
  * "No entanto, observem a última coluna: a razão de variâncias amostrais $\text{EP}^2_{\text{bin}}/\text{EP}^2_{\text{ord}}$ varia de **1,73 a 1,89**. Ou seja: ao dicotomizar a pontuação e descartar a variação interna entre 80-89 e entre 90-100 pontos, **o analista joga fora quase metade da eficiência estatística dos dados**, exigindo uma amostra quase 80% a 90% maior para obter a mesma precisão inferencial!"

### Slide 17: Discriminação e Calibração (ROC e Youden)
* **O que falar (Slide 1 do professor, págs. 79 a 88)**:
  * "Comparamos a capacidade de discriminação entre a probabilidade direta do modelo binário e a probabilidade acumulada $P(Y \ge 4)$ derivada do modelo ordinal."
  * "Ambos os modelos alcançam um excelente poder de discriminação com $\text{AUC} = 0,792$."
  * "O índice de Youden identifica o limiar ótimo de corte de probabilidade em 0,381, entregando sensibilidade de 71,9% e especificidade de 72,5%."

### Slide 18: Razão de Chances ($\text{OR}$) $\times$ Risco Relativo ($\text{RR}$)
* **O que falar (Slide 1 do professor, págs. 19 a 26)**:
  * "Relembrando a dedução fundamental do Slide 1: a Razão de Chances é uma aproximação do Risco Relativo apenas quando o desfecho é raro ($\pi \to 0$)."
  * "Como 37,5% da nossa base tem 90+ pontos, o desfecho **não é raro**. Portanto, $\text{OR} = \text{RR} \times \frac{1-\pi_0}{1-\pi_1}$."
  * "Calculando para um vinho do Novo Mundo que passa de US$ 20 para US$ 40: a probabilidade de ser premiado sobe de 17,2% para 46,3%. O Risco Relativo é $\text{RR} = 2,69$, enquanto a Razão de Chances é $\text{OR} = 4,13$. Chamar OR de 'vezes mais probabilidade' geraria um exagero de mais de 50% na interpretação!"

### Slide 19: Frases Equivocadas (Armadilhas Interpretativas)
* **O que falar**:
  * "Compilamos quatro frases corriqueiras que reprovam em concursos e relatórios técnicos e que devem ser combatidas:"
    1. Confundir OR com RR ("tem 4 vezes mais probabilidade").
    2. Interpretar OR percentual como ponto percentual de probabilidade ("tem 30% mais vinhos premiados").
    3. Tratar $\exp(\hat\beta)$ genericamente como risco relativo.
    4. Tratar probabilidade ordinal como escala de qualidade linear ("o vinho fica 4 vezes melhor").

### Slide 20: Abordagem Bayesiana
* **O que falar**:
  * "Como extensões futuras apontadas na literatura recente, a inferência Bayesiana oferece três grandes vantagens práticas:"
    1. *Prioris regularizadoras* (como Ridge/Normal) para castas raras e pequenos produtores, prevenindo separação quase-completa via *shrinkage*.
    2. *Modelos hierárquicos com efeitos aleatórios* para modelar os avaliadores individuais (`taster_name`), isolando o rigor ou generosidade do crítico.
    3. Obtenção direta da distribuição posterior exata de quantidades não-lineares, como o Risco Relativo e probabilidades preditas por MCMC, sem depender de aproximações de primeira ordem (método Delta).

### Slide 21: Referências
* **O que falar**:
  * "Nossa base teórica ancora-se nos três grandes clássicos recomendados pelo professor: Alan Agresti (2010), o artigo seminal de Brant (1990) para o teste de paralelismo, Peterson & Harrell (1990) para o modelo parcial, e a metodologia de resíduos substitutos de Liu & Zhang (2018, JASA) e Greenwell et al. (2018, *The R Journal*). Muito obrigado, estamos abertos a perguntas da banca."

