# Preparação da base de vinhos usada nas seções "Em R com os vinhos".
# Mesmas definições do pipeline do TP1 (capítulo 11). Na primeira execução
# salva um .rds para acelerar os capítulos seguintes.

suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(MASS, exclude = "select")
  library(VGAM)
})

arq_rds <- "R/vinhos.rds"

if (file.exists(arq_rds)) {
  df <- readRDS(arq_rds)
} else {
  raw <- read.csv("../TP1/data/winemagv2.csv", encoding = "UTF-8")

  K_CAT   <- 5
  cortes  <- quantile(raw$points, probs = seq(0, 1, length.out = K_CAT + 1), type = 1)
  velho   <- c("France", "Italy", "Spain", "Portugal", "Germany", "Austria")
  novo    <- c("US", "Chile", "Argentina", "Australia", "South Africa", "New Zealand")
  top_var <- names(sort(table(raw$variety), decreasing = TRUE))[1:5]

  df <- raw |>
    filter(!is.na(price), country != "") |>
    mutate(
      points_ord  = cut(points, breaks = unique(cortes), include.lowest = TRUE,
                        labels = seq_len(length(unique(cortes)) - 1), ordered_result = TRUE),
      points_bin  = as.integer(points >= 90),
      log_price   = log(price),
      terroir     = factor(case_when(country %in% velho ~ "Velho Mundo",
                                     country %in% novo  ~ "Novo Mundo",
                                     TRUE               ~ "Outros"),
                           levels = c("Novo Mundo", "Velho Mundo", "Outros")),
      variety_top = relevel(factor(if_else(variety %in% top_var, variety, "Outras")), ref = "Outras"),
      taster_name = na_if(taster_name, "")
    ) |>
    select(points, points_ord, points_bin, price, log_price, country, terroir,
           variety, variety_top, taster_name)

  saveRDS(df, arq_rds)
}

theme_set(theme_minimal(base_size = 12))
paleta5 <- c("#D9A5B3", "#B86B77", "#9E3D52", "#7A182F", "#4A0E17")
vinho   <- c("#7A182F", "#B86B77", "#D9A5B3", "#4A0E17")
