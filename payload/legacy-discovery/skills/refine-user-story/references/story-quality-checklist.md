# Checklist de qualidade da história

Use para preencher `## Story Quality Assessment`. Cada critério recebe `OK` ou `GAP`. Todo `GAP` vira pelo menos uma ambiguidade `AMB-NN` — o checklist **não** autoriza você a reescrever a história.

## INVEST

| Critério | Pergunta | GAP típico |
|---|---|---|
| Independent | Pode ser entregue sem esperar outra história? | depende de outra US não entregue, de outro time, de outro repositório |
| Negotiable | Descreve o problema/necessidade, e não a implementação? | história já dita tabela, tela, endpoint, tecnologia |
| Valuable | Está claro quem ganha o quê? | sem persona, sem "para que" |
| Estimable | O time consegue dimensionar com o que está escrito + AS-IS? | área desconhecida, handoff `PARTIAL` |
| Small | Cabe em uma entrega curta? | vários fluxos, várias personas, "e também..." |
| Testable | Dá para provar que terminou? | sem critério de aceite, critérios subjetivos |

Se a história "dita a implementação" (Negotiable = GAP), registre a solução sugerida pelo PM como **restrição a confirmar** (`AMB-NN`: "a tela X é requisito ou sugestão?"), nunca como decisão.

Se Small = GAP, proponha fatias no `Execution Plan`, mas pergunte ao humano se a divisão é aceitável antes de `READY_FOR_SPECKIT` quando as fatias mudarem o que o usuário recebe.

## Definition of Ready

| Item | Pronto quando |
|---|---|
| Persona e valor explícitos | "como <persona>, quero <ação>, para <valor>" ou equivalente |
| Critérios de aceite do PM | existe ao menos um critério verificável escrito pelo PM |
| Dependências externas conhecidas | integrações/consumidores externos citados no handoff estão endereçados |
| Dados e privacidade | dado sensível tocado está identificado e tem regra |
| Comportamento em erro | ao menos o erro principal está descrito |
| Estado existente | está claro o que acontece com dados/registros já existentes |
| Base AS-IS | há `SPECKIT_HANDOFF` relacionado |

Itens de DoR que não se aplicam: marque `OK` e escreva `N/A — motivo` na observação.

## Sinais de alerta que sempre viram pergunta bloqueante

- a história muda regra de cálculo, valor, prazo ou elegibilidade;
- a história remove ou altera campo/contrato consumido fora do repositório;
- a história contradiz um `Compatibility Constraint` do handoff;
- a história menciona "igual ao sistema X" sem especificar;
- a história usa "todos", "sempre", "nunca" sobre dados legados.
