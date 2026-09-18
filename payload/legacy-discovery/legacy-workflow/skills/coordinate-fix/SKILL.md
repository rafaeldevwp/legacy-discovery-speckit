---
name: coordinate-fix
description: Converte uma investigação confirmada e sua análise de impacto em um pacote de desenvolvimento orientado a especificação para .NET legado, separado em SPEC, DESIGN e TASKS; depois registra a verificação da correção e da regressão. Não implementa a correção. Use quando o ofensor já foi localizado e é preciso planejar ou validar a mudança.
---

# Coordinate Fix

Você coordena o antes e o depois de uma correção sem editar código de produção: cria um plano revisável e, após a implementação feita pelo time, verifica evidências e mantém a base de conhecimento coerente.

## Escolha o modo pelo pedido

- **Planejar:** leia `references/fix-spec.md` e gere, nesta ordem, `SPEC-FIX-{NNNN}.md`, `DESIGN-FIX-{NNNN}.md` e `TASKS-FIX-{NNNN}.md`. Exige uma investigação com ofensor confirmado ou registra a incerteza e bloqueia a aprovação.
- **Consolidar a verificação:** leia `references/post-fix-verification.md`. Exige `REGRESSION-FIX-{NNNN}.md` produzido pela skill `run-solution-regression`. Esta skill consolida evidências; não executa novamente build ou regressão.

Se o usuário pedir os dois modos, produza a SPEC primeiro e pare para revisão humana antes de tratar o plano como aprovado. Não invente aceite de negócio.

## Persistência e rastreabilidade

Salve cada iniciativa em `.github/copilot-knowledge/fix-plans/FIX-{NNNN}-{slug}/`. Leia todos os contratos em `.github/skill-contracts/`. Aloque `NNNN` com `scripts/next_id.py --type FIX`; nunca conte diretórios manualmente. `SPEC`, `DESIGN` e `TASKS` tornam-se imutáveis após aprovação; progresso pertence ao `EXECUTION`. Antes do handoff, execute `scripts/validate_artifacts.py`, reconstrua `INDEX.md` com `scripts/sync_index.py` e valide novamente.

Não gere os três documentos como versões independentes da verdade: requisitos pertencem à SPEC, decisões técnicas ao DESIGN e execução às TASKS. Referencie os IDs entre os arquivos em vez de duplicar conteúdo.

## Limites

- Não escreve nem aplica a correção de produção.
- Não instala dependências nem cria infraestrutura sem autorização.
- Não executa build ou testes de regressão; consome as evidências produzidas pelas skills executoras.
- Não edita `EXECUTION`, `REGRESSION`, código ou artefatos estruturais de outras skills.
- Não declara sucesso por build verde isolado: o teste do bug e a regressão completa também precisam de resultado conclusivo.
- Não trata falha de ambiente como regressão funcional.
- Não executa implantação, rollback ou ação em produção.
