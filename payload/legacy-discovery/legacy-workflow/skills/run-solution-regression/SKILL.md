---
name: run-solution-regression
description: Executa o gate completo de regressão de uma correção .NET após todas as TASKS terminarem. Valida o build da solution inteira, executa todos os testes e grava REGRESSION-FIX-NNNN.md. Não corrige código nem testes.
---

# Run Solution Regression

Você executa uma verificação independente depois que a implementação terminou. Não implementa tarefas e não tenta corrigir falhas; coleta evidências confiáveis para o gate final.

Antes de começar, leia os contratos de nomes, lifecycle, ownership, handoffs e falhas em `.github/skill-contracts/`. Esta skill é a única proprietária de `REGRESSION-FIX-{NNNN}.md`.

## Pré-condições

- Todas as `TASK-*` possuem estado runtime derivado `PUBLISHED` e commit local verificavel no historico Git local.
- `EXECUTION-FIX-{NNNN}.md` contém build verde da solution para cada tarefa.
- O worktree está limpo e na branch da FIX, com HEAD local coerente com `EXECUTION-FIX-{NNNN}.md`.
- `DESIGN-FIX-{NNNN}.md` aprovado declara `solution_path`, `build_configuration`, `build_command`, `regression_command` e `regression_scope`.

Se qualquer pré-condição falhar, registre `status: BLOCKED` sem iniciar uma regressão parcial apresentada como completa.

Siga `references/regression-gate.md` para validar e executar o conjunto completo aprovado no DESIGN. Grave o resultado conforme `references/regression-report.md`.

## Invariantes

- O build de entrada é sempre da solution inteira.
- O gate inclui todos os projetos/suítes de teste definidos pela solution ou pipeline oficial; não selecione apenas testes relacionados à mudança.
- Testes ignorados, não descobertos ou bloqueados são explicitados; não contam como sucesso silencioso.
- Não edite código de produção, testes, configuração ou dependências para obter verde.
- Não entre em loop: no máximo uma repetição diagnóstica de teste falho, sem alterações, para classificar possível instabilidade.
- Não faça commit, push, PR, merge, deploy ou rollback.

## Saída

Crie `REGRESSION-FIX-{NNNN}.md` na pasta da `FIX-*`. A `coordinate-fix` o consome para produzir `VERIFICATION-FIX-{NNNN}.md`.
Depois de gravar, execute `validate_artifacts.py`, `sync_index.py` e novamente `validate_artifacts.py` em `.github/skill-contracts/scripts/`.
