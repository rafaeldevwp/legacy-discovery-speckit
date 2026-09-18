# Migração V1 → V2 (Discovery + Spec Kit)

## Objetivo

Eliminar a duplicidade entre o workflow próprio `SPEC-FIX → DESIGN-FIX → TASKS-FIX → execução` e o Spec Kit oficial, preservando todo o conhecimento legado já produzido.

## O que permanece ativo

- `analyze-legacy-solution`;
- `investigate-legacy-bug`;
- `analyze-change-impact`;
- `.github/copilot-knowledge/`;
- contratos e scripts de validação/indexação;
- artefatos V1 já existentes.

## O que muda

A V2 adiciona:

- `prepare-speckit-context`;
- `SPECKIT_HANDOFF`;
- Knowledge Gate por cobertura;
- orçamento explícito de discovery incremental;
- integração documentada com o Spec Kit.

## Skills V1 retiradas da descoberta automática

Foram movidas para `legacy-workflow/skills/`:

- `coordinate-fix`;
- `execute-fix-plan`;
- `run-solution-regression`.

Motivo: quando essas skills permanecem em `.github/skills/`, o agente pode escolher o workflow antigo e gerar uma segunda SPEC/DESIGN/TASKS paralela à `spec.md/plan.md/tasks.md` do Spec Kit.

## Artefatos V1 existentes

Não apague `fix-plans/`, RFCs ou relatórios antigos. Os scripts da V2 continuam aceitando esses tipos para auditoria e histórico.

A regra é apenas:

> não criar novos `SPEC-FIX`, `DESIGN-FIX`, `TASKS-FIX`, `EXECUTION-FIX`, `REGRESSION-FIX` ou `VERIFICATION-FIX` quando a iniciativa estiver sob Spec Kit.

## Novo fluxo

```text
Pedido de mudança
   ↓
Knowledge Preflight
   ↓
Discovery/Impact somente se houver gap
   ↓
SPECKIT_HANDOFF
   ↓
/speckit.specify
   ↓
/speckit.clarify
   ↓
/speckit.plan
   ↓
/speckit.tasks
   ↓
/speckit.analyze
   ↓
/speckit.implement
   ↓
/speckit.converge
```

## Instalação segura

1. Faça backup/commit da configuração atual.
2. Remova da `.github/skills/` ativa as três skills V1 arquivadas, se existirem.
3. Copie as quatro skills V2 e `skill-contracts`.
4. Preserve `.github/copilot-knowledge/` existente.
5. Rode `validate_artifacts.py` para confirmar compatibilidade do histórico.
6. Inicialize/atualize o Spec Kit separadamente.
7. Use `prepare-speckit-context` antes da primeira mudança relevante.


## V2.1 — Git branch gate restaurado

O comportamento Git que antes vivia dentro de `execute-fix-plan` volta como skill ativa independente `prepare-feature-branch`. O workflow antigo continua arquivado. O novo gate cria `feature/mmYYYY/descricao-curta` a partir de `main` sincronizada via fast-forward antes do `/speckit.specify`.

## V2.2 — Governança de artefatos e interatividade

- A criação de branch no fluxo de governança continua com a skill `prepare-feature-branch`.
- Artefatos gerados por skill passam a ser local-only por padrão; artefatos do Spec Kit seguem política normal do time.
- O instalador configura `.git/info/exclude` local para reduzir versionamento acidental de artefatos de skill.
- Foi adicionado o comando `archive_skill_artifacts.py` para arquivar e opcionalmente limpar artefatos/metadados de skill sem alterar arquivos de código do repositório.
- Skills ativas foram ajustadas com checkpoints de interação para reduzir ambiguidades antes de investigações custosas.
- `prepare-speckit-context` reforça guardrails para `/speckit.constitution` e `/speckit.plan` respeitarem AS-IS e arquitetura existente.
