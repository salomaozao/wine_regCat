# Governança da Memória do Projeto (.brain)

Este diretório mantém a memória compartilhada, as decisões metodológicas e o histórico de trabalho entre desenvolvedores e inteligências artificiais no projeto **wine_regCat** (Trabalho Prático 1 de Regressão para Dados Categóricos e Ordinais - UFMG).

---

## Estrutura da Pasta `.brain/`

```text
.brain/
├── README.md                      # Este guia de governança
├── plano_implementacao.md         # Plano analítico, metodológico e de apresentação do TP1
├── dialogo_ias.md                 # Log cronológico de ações e handoffs entre sessões/IAs
├── decisoes.md                    # Sumário executivo das decisões metodológicas ativas
├── decisoes/                      # Decisões detalhadas em Markdown com YAML frontmatter
│   └── 01_modelagem_tp1_vinhos.md
├── pendencias.md                  # Sumário executivo das pendências (abertas e resolvidas)
├── pendencias/                    # Pendências detalhadas em Markdown com YAML frontmatter
│   └── 01_definicao_cortes_ordinais.md
└── scripts/
    └── manage_brain.py            # Script CLI para sincronização (sync) e auditoria (audit)
```

---

## Workflow para Sessões e IAs

1. **Início de Sessão**:
   * Ler `decisoes.md` para respeitar as diretrizes teóricas e metodológicas acordadas.
   * Ler `pendencias.md` para identificar bloqueios ou itens em aberto.
   * Ler o final de `dialogo_ias.md` (bloco *Próxima IA / Handoff*).

2. **Durante a Sessão**:
   * Novas decisões devem ser salvas em `decisoes/` e pendências em `pendencias/`.
   * Rodar `python .brain/scripts/manage_brain.py sync` para atualizar automaticamente os sumários.

3. **Final de Turno / Bloco de Trabalho**:
   * Registrar o commit/handoff no formato padronizado ao final de `dialogo_ias.md`.

