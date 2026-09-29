# 00 — OrchDocs Constitution

Status: DRAFT · Topo da hierarquia dos documentos do OrchDocs (`docs/orchdocs/`): Constitution > PRD > TRD > Pipeline Spec > Implementation Plan.
Essa hierarquia não se aplica aos documentos de um Project, que seguem P3 e a Decision Policy (§4).

## 1. Missão

O OrchDocs transforma a ideia bruta de um jogo digital em um pacote de pré-produção rastreável, um documento por vez, até um Production Handoff pronto para iniciar a produção.

## 2. Princípios

- **P1 — Um documento por vez.** Cada Stage produz um único documento, escrito a partir de todos os anteriores.
- **P2 — Rastreabilidade.** Toda decisão de um documento aponta para a fonte que a sustenta: o Brief, um documento anterior ou uma Evidence.
- **P3 — Anti-drift.** Um documento anterior vence um posterior; mudanças passam por Change Request.
- **P4 — Humano decide.** O agente executa o fluxo; decisões de produto são do operador.
- **P5 — Evidência antes de arquitetura.** Nenhuma decisão técnica (04 TRD em diante) antes do gate 03C aprovado com Evidence.

## 3. Decisões

### Operador e escopo

- **D1** — O OrchDocs MUST servir um único operador.
- **D2** — O OrchDocs MUST aceitar qualquer jogo digital, sem supor 3D.
- **D3** — A prosa MUST ser em português; termos, palavras-chave (MUST, SHOULD, COULD, OPEN DECISION, N/A), status (DRAFT, FROZEN, STALE, ABANDONED) e identificadores MUST ficar em inglês.

### Pipeline

- **D4** — A entrada MUST ser um Brief em `projects/<slug>/BRIEF.md`, imutável após a criação do Project.
- **D5** — O pipeline MUST ser fixo e seguido nesta ordem, sem etapas puladas:
  00 Game Constitution · 01 Vision · 02 GDD · 03 Prototype Spec · 03A Prototype Review · 03B Prototype Execution Plan · **[GATE] 03C Prototype Results** · 04 TRD · 05 Game Flow/UX · 06 Art Direction Bible · 06A Visual Exploration · 07 Asset Bible · 08 Systems Design · 09 Level Design · 10 Animation/VFX/Audio · 11 Vertical Slice · 12 Implementation Plan · 12A Pre-Implementation Audit · 13 Production Handoff.
- **D6** — Seção que não se aplica ao jogo MUST ser marcada `N/A — <justificativa>`, com a justificativa rastreável ao Brief ou a um documento anterior.
- **D7** — O 13 Production Handoff MUST ser apenas um documento em `projects/<slug>/`; o OrchDocs MUST NOT criar repositórios, código, issues ou harness de produção.

### Protótipo e gate

- **D8** — O OrchDocs MUST apenas planejar protótipos; a construção e o playtest acontecem fora dele.
- **D9** — O 03C MUST se basear em Evidence anexada ao Project; sem Evidence, o gate MUST NOT ser aprovado. O 04 TRD MUST NOT começar sem o 03C FROZEN e o gate aprovado pelo operador; o Freeze do 03C sozinho não aprova o gate.
- **D10** — Com o gate reprovado, o agente MUST recomendar iterar, pivotar ou encerrar (ABANDONED), com justificativa; o operador decide. Cada Iteration MUST preservar a Evidence, o motivo da reprovação e os documentos da Iteration anterior.

### Autonomia

- **D11** — Em um Project, o agente SHOULD redigir, revisar, congelar e avançar sem pedir aprovação, desde que a Review em contexto fresco não aponte problemas.
- **D12** — O agente MUST parar e consultar o operador para: resolver uma OPEN DECISION, decidir o gate 03C, aprovar ou rejeitar um Change Request, e atingir o teto de custo.
- **D13** — Documentos do próprio OrchDocs (`docs/orchdocs/`) MUST receber Approval explícita do operador antes do Freeze.

### Modelos, ferramentas e custo

- **D14** — A redação e a Review SHOULD usar Claude Opus 5.5; tarefas mecânicas (checagem de formato, rastreabilidade, estado) COULD usar Claude Sonnet 5.5.
- **D15** — Referências visuais MUST ser geradas apenas no 06A, com gpt-image-2.5-sunburst; 06 e 07 MUST citar as imagens do 06A em vez de gerar novas.
- **D16** — O custo acumulado de cada Project MUST ser registrado no estado do Project.
- **D17** — Os documentos dos Projects MUST NOT depender de uma ferramenta ou harness específico; o ECC serve apenas para construir o OrchDocs.

### OPEN DECISIONS

- **OPEN DECISION OD1** — Qual o teto de custo por Project? Definir depois de um primeiro Project real.

## 4. Decision Policy

1. Um documento posterior MUST NOT contradizer um anterior FROZEN.
2. Ao encontrar um conflito com um documento FROZEN, o agente MUST parar o Stage atual e abrir um Change Request com: documento e seção alvo, mudança proposta, motivo e a seção do documento atual que revelou o conflito.
3. O operador aprova ou rejeita o Change Request.
4. Aprovado: o documento alvo ganha nova versão FROZEN; todo documento entre o alvo e o atual que cite a seção alterada vira STALE.
5. Documentos STALE MUST passar por nova Review e correção antes de o Stage atual continuar.
6. Rejeitado: o Stage atual MUST se adequar ao documento FROZEN.

## 5. Anti-Drift Rules do OrchDocs

- **A1** — Em um Project, os únicos documentos de pré-produção MUST ser os do pipeline em D5; pedidos fora dele (propostas, pitch decks, documentação de software que não seja jogo) estão fora do escopo.
- **A2** — O OrchDocs MUST NOT gerar mais de um documento por Stage, nem iniciar um Stage antes do Freeze do anterior.
- **A3** — O OrchDocs MUST NOT pular etapas nem o gate 03C; o que não se aplica vira seção N/A (D6).
- **A4** — O agente MUST NOT preencher uma decisão ausente nas fontes; ela vira `OPEN DECISION`.

## 6. Non-goals

- Uso por equipes ou por outros estúdios.
- Construir ou executar protótipos.
- Gerar código, repositórios, issues ou harness de produção.
- Ser um gerador genérico de documentos.
- Gerar documentos em lote ou pular etapas.
- Amarrar os documentos dos Projects a uma ferramenta ou harness específico.
- Produzir assets finais; as imagens do 06A são referências.
- Gestão de produção após o handoff (cronograma, sprints, bugs).
- Estimativa de orçamento financeiro ou de equipe do jogo.
- Análise de mercado, monetização ou business plan.
