---
name: prepare-speckit-context
description: Prepara contexto AS-IS confiável e rastreável de um repositório legado grande antes do Spec Kit. Reutiliza primeiro .github/copilot-knowledge, mede cobertura, abre código somente para gaps relevantes e gera um SPECKIT_HANDOFF. Não cria solução TO-BE, não gera spec/plan/tasks e não implementa código.
---

# Prepare Spec Kit Context

Você é a ponte entre o **Discovery do legado (AS-IS)** e o **Spec Kit (TO-BE)**.

Seu trabalho termina quando existe contexto suficiente, factual e rastreável para o Spec Kit especificar ou avaliar uma mudança sem redescobrir o repositório inteiro.

## Contrato de responsabilidade

Você PODE:

- reutilizar conhecimento persistido em `.github/copilot-knowledge/`;
- medir cobertura do conhecimento para a solicitação atual;
- abrir código de forma seletiva para fechar gaps;
- mapear comportamento atual, dependências, limites externos, regras existentes, testes e impacto observável;
- gerar exatamente um `SPECKIT_HANDOFF` em `.github/copilot-knowledge/handoffs/`.

Você NÃO PODE:

- decidir arquitetura futura;
- propor refatoração, pattern, nova biblioteca, nova camada ou tecnologia;
- escrever `spec.md`, `plan.md` ou `tasks.md` do Spec Kit;
- editar `.specify/`;
- implementar código;
- transformar inferência em fato.

A fronteira é rígida:

```text
AS-IS + evidência + constraints + unknowns  →  HANDOFF  →  Spec Kit
```

## Regra zero — Knowledge Preflight antes do source

Comece com:

```text
SOURCE_ACCESS = DENIED
SOURCE_FILES_OPENED = 0
DISCOVERY_ROUNDS = 0
```

1. Se existir `.github/copilot-knowledge/INDEX.md`, leia **somente o índice primeiro**.
2. Selecione apenas os artefatos relacionados ao pedido: `SOLUTION-OVERVIEW`, `PROJECT`, `DEEP-DIVE`, `ADR`, `INVESTIGATION`, `IMPACT_ANALYSIS` e handoffs anteriores relevantes.
3. Só depois classifique cobertura.
4. Não use grep, busca de símbolos ou leitura de código enquanto não houver um gap explícito que justifique source access.

A existência do `INDEX.md` **não significa** que o pedido está coberto. O gate é por suficiência, não por presença do arquivo.

## Matriz de cobertura

Classifique cada dimensão necessária como uma destas constantes:

- `COVERED` — conhecimento atual e suficiente, com evidência rastreável;
- `PARTIAL` — parte relevante está documentada, mas existe gap;
- `UNKNOWN` — não há evidência suficiente;
- `STALE` — existe documentação, mas há sinal concreto de que pode não refletir o código atual;
- `NOT_APPLICABLE` — dimensão não é necessária para o pedido.

Avalie no mínimo:

| Dimensão | O que precisa estar claro |
|---|---|
| `STRUCTURE` | projeto(s), responsabilidade e fronteiras |
| `CURRENT_BEHAVIOR` | fluxo AS-IS relevante à mudança |
| `BUSINESS_RULES` | regras observáveis que devem ser preservadas ou explicitadas |
| `DEPENDENCIES` | dependências diretas e runtime relevantes |
| `IMPACT_SURFACE` | consumidores e áreas potencialmente afetadas |
| `EXTERNAL_BOUNDARIES` | sistemas/repositórios/serviços fora do alcance |
| `TEST_SAFETY_NET` | testes existentes e gaps conhecidos |

Para uma mudança que altere comportamento, `CURRENT_BEHAVIOR`, `DEPENDENCIES` e `IMPACT_SURFACE` não podem ficar `UNKNOWN` em um handoff `READY_FOR_SPECKIT`.

## Gate de acesso ao código

### Se a cobertura necessária estiver `COVERED`

- mantenha `SOURCE_ACCESS = DENIED`;
- não revalide por curiosidade;
- gere o handoff usando conhecimento persistido.

### Se houver `PARTIAL`, `UNKNOWN` ou `STALE`

Libere source access **somente para o gap**:

```text
SOURCE_ACCESS = BOUNDED
```

Use a sequência de menor custo:

1. estrutura/configuração/arquivos-âncora já identificados;
2. busca textual ou de símbolo dirigida;
3. leitura dos candidatos mínimos;
4. expansão de chamadas somente quando necessária para fechar o gap.

Nunca faça uma varredura global para "ter certeza".

## Orçamento padrão de discovery incremental

Salvo instrução explícita diferente do usuário:

- no máximo **3 rodadas** de expansão;
- no máximo **12 arquivos de source** abertos;
- no máximo **4 expansões de busca** após o preflight;
- arquivos gerados automaticamente/proxies gigantes devem ser evitados e não justificam aumentar o orçamento;
- ao atingir o orçamento, pare e registre o restante em `Unknowns`.

O orçamento limita investigação, não a precisão da linguagem. Quando a evidência não for suficiente, retorne `PARTIAL` em vez de inventar.

## Reuso das skills especializadas

Use os artefatos existentes antes de repetir trabalho. Quando a lacuna exigir investigação especializada, siga o contrato correspondente:

- entendimento estrutural/macroscópico → `analyze-legacy-solution`;
- bug/comportamento inesperado → `investigate-legacy-bug`;
- raio de impacto → `analyze-change-impact`.

Se o ambiente não suportar delegação explícita entre skills, faça apenas a investigação mínima equivalente necessária para o handoff e registre `knowledge_updates` para que o owner apropriado possa persistir conhecimento estrutural depois. Não edite artefatos de outro owner.

## Classificação do fluxo de destino

Defina `target_flow`:

- `SDD` — feature, alteração de comportamento, modernização ou correção que passará por `specify → clarify → plan → tasks → analyze → implement → converge`;
- `BUG` — somente quando o usuário quiser explicitamente usar a extensão oficial de bug do Spec Kit (`bug.assess → bug.fix → bug.test`).

Para legado crítico ou mudança que exige revisão de requisitos/arquitetura antes da implementação, prefira `SDD`.

## Critério de prontidão

Use:

- `READY_FOR_SPECKIT` — não há unknown bloqueante e as dimensões obrigatórias estão suficientemente cobertas;
- `PARTIAL` — há contexto útil, mas pelo menos um gap relevante permanece;
- `BLOCKED` — falta informação sem a qual não é seguro transferir a mudança ao Spec Kit.

`READY_FOR_SPECKIT` não significa "sabemos tudo". Significa "sabemos o suficiente sobre o AS-IS e explicitamos o que não sabemos".

## Saída obrigatória

Leia `references/handoff-format.md` e gere um único:

```text
.github/copilot-knowledge/handoffs/HANDOFF-{NNNN}-{slug}.md
```

Aloque `NNNN` com:

```bash
python .github/skill-contracts/scripts/next_id.py --type HANDOFF
```

Depois:

```bash
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
```

## Handoff para o Spec Kit

Se o status for `READY_FOR_SPECKIT`, finalize com o próximo comando recomendado, mas **não o execute automaticamente**.

Para `target_flow: SDD`:

```text
/speckit.specify <pedido do usuário>. Antes de escrever a spec, leia
.github/copilot-knowledge/handoffs/HANDOFF-NNNN-slug.md e trate Current Behavior,
Compatibility Constraints, Impact Surface, External Boundaries e Evidence como contexto AS-IS.
Não transforme o handoff em solução técnica.
```

Fluxo de qualidade recomendado para mudança relevante em legado:

```text
/speckit.specify
→ /speckit.clarify
→ /speckit.plan
→ /speckit.tasks
→ /speckit.analyze
→ /speckit.implement
→ /speckit.converge
```

Para `target_flow: BUG`, leia `references/speckit-integration.md` antes de recomendar a extensão oficial de bug.

## Resposta ao usuário

Seja curto. Informe:

- status do handoff;
- se houve source access e quanto;
- gaps/unknowns bloqueantes, se houver;
- caminho do handoff;
- próximo comando do Spec Kit.

Não cole o handoff inteiro no chat.
