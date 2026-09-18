# Formato do STORY_REFINEMENT

O refinamento é um **contrato de clareza** entre a história do PM e o Spec Kit. Ele não é spec, não é plan e não é lista de tasks de código. Tudo que está aqui em formato de tabela é verificado por `validate_artifacts.py` — siga os cabeçalhos e os IDs exatamente.

## Nome e local

```text
.github/copilot-knowledge/refinements/REFINEMENT-{NNNN}-{slug}.md
```

Uma história = um arquivo. Novas rodadas de resposta atualizam o mesmo arquivo e incrementam `revision`.

## Frontmatter obrigatório

```yaml
---
schema_version: 1
artifact_type: STORY_REFINEMENT
id: REFINEMENT-0001
status: AWAITING_HUMAN
owner_skill: refine-user-story
created_at: 2026-09-18T12:00:00Z
updated_at: 2026-09-18T12:00:00Z
story_ref: "US-1234"
handoff: HANDOFF-0003
revision: 1
decision_owner: "PM"
open_questions: 2
source_access: NONE
reviewed_by: null
reviewed_at: null
block_reason: null
---
```

| Campo | Regra |
|---|---|
| `status` | `READY_FOR_SPECKIT`, `AWAITING_HUMAN` ou `BLOCKED` |
| `story_ref` | ID do work item do PM, ou `UNSPECIFIED` |
| `handoff` | `HANDOFF-NNNN` existente na base, ou `NONE` |
| `revision` | inteiro ≥ 1; incrementa a cada rodada |
| `decision_owner` | quem responde pelas decisões de negócio |
| `open_questions` | **igual** ao número de linhas `OPEN_HUMAN` no registro |
| `source_access` | `NONE` ou `BOUNDED` |
| `reviewed_by` / `reviewed_at` | `null` até o humano confirmar a revisão nesta conversa; obrigatórios em `READY_FOR_SPECKIT` |
| `block_reason` | `null`, ou código de `failure-policy.md`; obrigatório em `BLOCKED` |

## Corpo obrigatório

Os títulos `##` abaixo são obrigatórios, nesta grafia.

```markdown
# Refinamento — <título curto da história>

## Story (verbatim)

> Texto da história exatamente como o PM escreveu. Nunca editado depois do intake.

## Story Quality Assessment

| Critério | Resultado | Observação |
|---|---|---|
| Independent | OK / GAP | ... |
| Negotiable | OK / GAP | ... |
| Valuable | OK / GAP | ... |
| Estimable | OK / GAP | ... |
| Small | OK / GAP | ... |
| Testable | OK / GAP | ... |
| DoR: persona e valor explícitos | OK / GAP | ... |
| DoR: critérios de aceite do PM | OK / GAP | ... |
| DoR: dependências externas conhecidas | OK / GAP | ... |

Todo `GAP` gera pelo menos um `AMB-NN`.

## AS-IS Basis

- `FACT` — <fato> — `HANDOFF-0003` / `IMPACT-...` / `path/File.cs:42`
- `INFERRED` — <inferência> — <evidência>
- `UNKNOWN` — <o que ninguém sabe ainda>

## Scope

### In scope
- ...

### Out of scope
- ... (itens fora de escopo que alguém poderia supor que estão dentro)

## Ambiguity Register

| ID | Question | Why it matters | Source | Status | Blocking | Evidence / Answer |
|---|---|---|---|---|---|---|
| AMB-01 | ... | ... | KNOWLEDGE | RESOLVED_BY_EVIDENCE | NO | HANDOFF-0003 § Current Behavior |
| AMB-02 | ... | ... | HUMAN | OPEN_HUMAN | YES | - |
| AMB-03 | ... | ... | HUMAN | ANSWERED_BY_HUMAN | YES | "Resposta literal" — PM, 2026-09-18 |

## Human Decisions Required

Perguntas abertas no formato de `ambiguity-protocol.md`, uma por `AMB-NN` com `OPEN_HUMAN`.
Se não houver nenhuma, escreva `NONE`.

## Acceptance Criteria

| ID | Given / When / Then | Origin |
|---|---|---|
| AC-01 | Dado ..., quando ..., então ... | STORY |
| AC-02 | Dado ..., quando ..., então ... | HUMAN:AMB-03 |
| AC-03 | Dado ..., quando ..., então ... (comportamento atual mantido) | AS-IS:HANDOFF-0003 |

## Regression Guardrails

| ID | Preserved behavior | Evidence | Proof |
|---|---|---|---|
| GR-01 | ... | HANDOFF-0003 § Compatibility Constraints | EXISTING_TEST:tests/X/YTests.cs::Metodo |
| GR-02 | ... | `path/File.cs:88` | CHARACTERIZATION_TEST_REQUIRED |

Se genuinamente nenhum comportamento existente for tocado, escreva uma linha
`NO_EXISTING_BEHAVIOR_AFFECTED — <justificativa com evidência>` no lugar da tabela.

## Risks and Dependencies

- risco / dependência — probabilidade/impacto qualitativo — evidência — quem trata.

## Execution Plan

| Slice | Goal | AC | GR | Toolchain | Depends on |
|---|---|---|---|---|---|
| SLICE-01 | Rede de proteção | AC-03 | GR-02 | /speckit.tasks → teste de caracterização primeiro | - |
| SLICE-02 | ... | AC-01, AC-02 | GR-01 | /speckit.specify → ... → /speckit.implement | SLICE-01 |

### Non-binding technical considerations

- pontos de atenção para o `/speckit.plan` decidir — nunca decisão tomada.

### Size signals

- sinais qualitativos de tamanho/complexidade (não é estimativa de horas).

## Explicitly Not Decided

- arquitetura TO-BE, biblioteca/tecnologia, decomposição em tasks de código;
- qualquer decisão de negócio ainda `OPEN_HUMAN`.

## Next Steps

1. passo recomendado, sem executar.
```

## Valores válidos nas tabelas

| Coluna | Valores |
|---|---|
| Ambiguity `Source` | `STORY`, `KNOWLEDGE`, `CODE`, `HUMAN` |
| Ambiguity `Status` | `RESOLVED_BY_EVIDENCE`, `OPEN_HUMAN`, `ANSWERED_BY_HUMAN`, `ASSUMPTION_ACCEPTED` |
| Ambiguity `Blocking` | `YES`, `NO` |
| AC `Origin` | `STORY`, `HUMAN:AMB-NN`, `AS-IS:<referência>` |
| GR `Proof` | `EXISTING_TEST:<referência>`, `CHARACTERIZATION_TEST_REQUIRED`, `MANUAL_CHECK:<descrição>` |

Regras entre colunas:

- `RESOLVED_BY_EVIDENCE` → `Source` diferente de `HUMAN` e evidência preenchida;
- `OPEN_HUMAN`, `ANSWERED_BY_HUMAN`, `ASSUMPTION_ACCEPTED` → `Source` = `HUMAN`;
- `ANSWERED_BY_HUMAN` e `ASSUMPTION_ACCEPTED` → resposta/aceite registrado com quem e quando;
- `ASSUMPTION_ACCEPTED` só existe quando o humano **aceitou explicitamente** a suposição proposta.

## O que o validador exige

Sempre:

- frontmatter e seções obrigatórias;
- valores válidos nas tabelas e regras entre colunas;
- `open_questions` igual ao número de `OPEN_HUMAN`;
- `handoff` aponta para um `SPECKIT_HANDOFF` existente (ou `NONE`);
- `AWAITING_HUMAN` tem ao menos uma `OPEN_HUMAN`; `BLOCKED` tem `block_reason`.

Adicionalmente em `READY_FOR_SPECKIT`:

- `handoff` existe e está `READY_FOR_SPECKIT`;
- nenhuma `OPEN_HUMAN` com `Blocking: YES`;
- `reviewed_by` e `reviewed_at` preenchidos (ISO-8601);
- ao menos um `AC-NN`, todos com `Origin` válida; `HUMAN:AMB-NN` aponta para ambiguidade respondida ou aceita;
- guardrails presentes (tabela ou `NO_EXISTING_BEHAVIOR_AFFECTED`);
- ao menos uma `SLICE-NN`; toda fatia cita AC existente; todo AC e todo GR aparecem em alguma fatia; `Depends on` só cita fatias existentes.

## Critérios de qualidade

1. A história original está intacta e separada da interpretação.
2. Nenhum AC nasce de suposição não confirmada.
3. Fato, inferência e unknown estão rotulados.
4. Toda pergunta ao humano é fechada, com opções e consequência.
5. Todo comportamento atual tocado tem prova de não-regressão planejada.
6. Nada de arquitetura TO-BE, biblioteca ou tasks de código.
