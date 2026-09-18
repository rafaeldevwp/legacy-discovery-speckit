# Política Git — Legacy Discovery + Spec Kit

## Regra de segurança

Nunca use automaticamente:

- `git stash`
- `git reset`
- `git merge`
- `git rebase`
- `git clean`
- `git push --force`
- exclusão de branch

Qualquer necessidade dessas operações exige decisão humana separada.

## Baseline

A branch de feature sempre nasce de `main` sincronizada por fast-forward:

```bash
git fetch origin
git switch main
git pull --ff-only origin main
```

Depois da atualização, `main` local deve apontar para o mesmo commit de `origin/main`.

## Nome

```text
feature/mmYYYY/descricao-curta
```

O mês/ano é calculado no ambiente local no instante da criação.

## Branch existente

Se o nome existir local ou remotamente, bloquear com `BRANCH_EXISTS`. Não incrementar, renomear, apagar ou reutilizar silenciosamente.

## Publicação

Esta Skill não faz push. Publicação pertence à etapa de implementação/revisão adotada pela equipe.

## Escopo de versionamento bloqueado

Para este fluxo, nenhum artefato gerado por skill pode ser versionado.

Bloqueio minimo por caminho:

- `.github/copilot-knowledge/`
- `.github/legacy-discovery/installation.json`

Mesmo fora desses caminhos, arquivos gerados por skill permanecem locais e nao podem ser publicados.

Se esses caminhos/arquivos estiverem tracked, remover do indice antes de qualquer publicacao.

Artefatos gerados pelo Spec Kit (`.specify/` e `specs/`) seguem a politica normal de versionamento da equipe.
