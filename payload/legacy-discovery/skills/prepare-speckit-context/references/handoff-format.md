# Formato do SPECKIT_HANDOFF

O handoff é um **contrato de contexto AS-IS**. Ele não é uma spec, um design ou um plano de implementação.

## Nome e local

```text
.github/copilot-knowledge/handoffs/HANDOFF-{NNNN}-{slug}.md
```

## Frontmatter obrigatório

```yaml
---
schema_version: 1
artifact_type: SPECKIT_HANDOFF
id: HANDOFF-0001
status: READY_FOR_SPECKIT
owner_skill: prepare-speckit-context
created_at: 2026-08-28T12:00:00Z
updated_at: 2026-08-28T12:00:00Z
request: "descrição curta da mudança"
target_flow: SDD
confidence: HIGH
source_access: NONE
---
```

Valores válidos:

- `status`: `READY_FOR_SPECKIT`, `PARTIAL`, `BLOCKED`;
- `target_flow`: `SDD`, `BUG`;
- `confidence`: `HIGH`, `MEDIUM`, `LOW`;
- `source_access`: `NONE`, `BOUNDED`.

## Corpo obrigatório

```markdown
# Handoff para Spec Kit — <título>

## Request

<pedido original resumido sem reinterpretar solução>

## Knowledge Coverage

| Dimension | Status | Basis |
|---|---|---|
| STRUCTURE | COVERED | PROJECT-x |
| CURRENT_BEHAVIOR | COVERED | DEEP-DIVE-x |
| BUSINESS_RULES | PARTIAL | INVESTIGATION-x |
| DEPENDENCIES | COVERED | SOLUTION-OVERVIEW |
| IMPACT_SURFACE | COVERED | IMPACT-x |
| EXTERNAL_BOUNDARIES | COVERED | SOLUTION-OVERVIEW |
| TEST_SAFETY_NET | PARTIAL | test inventory |

## Current Behavior

Somente fatos do AS-IS relevantes para a mudança.

## Relevant Components

- componente/projeto/método relevante;
- responsabilidade atual observada.

## Existing Business Rules

- regras observáveis existentes;
- se inferida, marque explicitamente `INFERRED` e cite a evidência.

## Compatibility Constraints

- contratos e comportamentos existentes que o planejamento deve considerar;
- não prescreva a solução.

## Impact Surface

- dependentes diretos;
- dependentes indiretos;
- documentação/testes possivelmente afetados.

## External Boundaries

- consumidores ou serviços fora do repositório;
- o que não foi possível validar localmente.

## Test Safety Net

- testes existentes relevantes;
- gaps de cobertura conhecidos.

## Evidence

- `PROJECT-x` — <fato sustentado>;
- `DEEP-DIVE-x` — <fato sustentado>;
- `path/to/File.cs:linha` — somente quando source foi necessário.

## Unknowns

### Blocking

- `NONE`, ou liste os unknowns que impedem prontidão.

### Non-blocking

- unknowns que o Spec Kit deve manter explícitos/validar no planejamento.

## Explicitly Not Decided

Esta seção deve deixar claro o que **não** foi decidido no Discovery, por exemplo:

- arquitetura TO-BE;
- nova abstração/camada;
- biblioteca/tecnologia;
- estratégia de migração;
- decomposição em tasks.

## Spec Kit Handoff

### Target flow

`SDD` ou `BUG`.

### Suggested invocation

<comando sugerido, apontando este handoff como contexto obrigatório>
```

## Critérios de qualidade

Um handoff `READY_FOR_SPECKIT` deve:

1. separar fato, inferência e unknown;
2. citar evidência suficiente para os pontos críticos;
3. explicitar limites externos;
4. mostrar raio de impacto conhecido;
5. não conter design TO-BE;
6. ter `Blocking: NONE`;
7. não depender de uma leitura global do repositório para ser compreendido.
