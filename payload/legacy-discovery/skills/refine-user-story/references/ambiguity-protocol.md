# Protocolo de ambiguidades

Ambiguidade é qualquer ponto em que duas pessoas razoáveis, lendo a mesma história, construiriam comportamentos diferentes. O objetivo não é eliminar todas — é garantir que **nenhuma seja resolvida por suposição silenciosa**.

## 1. Como encontrar

Procure, na história e nos critérios do PM:

| Sinal | Exemplo |
|---|---|
| termo vago | "rápido", "adequado", "quando necessário", "etc." |
| sujeito oculto | "deve ser notificado" — quem? por qual canal? |
| regra sem limite | "permitir desconto" — até quanto? para quem? |
| caminho feliz só | nada sobre erro, timeout, dado ausente, duplicidade |
| estado não definido | o que acontece com registros já existentes? |
| conflito com AS-IS | o handoff diz que hoje X; a história pede Y sem dizer que X muda |
| contrato externo | toca API, arquivo, fila, relatório consumido fora do repositório |
| dado sensível | CPF, dado financeiro, dado de saúde, log de dado pessoal |
| permissão | quem pode fazer, quem pode ver |
| migração | dado legado precisa ser convertido, recalculado, reprocessado? |
| critério de pronto | não há como saber, por teste, que terminou |

Cada `GAP` do checklist de qualidade também é uma ambiguidade.

## 2. Classificar a fonte de resolução

Pergunte: **essa dúvida é sobre o presente ou sobre o futuro desejado?**

| Tipo de dúvida | Fonte possível |
|---|---|
| "Como o sistema faz isso hoje?" | `STORY` → `KNOWLEDGE` → `CODE` |
| "Quem consome isso hoje?" | `KNOWLEDGE` (IMPACT/HANDOFF) → `CODE` |
| "Existe teste cobrindo isso?" | `KNOWLEDGE` (Test Safety Net) → `CODE` |
| "Como deveria funcionar?" | `HUMAN` — sempre |
| "Isso está no escopo?" | `HUMAN` — sempre |
| "O comportamento atual deve mudar?" | `HUMAN` — sempre |
| "Qual o valor/limite/regra de negócio nova?" | `HUMAN` — sempre |

Código nunca responde intenção. Encontrar um `if` no legado prova o que acontece hoje, não o que o PM quer amanhã.

## 3. Escada de resolução

```text
STORY ──resolve?──► RESOLVED_BY_EVIDENCE (evidência: trecho da história)
  │ não
KNOWLEDGE ──resolve?──► RESOLVED_BY_EVIDENCE (evidência: ID do artefato + seção)
  │ não
CODE (só fato AS-IS, dentro do orçamento) ──resolve?──► RESOLVED_BY_EVIDENCE (evidência: path:linha)
  │ não / orçamento esgotado / é intenção
HUMAN ──► OPEN_HUMAN ──resposta──► ANSWERED_BY_HUMAN
                     └─aceita sugestão──► ASSUMPTION_ACCEPTED
```

Uma resolução por evidência precisa de evidência **citável**. "Parece que" não resolve: vira `INFERRED` na base AS-IS e a ambiguidade continua subindo a escada.

## 4. Quando é bloqueante (`Blocking: YES`)

Marque `YES` se, sem a resposta:

- um critério de aceite não pode ser escrito ou testado;
- há risco de alterar comportamento existente sem intenção;
- há contrato externo, dado sensível, regra financeira/regulatória envolvida;
- duas fatias possíveis levariam a entregas diferentes para o usuário;
- a história conflita com o AS-IS.

Marque `NO` somente quando a resposta pode ser tomada durante `/speckit.clarify` sem mudar escopo, AC ou guardrail (ex.: texto de mensagem, ordem de colunas). Na dúvida, `YES`.

## 5. Formato da pergunta ao humano

Uma pergunta por `AMB-NN`, fechada, curta, com consequência:

```markdown
### AMB-02 — Registros já existentes entram na nova regra? (BLOQUEANTE)

Contexto: hoje o cálculo é feito só na criação (HANDOFF-0003 § Current Behavior).
A história não diz o que acontece com os registros anteriores.

- **A)** Só registros novos. → Nenhuma migração; relatórios antigos ficam com a regra velha.
- **B)** Recalcular todos. → Exige migração/reprocessamento; afeta relatório X (IMPACT-20260910-...).
- **C)** Outro — descreva.

Sugestão do PO técnico (não aplicada): A, porque não toca histórico.
```

Regras:

- no máximo 7 perguntas por rodada; bloqueantes primeiro;
- nunca pergunte o que o conhecimento ou o código já respondem — isso é custo para o humano;
- nunca embuta duas decisões em uma pergunta;
- a sugestão é opcional e **nunca** é gravada como resposta.

## 6. Registrar a resposta

Ao receber a resposta:

- `Status` → `ANSWERED_BY_HUMAN` (ou `ASSUMPTION_ACCEPTED` se o humano aceitou literalmente a sugestão);
- `Evidence / Answer` → resposta literal entre aspas, quem respondeu e data;
- se a resposta gerar nova dúvida, crie um novo `AMB-NN` — não edite a pergunta original;
- incremente `revision` e atualize `open_questions`.

Se quem respondeu não for o `decision_owner` declarado, registre o nome e sinalize na resposta ao usuário.

## 7. O que nunca fazer

- escolher uma opção porque "é o mais comum";
- transformar sugestão em AC antes da resposta;
- reduzir `Blocking` de `YES` para `NO` para conseguir `READY_FOR_SPECKIT`;
- remover uma pergunta aberta do registro sem resposta;
- reinterpretar a resposta do humano — se ela for ambígua, pergunte de novo.
