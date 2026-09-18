# Planejamento de execução (refinamento técnico)

O `## Execution Plan` diz **em que ordem** a história será entregue, **o que cada passo prova** e **qual ferramenta** o executa. Ele não diz **como** o código será escrito — isso é do `/speckit.plan` e do `/speckit.tasks`.

| Pertence ao refinamento | Pertence ao Spec Kit |
|---|---|
| fatias de valor e sua ordem | arquitetura, design, classes, camadas |
| AC e GR cobertos por fatia | tasks de código e arquivos a alterar |
| pré-requisitos de rede de proteção | escolha de biblioteca/padrão |
| passo do ferramental por fatia | estimativa detalhada |
| considerações técnicas **não vinculantes** | decisão sobre essas considerações |

## 1. Fatiar

Prefira fatias **verticais** (cada uma entrega comportamento observável e testável) a fatias por camada ("fazer o banco", "fazer a tela").

Heurísticas, na ordem:

1. **Rede de proteção primeiro** — se algum `GR-NN` tem `Proof: CHARACTERIZATION_TEST_REQUIRED`, a primeira fatia cria esses testes contra o comportamento **atual**, antes de qualquer mudança. Ela nasce verde.
2. **Caminho feliz mínimo** — o menor fluxo que entrega o valor principal.
3. **Variações de regra** — cada variação de negócio relevante em sua fatia.
4. **Erros e bordas** — timeout, dado ausente, duplicidade.
5. **Dados existentes** — migração/reprocessamento, se o humano decidiu que existe.

Regras:

- toda fatia cita ao menos um `AC-NN`;
- todo `AC-NN` aparece em alguma fatia;
- todo `GR-NN` aparece em alguma fatia (normalmente na primeira e em toda fatia que toca aquela área);
- `Depends on` só cita fatias existentes; sem ciclos;
- se a divisão muda o que o usuário recebe em cada entrega, a divisão é uma pergunta ao humano.

## 2. Guardrails de regressão

Para cada comportamento atual que a história pode tocar (use `Compatibility Constraints`, `Impact Surface` e `Test Safety Net` do handoff):

| Situação | Proof |
|---|---|
| existe teste automatizado que cobre | `EXISTING_TEST:<caminho::teste>` |
| não existe teste e é automatizável | `CHARACTERIZATION_TEST_REQUIRED` |
| não é automatizável agora (integração externa, relatório) | `MANUAL_CHECK:<o que verificar e onde>` |

Consumidor externo não visível no repositório **sempre** vira guardrail `MANUAL_CHECK` ou pergunta ao humano — nunca é ignorado.

## 3. Coluna Toolchain

Cite o ferramental real do pacote, sem inventar comando:

| Situação da fatia | Toolchain |
|---|---|
| AS-IS insuficiente para a área | `prepare-speckit-context` (novo handoff/atualização) |
| raio de impacto desconhecido | `analyze-change-impact` |
| comportamento atual suspeito de bug | `investigate-legacy-bug` |
| entrega normal | `/speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.analyze → /speckit.implement → /speckit.converge` |
| bug pontual com extensão oficial | `/speckit.bug.assess → /speckit.bug.fix → /speckit.bug.test` |

A branch (`prepare-feature-branch`) é criada uma vez, antes do `/speckit.specify`, não por fatia — salvo decisão do time.

## 4. Considerações técnicas não vinculantes

Pode listar, com evidência, pontos que o `/speckit.plan` precisa decidir:

- "o cálculo hoje está duplicado em A e B (`path:linha`) — o plan precisa decidir se altera ambos";
- "a tabela X não tem índice por Y — impacto de performance a avaliar".

Não pode escrever: "usar a biblioteca Z", "criar um serviço novo", "aplicar o padrão W". Se sentir necessidade, registre como pergunta para o plan, não como decisão.

## 5. Sinais de tamanho

Liste fatores objetivos de complexidade (nº de projetos tocados, consumidores externos, ausência de testes, migração de dados). Não converta em horas ou pontos — isso é do time.
