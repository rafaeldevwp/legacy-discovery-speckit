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
