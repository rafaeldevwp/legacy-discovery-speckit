---
description: "Lista os comandos /legacy.*, mostra o estado das histórias e sugere o próximo passo."
argument-hint: "(opcional) HANDOFF-NNNN ou REFINEMENT-NNNN"
agent: agent
---

# AJUDA

## Objetivo
Orientar o usuário: quais comandos existem e qual é o próximo passo de cada história em andamento.

## Entradas Mínimas
- Nenhuma. Opcionalmente um ID de handoff ou refinamento.

## Passos
1. Execute `python .github/skill-contracts/scripts/story_status.py --root .github/copilot-knowledge` (acrescente `--id <ID>` se informado).
2. Mostre a tabela de comandos abaixo.
3. Para cada história em andamento, destaque o próximo comando indicado pelo script.

| Comando | Faz |
|---|---|
| `/legacy.story <história>` | Fluxo guiado: handoff → refinamento, parando nas decisões humanas |
| `/legacy.analyze <área>` | Mapeia o AS-IS (analyze-legacy-solution) |
| `/legacy.bug <sintoma>` | Investiga bug sem corrigir (investigate-legacy-bug) |
| `/legacy.impact <alvo>` | Raio de impacto (analyze-change-impact) |
| `/legacy.handoff <mudança>` | Gera o SPECKIT_HANDOFF (prepare-speckit-context) |
| `/legacy.refine <história>` | PO técnico gera o STORY_REFINEMENT (refine-user-story) |
| `/legacy.answer <REFINEMENT> <respostas>` | Registra respostas humanas às perguntas AMB-NN |
| `/legacy.approve <REFINEMENT> revisor: <nome>` | Registra sua revisão e libera READY_FOR_SPECKIT |
| `/legacy.branch <descrição>` | Cria a branch feature/mmYYYY/... (prepare-feature-branch) |
| `/legacy.status [ID]` | Estado das histórias e próximo comando |
| `/legacy.validate` | Valida contratos e reconstrói o INDEX |
| `/legacy.archive` | Arquiva artefatos locais das skills |

## Saída Obrigatória
- Tabela de comandos.
- Estado das histórias com o próximo comando de cada uma.

## Regras
- Somente leitura: não crie nem altere artefatos.
- Artefatos de skill são local-only: não faça stage, commit ou push de `.github/copilot-knowledge/`.
- Nunca escreva em `.specify/` ou `specs/`; isso pertence ao Spec Kit.
- Separe Evidência, Inferência e Lacuna. Não transforme inferência em fato.
- Não edite artefato de outro owner; registre `knowledge_updates`.
- Respeite todos os checkpoints de interação com humano da skill.
