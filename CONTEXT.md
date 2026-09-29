# OrchDocs

Orquestração da documentação de pré-produção de um jogo, um documento por vez, do Brief ao Implementation Plan.

> Todos os termos abaixo são **provisórios** até serem resolvidos via `/domain-modeling`.

## Language

**Project** _(provisório)_: um jogo em pré-produção, com seus documentos e estado em `projects/<slug>/`.

**Brief** _(provisório)_: a ideia bruta do jogo, entrada do primeiro Stage.

**Stage** _(provisório)_: uma etapa do pipeline que produz exatamente um documento.

**Stage Contract** _(provisório)_: o que um Stage exige de entrada e promete de saída.

**Gate** _(provisório)_: condição que precisa ser satisfeita para avançar ao próximo Stage (ex.: o gate de protótipo).

**Draft** _(provisório)_: versão de trabalho de um documento, ainda editável.

**Review** _(provisório)_: avaliação de um Draft feita em contexto fresco, antes da Approval.

**Approval** _(provisório)_: aceite humano de um documento revisado.

**Freeze** _(provisório)_: transição de um documento aprovado para o status FROZEN, que o torna imutável.

**Change Request** _(provisório)_: pedido formal de alteração em um documento FROZEN.

**Open Decision** _(provisório)_: decisão que as fontes não resolvem, marcada `OPEN DECISION` no documento até alguém decidir.
