# Convenção de nomes dos artefatos

A fonte de verdade para nomes é:

```text
.github/skill-contracts/artifact-naming.md
```

Este arquivo existe apenas como referência local da skill para manter compatibilidade com instalações antigas.

Na V2, os artefatos ativos desta skill são:

- `SOLUTION-OVERVIEW.md`;
- `PROJECT-{project-slug}.md`;
- `ADR-{NNNN}-{slug}.md`;
- `DEEP-DIVE-{project-slug}-{class-slug}.md`.

A integração com o Spec Kit usa `HANDOFF-{NNNN}-{slug}.md`, cujo owner é `prepare-speckit-context`.

Não crie novos `SPEC-FIX`, `DESIGN-FIX`, `TASKS-FIX` ou RFCs de modernização por esta skill quando o repositório estiver usando a V2 + Spec Kit.
