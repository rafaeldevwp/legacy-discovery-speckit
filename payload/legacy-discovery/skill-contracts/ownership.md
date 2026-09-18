# Artifact ownership contract

Each artifact type has one writer. Other skills may read it or record a requested change in their own output, but must not edit it.

## V2 active ownership

| Artifact/source | Owner |
|---|---|
| `SOLUTION-OVERVIEW`, `PROJECT`, `ADR`, `DEEP-DIVE` | `analyze-legacy-solution` |
| `INVESTIGATION` and the bug-demonstrating test | `investigate-legacy-bug` |
| `IMPACT` | `analyze-change-impact` |
| `SPECKIT_HANDOFF` | `prepare-speckit-context` |
| Git branch `feature/mmYYYY/descricao-curta` | `prepare-feature-branch` |
| `INDEX.md` | deterministic `sync_index.py` script |
| Spec Kit `spec.md`, `plan.md`, `tasks.md` and managed `.specify/` artifacts | **Spec Kit**, nunca estas skills |

## V1 compatibility ownership

Artefatos existentes continuam com seus owners históricos para validação e auditoria:

| Artifact/source | Legacy owner |
|---|---|
| `RFC` | `analyze-legacy-solution` |
| `FIX_SPEC`, `FIX_DESIGN`, `FIX_TASKS`, `FIX_VERIFICATION` | `coordinate-fix` |
| `FIX_EXECUTION` | `execute-fix-plan` |
| `FIX_REGRESSION` | `run-solution-regression` |

As skills V1 estão arquivadas fora da pasta ativa na distribuição V2.

## Knowledge deltas

If a non-owner discovers stale or missing structural knowledge, it records a `knowledge_updates` entry in its own artifact:

```yaml
knowledge_updates:
  - target_type: DEEP_DIVE
    target: PROJECT-x / ClassY
    reason: comportamento observado durante investigação
```

The owner applies the delta in a later explicit refresh. Never silently cross-write another owner's artifact.

## Regra de fronteira com Spec Kit

Nenhuma skill desta camada escreve diretamente em `.specify/` ou altera artefatos gerenciados pelo Spec Kit. A integração acontece exclusivamente por leitura/referência de `SPECKIT_HANDOFF`.

O fluxo de governanca de branch continua sob responsabilidade da skill `prepare-feature-branch`.

## Politica global de privacidade e versionamento

Para esta funcionalidade, artefatos gerados por skill devem permanecer locais.
Artefatos gerados pelo Spec Kit seguem a politica normal de versionamento do time.

Regras obrigatorias:

1. Nao fazer staging/commit/push de qualquer arquivo gerado por skill, independentemente do caminho.
2. Tratar como local-only, no minimo, `.github/copilot-knowledge/` e `.github/legacy-discovery/installation.json`.
3. Se algum artefato de skill estiver tracked, remover do indice com `git rm --cached` antes de publicar alteracoes.
4. Se uma skill gerar artefato fora desses caminhos (ex.: teste temporario de investigacao), o arquivo tambem permanece local e nao pode ser publicado.
5. Artefatos de Spec Kit em `.specify/` e `specs/` nao entram neste bloqueio por padrao.
6. Esta politica tem precedencia sobre instrucoes operacionais locais de qualquer skill.
