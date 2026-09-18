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
