---
name: prepare-feature-branch
description: Prepara uma branch Git segura para uma mudança em sistema legado antes do Spec Kit. Atualiza main via fast-forward, valida worktree e origin, cria branch no padrão feature/mmYYYY/descricao-curta e nunca faz stash, reset, merge, rebase, force ou push automaticamente.
---

# Prepare Feature Branch

Você controla **somente o baseline Git e a criação da branch de trabalho**.

Use esta skill depois que um `SPECKIT_HANDOFF` estiver `READY_FOR_SPECKIT` e antes de `/speckit.specify` quando a mudança será implementada em uma feature branch.

## Responsabilidade

Você PODE:

- validar se o diretório atual é um repositório Git;
- exigir worktree limpo;
- validar o remote `origin`;
- executar `git fetch origin`;
- mudar para `main`;
- atualizar `main` somente com `git pull --ff-only origin main`;
- criar uma nova branch **a partir da main atualizada**;
- usar o padrão `feature/mmYYYY/descricao-curta`;
- reportar branch e `base_commit`.

Você NÃO PODE:

- executar `git stash` automaticamente;
- descartar alterações;
- executar `git reset`;
- executar merge ou rebase;
- usar `--force`;
- apagar ou recriar branch existente;
- fazer push automaticamente;
- modificar código, spec, plan ou tasks.

## Pré-condições

Antes de criar a branch:

1. O `SPECKIT_HANDOFF` da mudança deve estar `READY_FOR_SPECKIT`, salvo ordem explícita do usuário para apenas preparar Git.
2. O worktree deve estar limpo.
3. `origin` deve existir.
4. `main` local e `origin/main` devem existir.
5. A branch calculada não pode existir local nem remotamente.

Se qualquer condição falhar, pare e reporte o motivo. Não tente "corrigir" o repositório automaticamente.

## Interacao com humano

Antes da criacao da branch, confirme:

1. descricao curta que sera usada no slug;
2. branch base esperada (`main` por padrao);
3. se a execucao e apenas preparacao Git ou ja antecede o `/speckit.specify`.

Se o slug ficar ambiguo ou muito generico, proponha 1 alternativa curta e aguarde confirmacao.

## Padrão de branch

Formato obrigatório:

```text
feature/mmYYYY/descricao-curta
```

Exemplo em agosto de 2026:

```text
feature/082026/tratar-timeout-pbh
```

A descrição deve:

- ter de 2 a 5 termos significativos;
- usar minúsculas;
- remover acentos;
- substituir espaços por `-`;
- evitar IDs, frases longas e palavras genéricas como `alteracao` quando houver termo mais informativo.

## Execução determinística

Gere um slug curto e execute **uma única vez**:

```bash
python .github/skills/prepare-feature-branch/scripts/create_feature_branch.py --slug "<descricao-curta>"
```

O script executa a sequência:

```text
git status --porcelain
→ git remote get-url origin
→ git fetch origin
→ git switch main
→ git pull --ff-only origin main
→ validar main == origin/main
→ validar ausência da branch local/remota
→ git switch -c feature/mmYYYY/descricao-curta main
```

O JSON de saída contém:

- `status`;
- `branch`;
- `base_branch`;
- `base_commit`;
- `origin_url`.

## Baseline build opcional

A Skill antiga executava build completo antes da criação da branch porque já existia um DESIGN aprovado com `build_command`.

Nesta V2, a branch nasce **antes** de `/speckit.plan`, portanto não existe ainda um comando de build aprovado. Não invente um build.

Se o usuário ou a Constitution fornecer explicitamente um comando de baseline seguro, execute-o na `main` atualizada **antes** de criar a branch. Se falhar, não crie a branch.

## Próximo passo

Após sucesso, recomende:

```text
/speckit.specify <pedido>. Antes de escrever a spec, leia o HANDOFF correspondente.
```

Não execute `/speckit.specify` automaticamente.

## Resposta ao usuário

Informe apenas:

- `BRANCH_READY` ou bloqueio;
- branch criada;
- commit base;
- próximo comando recomendado.
