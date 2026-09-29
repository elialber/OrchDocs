# OrchDocs

Orquestração da documentação de pré-produção de um jogo, um documento por vez, do Brief ao Production Handoff.

> Todos os termos abaixo são **provisórios** até serem resolvidos via `/domain-modeling`.

## Language

**Project** _(provisório)_: um jogo em pré-produção, com seus documentos e estado em `projects/<slug>/`.

**Brief** _(provisório)_: a ideia bruta do jogo, entrada do primeiro Stage.

**Stage** _(provisório)_: uma etapa do pipeline que produz exatamente um documento.

**Stage Contract** _(provisório)_: o que um Stage exige de entrada e promete de saída.

**Gate** _(provisório)_: condição que precisa ser satisfeita para avançar ao próximo Stage (ex.: o gate de protótipo).

**Draft** _(provisório)_: versão de trabalho de um documento, ainda editável; status `DRAFT`.

**Review** _(provisório)_: avaliação de um Draft feita em contexto fresco, antes da Approval.
Não confundir com o Stage 03A Prototype Review, que é um documento do pipeline.

**Approval** _(provisório)_: aceite humano de um documento revisado.

**Freeze** _(provisório)_: transição de um documento aprovado para o status FROZEN, que o torna imutável.

**Change Request** _(provisório)_: pedido formal de alteração em um documento FROZEN.

**Open Decision** _(provisório)_: decisão que as fontes não resolvem, marcada `OPEN DECISION` no documento até alguém decidir.

**N/A Section** _(provisório)_: seção de um documento que não se aplica ao jogo, marcada `N/A — <justificativa>` rastreável ao Brief ou a um documento anterior.

**Evidence** _(provisório)_: material de um protótipo jogado de verdade (builds, vídeos, notas de playtest, métricas), anexado ao Project e base do gate 03C.

**Iteration** _(provisório)_: uma rodada de 03 → 03C; uma reprovação no gate pode abrir uma nova Iteration, preservando a anterior.

**STALE** _(provisório)_: status de um documento FROZEN afetado por um Change Request aprovado num documento anterior; exige nova Review.

**ABANDONED** _(provisório)_: status de um Project encerrado por decisão do operador após o gate reprovado.

**Production Handoff** _(provisório)_: o documento 13, último do pipeline, com o necessário para iniciar a produção.
_Avoid_: transição para produção
