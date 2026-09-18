---
name: execute-fix-plan
description: Executa uma tarefa por vez de um plano aprovado de correção .NET definido por SPEC, DESIGN e TASKS. Atualiza a main, cria uma branch feature/mmYYYY/slug, exige testes unitários focados quando aplicáveis e build da solution inteira, então cria e envia o commit para a branch remota antes de aguardar autorização humana para a próxima tarefa. Interrompe e registra bloqueios. Não executa regressão completa, PR, merge ou deploy.
---

# Execute Fix Plan

Você implementa um plano aprovado sem trabalhar em one-shot. Cada execução cobre exatamente uma `TASK-*`: implementar, rodar os testes unitários necessários, compilar a solution inteira, concluir, commitar e fazer push da branch. Depois, informe o resultado ao humano e pare até ele autorizar a próxima tarefa.

## Pré-condições

Leia `SPEC-FIX-{NNNN}.md`, `DESIGN-FIX-{NNNN}.md` e `TASKS-FIX-{NNNN}.md` da mesma pasta. Execute `.github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge` antes de tocar no Git ou no código. Prossiga somente quando os contratos passarem e os três artefatos estiverem aprovados e rastreáveis.

Leia todos os contratos compartilhados. Use `references/git-workflow.md` para distinguir primeira execução de retomada, `references/task-execution.md` para a transação de uma TASK e `references/build-gate.md` para gates e orçamento.

## Invariantes

- A base é sempre `main`, atualizada a partir de `origin/main` por fast-forward.
- Na primeira execução, a `main` atualizada precisa passar o build completo antes de criar a feature; depois disso, a base fica congelada durante a FIX.
- Em retomadas, valide que HEAD local e remoto coincidem; não recrie a branch nem atualize `main`.
- A branch segue `feature/mmYYYY/descricao-curta`, com mês de dois dígitos, ano de quatro, letras minúsculas, números e hífens.
- Nunca execute mais de uma tarefa por autorização, mesmo que a anterior termine rapidamente.
- Uma tarefa só fica concluída depois de build bem-sucedido da solution inteira; build de projeto isolado nunca libera o gate.
- Quando a tarefa altera lógica executável, o teste unitário focado aplicável também precisa passar antes do commit.
- Um commit corresponde a uma tarefa concluída e só é criado após todos os gates aplicáveis ficarem verdes.
- Depois do commit, faça push somente da branch `feature/*` atual para `origin`. Nunca faça push direto em `main`.
- Depois do push, apresente resumo, gates, commit remoto e próxima tarefa; pergunte explicitamente se deseja continuar e pare.
- Se a recuperação do build ultrapassar o limite de tentativas ou o escopo da tarefa, pare e registre `BLOQUEADA`.
- Não execute regressão completa; essa responsabilidade pertence à skill `run-solution-regression`.
- Não abra PR, faça merge, qualquer rebase, force-push ou deploy.

## Estado persistente

Não edite `TASKS-FIX-{NNNN}.md`. Registre runtime somente em `EXECUTION-FIX-{NNNN}.md`, seguindo `.github/skill-contracts/`. Não altere SPEC, DESIGN, TASKS ou VERIFICATION.
