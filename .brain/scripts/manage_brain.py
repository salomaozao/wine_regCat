#!/usr/bin/env python3
"""
CLI de gerenciamento da pasta .brain/ para o projeto wine_regCat.
Suporta comandos:
  - sync: sincroniza decisoes.md e pendencias.md a partir dos arquivos em decisoes/ e pendencias/
  - audit: audita a integridade dos metadados e arquivos de governança
"""

import os
import sys
import glob
import re

BRAIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DECISOES_DIR = os.path.join(BRAIN_DIR, "decisoes")
PENDENCIAS_DIR = os.path.join(BRAIN_DIR, "pendencias")
DECISOES_MD = os.path.join(BRAIN_DIR, "decisoes.md")
PENDENCIAS_MD = os.path.join(BRAIN_DIR, "pendencias.md")


def parse_frontmatter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    raw_yaml, body = match.groups()
    meta = {}
    for line in raw_yaml.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                val = [item.strip().strip('"').strip("'") for item in val[1:-1].split(",") if item.strip()]
            meta[key] = val
    return meta, body


def sync_decisoes():
    files = sorted(glob.glob(os.path.join(DECISOES_DIR, "*.md")))
    ativas = []
    revogadas = []

    for fpath in files:
        meta, _ = parse_frontmatter(fpath)
        fname = os.path.basename(fpath)
        dec_id = meta.get("id", fname.replace(".md", ""))
        titulo = meta.get("titulo", "Sem título")
        modulo = meta.get("modulo_afetado", "-")
        if isinstance(modulo, list):
            modulo = ", ".join(modulo)
        data = meta.get("data_decisao", "-")
        status = meta.get("status", "ativo").lower()

        rel_link = f"[decisoes/{fname}](decisoes/{fname})"
        row = f"| **{dec_id}** | {titulo} | {modulo} | {data} | {rel_link} |"

        if status == "ativo":
            ativas.append(row)
        else:
            revogadas.append(row)

    out = [
        "# Sumário Executivo de Decisões Metodológicas e Arquiteturais",
        "",
        "> Este arquivo é gerado automaticamente via `python .brain/scripts/manage_brain.py sync`.",
        "",
        "## Decisões Ativas",
        "",
        "| ID | Título | Módulos | Data | Arquivo |",
        "|:---|:---|:---|:---|:---|",
    ]
    if ativas:
        out.extend(ativas)
    else:
        out.append("| - | Nenhuma decisão ativa registrada | - | - | - |")

    out.extend([
        "",
        "## Decisões Revogadas ou Substituídas",
        "",
        "| ID | Título | Módulos | Data | Arquivo |",
        "|:---|:---|:---|:---|:---|",
    ])
    if revogadas:
        out.extend(revogadas)
    else:
        out.append("| - | Nenhuma decisão revogada | - | - | - |")

    out.append("")
    with open(DECISOES_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"[OK] Sincronizado {DECISOES_MD} ({len(ativas)} ativas, {len(revogadas)} revogadas)")


def sync_pendencias():
    files = sorted(glob.glob(os.path.join(PENDENCIAS_DIR, "*.md")))
    abertas = []
    resolvidas = []

    for fpath in files:
        meta, _ = parse_frontmatter(fpath)
        fname = os.path.basename(fpath)
        pend_id = meta.get("id", fname.replace(".md", ""))
        titulo = meta.get("titulo", "Sem título")
        modulo = meta.get("modulo_afetado", "-")
        if isinstance(modulo, list):
            modulo = ", ".join(modulo)
        crit = meta.get("criticidade", "media").lower()
        status = meta.get("status", "aberto").lower()
        resp = meta.get("responsavel", "-")
        dt_res = meta.get("data_resolucao", "-")

        rel_link = f"[pendencias/{fname}](pendencias/{fname})"

        if status == "resolvido":
            resolvidas.append(f"| **{pend_id}** | {titulo} | {modulo} | {dt_res} | {resp} | {rel_link} |")
        else:
            abertas.append(f"| **{pend_id}** | {titulo} | {modulo} | {crit.upper()} | {resp} | {rel_link} |")

    out = [
        "# Sumário Executivo de Pendências (Backlog)",
        "",
        "> Este arquivo é gerado automaticamente via `python .brain/scripts/manage_brain.py sync`.",
        "",
        "## Pendências Abertas",
        "",
        "| ID | Título | Módulos | Criticidade | Responsável | Arquivo |",
        "|:---|:---|:---|:---|:---|:---|",
    ]
    if abertas:
        out.extend(abertas)
    else:
        out.append("| - | Nenhuma pendência aberta | - | - | - | - |")

    out.extend([
        "",
        "## Pendências Resolvidas",
        "",
        "| ID | Título | Módulos | Data Resolução | Responsável | Arquivo |",
        "|:---|:---|:---|:---|:---|:---|",
    ])
    if resolvidas:
        out.extend(resolvidas)
    else:
        out.append("| - | Nenhuma pendência resolvida | - | - | - | - |")

    out.append("")
    with open(PENDENCIAS_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"[OK] Sincronizado {PENDENCIAS_MD} ({len(abertas)} abertas, {len(resolvidas)} resolvidas)")


def audit():
    errors = 0
    print(f"=== Auditando integridade de .brain em {BRAIN_DIR} ===")

    for name, req_fields, pdir in [
        ("Decisões", ["id", "titulo", "status"], DECISOES_DIR),
        ("Pendências", ["id", "titulo", "status", "criticidade"], PENDENCIAS_DIR)
    ]:
        files = glob.glob(os.path.join(pdir, "*.md"))
        for fpath in files:
            meta, _ = parse_frontmatter(fpath)
            for req in req_fields:
                if req not in meta:
                    print(f"[ERRO] {name} {os.path.basename(fpath)} não possui metadado obrigatório '{req}'")
                    errors += 1

    dialogo = os.path.join(BRAIN_DIR, "dialogo_ias.md")
    if not os.path.exists(dialogo):
        print("[ERRO] Arquivo dialogo_ias.md não encontrado!")
        errors += 1

    if errors == 0:
        print("[SUCESSO] Auditoria concluída sem inconsistências!")
    else:
        print(f"[FALHA] Auditoria encontrou {errors} inconsistência(s).")
    return errors


def main():
    if len(sys.argv) < 2:
        print("Uso: python manage_brain.py [sync|audit]")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "sync":
        sync_decisoes()
        sync_pendencias()
    elif cmd == "audit":
        errs = audit()
        sys.exit(1 if errs > 0 else 0)
    else:
        print(f"Comando desconhecido: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()

