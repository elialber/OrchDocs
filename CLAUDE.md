# OrchDocs

Orquestrador que recebe a ideia bruta de um jogo (o Brief) e produz a documentação de pré-produção, um documento por vez.
Sequência: 00 Game Constitution → … → 12A Pre-Implementation Audit → 13 Production Handoff, com gate de protótipo em 03C.
Cada documento é escrito a partir dos anteriores. Normas em `docs/orchdocs/00_CONSTITUTION.md`; vocabulário em `CONTEXT.md`.

## Regras

- Um documento por vez. Só comece o próximo depois do Freeze do atual.
- Documentos de `docs/orchdocs/` só congelam com o "aprovado" do operador. Em Projects, avance sozinho e pare apenas em OPEN DECISION, gate 03C, Change Request ou teto de custo.
- Antes de escrever, leia todos os documentos anteriores do Project.
- Documento FROZEN é imutável: registre a mudança como Change Request. O hook de PreToolUse bloqueia a escrita.
- Decisão ausente nas fontes vira `OPEN DECISION: <pergunta>`; nunca a preencha por conta própria.
- Requisitos usam MUST / SHOULD / COULD.
- Antes de pedir Approval, faça a Review em contexto fresco (subagente sem o histórico da redação).
- Nenhum código antes da fase 6.

## Fontes da verdade

Em conflito, vence o documento mais alto:
Constitution > PRD > TRD > Pipeline Spec > Implementation Plan.

Os prompts originais em `reference/chatgpt-prompts/` são insumo, não fonte da verdade.

## Harness

- Estado por Project em `projects/<slug>/.orch/state.json`; estado do próprio OrchDocs em `docs/orchdocs/.status.json`.
- Hooks: `.claude/hooks/orch.py` (formato do estado documentado no topo do script).
- Testes: `python3 -m unittest discover -s tests -t .`
- Regras ECC: só `common/` em `.claude/rules/ecc/`. A regra de linguagem entra depois do TRD.

## Agent skills

### Issue tracker

Issues vivem no GitHub Issues de elialber/OrchDocs (via `gh`). See `docs/agents/issue-tracker.md`.

### Triage labels

Rótulos canônicos padrão (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` na raiz. See `docs/agents/domain.md`.
