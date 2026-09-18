# Comandos /legacy.*

Prompt files do GitHub Copilot instalados em `.github/prompts/`. No chat (Agent Mode), digite `/legacy.` para ver a lista.

Eles não substituem as skills: cada comando é um atalho que carrega a skill certa com as entradas certas, e os guardrails continuam nas skills e nos scripts de contrato.

| Comando | Skill / script |
|---|---|
| `/legacy.help` | Lista os comandos /legacy.*, mostra o estado das histórias e sugere o próximo passo. |
| `/legacy.analyze` | Mapeia o AS-IS de uma área do legado com a skill analyze-legacy-solution. |
| `/legacy.bug` | Investiga um bug no legado com a skill investigate-legacy-bug (localiza, não corrige). |
| `/legacy.impact` | Mapeia o raio de impacto de uma mudança com a skill analyze-change-impact. |
| `/legacy.handoff` | Gera o SPECKIT_HANDOFF (AS-IS da mudança) com a skill prepare-speckit-context. |
| `/legacy.refine` | PO técnico: refina a história do PM e gera o STORY_REFINEMENT com a skill refine-user-story. |
| `/legacy.answer` | Registra as respostas humanas às perguntas AMB-NN de um refinamento. |
| `/legacy.approve` | Registra a revisão humana de um refinamento e o libera como READY_FOR_SPECKIT, se os guardrails passarem. |
| `/legacy.branch` | Cria a branch feature/mmYYYY/descricao-curta a partir da main atualizada (prepare-feature-branch). |
| `/legacy.story` | Fluxo guiado de uma história do PM: handoff → refinamento, parando em cada decisão humana. |
| `/legacy.status` | Mostra o estado de cada história (handoff, refinamento, perguntas abertas) e o próximo comando. |
| `/legacy.validate` | Valida os contratos dos artefatos das skills e reconstrói o INDEX. |
| `/legacy.archive` | Arquiva os artefatos locais das skills num ZIP fora do repositório (e opcionalmente limpa). |

Fluxo típico de uma história do PM:

```text
/legacy.story <história>  →  /legacy.answer …  →  /legacy.approve REFINEMENT-NNNN revisor: <nome>
→  /legacy.branch <descrição>  →  /speckit.specify …
```

O prefixo `legacy.` evita colisão com os comandos do Spec Kit. O instalador só escreve arquivos `legacy.*.prompt.md`; outros prompts em `.github/prompts/` não são tocados.
