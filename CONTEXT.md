# OrchDocs

Orquestração da documentação de pré-produção de um jogo, um documento por vez, do Brief ao Production Handoff.

> Todos os termos abaixo são **provisórios** até serem resolvidos via `/domain-modeling`.

## Language

**Operator** _(provisório)_: a única pessoa que usa o OrchDocs e toma as decisões de produto (D1, P4).
_Avoid_: usuário

**Project** _(provisório)_: um jogo em pré-produção, com seus documentos e estado em `projects/<slug>/`.

**Active Project** _(provisório)_: o Project em que os comandos agem quando nenhum slug é informado; há no máximo um.

**Brief** _(provisório)_: a ideia bruta do jogo, entrada do primeiro Stage.

**Stage** _(provisório)_: uma etapa do pipeline que produz exatamente um documento.

**Stage Contract** _(provisório)_: o que um Stage exige de entrada e promete de saída.

**Gate** _(provisório)_: condição que precisa ser satisfeita para avançar ao próximo Stage (ex.: o gate de protótipo).

**Draft** _(provisório)_: versão de trabalho de um documento, ainda editável; status `DRAFT`.

**Stop Point** _(provisório)_: momento em que o agente interrompe o avanço autônomo e espera uma decisão do Operator (OPEN DECISION, gate 03C, Change Request, teto de custo, Review com problemas depois das correções, aguardando Evidence, impressões do Operator vazias no 03C e escolha depois do gate reprovado).
_Avoid_: pausa, bloqueio

**Review** _(provisório)_: avaliação de um Draft feita em contexto fresco, antes da Approval.
Não confundir com o Stage 03A Prototype Review, que é um documento do pipeline.

**Approval** _(provisório)_: aceite humano de um documento revisado.

**Freeze** _(provisório)_: transição de um documento aprovado para o status FROZEN, que o torna imutável.

**Audit Log** _(provisório)_: registro só de acréscimo de todas as transições de um Project, com data, autor e documento.
_Avoid_: histórico

**Change Request** _(provisório)_: pedido formal de alteração em um documento FROZEN.

**Open Decision** _(provisório)_: decisão que as fontes não resolvem, marcada `OPEN DECISION` no documento até alguém decidir.

**N/A Section** _(provisório)_: seção de um documento que não se aplica ao jogo, marcada `N/A — <justificativa>` rastreável ao Brief ou a um documento anterior.

**Evidence** _(provisório)_: material de um protótipo jogado de verdade (builds, vídeos, notas de playtest, métricas), anexado ao Project e base do gate 03C.

**Iteration** _(provisório)_: uma rodada de 03 → 03C; uma reprovação no gate pode abrir uma nova Iteration, preservando a anterior.

**STALE** _(provisório)_: status de um documento FROZEN afetado por um Change Request aprovado num documento anterior; exige nova Review.

**ABANDONED** _(provisório)_: status de um Project encerrado por decisão do operador após o gate reprovado.

**Production Handoff** _(provisório)_: o documento 13, último do pipeline, com o necessário para iniciar a produção.
_Avoid_: transição para produção
