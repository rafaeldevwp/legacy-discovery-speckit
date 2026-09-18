# Instalação rápida

Este ZIP contém o pacote V2 pronto para mesclar na pasta `.github` do seu repositório.

Copie:

```text
skills/          → .github/skills/
skill-contracts/ → .github/skill-contracts/
```

Preserve a pasta `.github/copilot-knowledge/` existente.

`legacy-workflow/` é somente backup do workflow V1 e **não deve** ser copiado para `.github/skills/` se o Spec Kit será a fonte de verdade para SDD.

Depois de instalar, consulte `skills/README.md` e `MIGRATION-V2.md`.


A V2.1 inclui também `.github/skills/prepare-feature-branch/`, responsável somente pelo baseline Git e criação da branch `feature/mmYYYY/descricao-curta`.

## Atualização V2.2 (pacote v4)

- Artefatos gerados por skill permanecem local-only por padrão.
- Artefatos do Spec Kit (`.specify/` e `specs/`) seguem a política normal de versionamento do time.
- O instalador configura `.git/info/exclude` para reduzir stage acidental de artefatos de skill.
- Para arquivar e limpar dados da skill sem tocar código do repositório:

```bash
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive-and-clean
```

## Atualização V2.3 (bundle 1.3.0) — incluída na V2.4

- Nova skill `.github/skills/refine-user-story/` (PO técnico que refina a história do PM).
- Novo diretório local-only `.github/copilot-knowledge/refinements/`.
- Novo script `.github/skill-contracts/scripts/refinement_rules.py` (usado por `validate_artifacts.py`).
- Novo script somente-leitura `.github/skill-contracts/scripts/story_status.py`.
- Comandos `/legacy.*`: copie `prompts/legacy.*.prompt.md` → `.github/prompts/` (o instalador faz isso). Não copie o `README.md` de `prompts/`.
- Nenhuma skill anterior foi alterada. Atualizar a partir da V2.2 preserva `.github/copilot-knowledge/`.

## Atualização V2.4 (bundle 1.4.0)

- Novo agente `.github/agents/legacy-discovery.agent.md` com o hook `.github/hooks/legacy_governance.py` (a fechadura).
  O instalador só grava esses dois arquivos; hooks e agentes de outros pacotes (ex.: AgentQA) não são tocados.
- Os comandos `/legacy.*` passam a rodar nesse agente.
- Novo script humano `.github/skill-contracts/scripts/approve_refinement.py`; novo status `READY_FOR_REVIEW`.
- `validate_artifacts.py` confere evidência quando a base está em `<repo>/.github/copilot-knowledge`.
- Refinamentos aprovados na V2.3 continuam válidos, com `WARNING` pedindo reaprovação para selar.
