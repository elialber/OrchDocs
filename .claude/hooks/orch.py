#!/usr/bin/env python3
"""OrchDocs harness: hooks do Claude Code e /orch-status.

Uso:
  orch.py pre-tool-use   PreToolUse (Edit/Write/MultiEdit): bloqueia arquivo FROZEN (exit 2)
  orch.py stop           Stop: registra resumo da sessão em .orch/sessions.md do projeto ativo
  orch.py status         lista projetos e etapa atual

Formato de estado (PROVISÓRIO, até a Pipeline Spec definir):
  projects/<slug>/.orch/state.json
    {"stage": "<etapa atual>",
     "documents": {"<caminho relativo a projects/<slug>/>": {"status": "FROZEN"}}}
  docs/orchdocs/.status.json
    {"documents": {"<caminho relativo a docs/orchdocs/>": {"status": "FROZEN"}}}
  projects/.active   uma linha com o <slug> do projeto ativo

Raiz do repo: $CLAUDE_PROJECT_DIR, senão o "cwd" do payload, senão o diretório atual.
"""
import glob
import json
import os
import re
import sys
from datetime import datetime

FROZEN = "FROZEN"
WRITE_TOOLS = {"Edit", "Write", "MultiEdit"}


def repo_root(payload):
    return os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()


def norm(path):
    return os.path.normcase(os.path.realpath(path))


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def state_files(root):
    """Pares (arquivo de estado, diretório base dos caminhos declarados nele)."""
    for state in glob.glob(os.path.join(root, "projects", "*", ".orch", "state.json")):
        yield state, os.path.dirname(os.path.dirname(state))
    status = os.path.join(root, "docs", "orchdocs", ".status.json")
    if os.path.isfile(status):
        yield status, os.path.dirname(status)


def frozen_owner(root, target):
    """Arquivo de estado que declara `target` como FROZEN, ou None."""
    target = norm(target)
    for state_path, base in state_files(root):
        docs = (load_json(state_path) or {}).get("documents") or {}
        for rel, entry in docs.items():
            status = entry.get("status") if isinstance(entry, dict) else entry
            if status == FROZEN and norm(os.path.join(base, rel)) == target:
                return state_path
    return None


def pre_tool_use(payload):
    if payload.get("tool_name") not in WRITE_TOOLS:
        return 0
    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0
    root = repo_root(payload)
    if not os.path.isabs(file_path):
        file_path = os.path.join(root, file_path)
    owner = frozen_owner(root, file_path)
    if owner is None:
        return 0
    sys.stderr.write(
        f"BLOQUEADO: {os.path.relpath(file_path, root)} está FROZEN "
        f"(declarado em {os.path.relpath(owner, root)}).\n"
        "Documentos FROZEN não são editados. Abra um Change Request descrevendo "
        "a mudança, o motivo e o impacto nos documentos seguintes, e peça Approval.\n"
    )
    return 2


def active_project(root):
    try:
        with open(os.path.join(root, "projects", ".active"), encoding="utf-8") as f:
            slug = f.read().strip()
    except OSError:
        return None
    path = os.path.join(root, "projects", slug)
    return path if slug and os.path.isdir(path) else None


def summarize_transcript(path):
    """(primeiro pedido do usuário, nº de pedidos, arquivos escritos)."""
    first, prompts, files = None, 0, []
    try:
        lines = read_text(path).splitlines()
    except (OSError, TypeError):
        lines = []
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        message = entry.get("message") or {}
        content = message.get("content")
        if entry.get("type") == "user" and message.get("role") == "user":
            text = content if isinstance(content, str) else " ".join(
                c.get("text", "") for c in content or [] if c.get("type") == "text")
            if text.strip():
                prompts += 1
                first = first or " ".join(text.split())[:100]
        if isinstance(content, list):
            for c in content:
                if c.get("type") == "tool_use" and c.get("name") in WRITE_TOOLS:
                    fp = (c.get("input") or {}).get("file_path")
                    if fp and fp not in files:
                        files.append(fp)
    return first, prompts, files


def stop(payload):
    root = repo_root(payload)
    project = active_project(root)
    if project is None:
        return 0
    session = str(payload.get("session_id") or "desconhecida")
    first, prompts, files = summarize_transcript(payload.get("transcript_path"))
    rel = [os.path.relpath(f, root) if os.path.isabs(f) else f for f in files]
    marker = f"<!-- session:{session} -->"
    block = "\n".join([
        marker,
        f"## {datetime.now():%Y-%m-%d %H:%M} · sessão {session[:8]}",
        f"- Pedido inicial: {first or '(sem texto)'}",
        f"- Pedidos: {prompts}",
        f"- Arquivos escritos: {', '.join(rel) if rel else 'nenhum'}",
        "",
    ])
    log = os.path.join(project, ".orch", "sessions.md")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    text = read_text(log) if os.path.isfile(log) else "# Sessões\n\n"
    # Stop dispara a cada resposta: um bloco por sessão, reescrito no lugar.
    pattern = re.compile(re.escape(marker) + r"\n.*?(?=\n<!-- session:|\Z)", re.S)
    if pattern.search(text):
        text = pattern.sub(lambda _: block.rstrip("\n"), text)
    else:
        text = text.rstrip("\n") + "\n\n" + block
    with open(log, "w", encoding="utf-8") as f:
        f.write(text)
    return 0


def status(payload):
    root = repo_root(payload)
    projects = sorted(
        d for d in glob.glob(os.path.join(root, "projects", "*"))
        if os.path.isdir(d) and not os.path.basename(d).startswith("."))
    if not projects:
        print("nenhum projeto")
        return 0
    active = active_project(root)
    for d in projects:
        state = load_json(os.path.join(d, ".orch", "state.json")) or {}
        mark = " (ativo)" if active and norm(d) == norm(active) else ""
        print(f"- {os.path.basename(d)}{mark}: {state.get('stage') or 'sem etapa registrada'}")
    return 0


COMMANDS = {"pre-tool-use": pre_tool_use, "stop": stop, "status": status}


def main(argv):
    if len(argv) != 2 or argv[1] not in COMMANDS:
        sys.stderr.write(f"uso: orch.py {{{'|'.join(COMMANDS)}}}\n")
        return 1
    payload = {}
    if argv[1] != "status" and not sys.stdin.isatty():
        try:
            payload = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            payload = {}
    if argv[1] == "stop":
        try:
            return stop(payload)
        except Exception as exc:  # o registro de sessão nunca deve travar o Stop
            sys.stderr.write(f"orch stop: {exc}\n")
            return 0
    return COMMANDS[argv[1]](payload)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
