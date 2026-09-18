# Processo de triagem (do sintoma ao(s) ponto(s) provável(is) da falha)

Execute na ordem. **Pare assim que tiver 1-2 hipóteses com confiança Alta** (ver `hypothesis-confidence.md`) — não é preciso completar todas as fases em todo caso. Cenário simples pode resolver na Fase 1 ou 2; cenário complexo com múltiplos projetos pode precisar de todas.

## Fase 0 — Estruturar o sintoma relatado

Antes de tocar em código, formalize o que foi dito (geralmente vago, tipo "o cálculo X está errado"):

- **O que é esperado?**
- **O que está acontecendo de fato?**
- **Tem um exemplo concreto?** (um caso/pedido/cliente específico onde o erro aparece — isso muda tudo na precisão da investigação)
- **Desde quando?** (ajuda a saber se é regressão recente ou sempre foi assim)
- **Termos de negócio envolvidos** (nomes que a PO usou — "desconto", "frete", "XPTO" — viram as palavras-chave da Fase 1)

Se faltar o exemplo concreto, **pergunte por ele antes de prosseguir** — sem um caso real, a investigação vira busca cega e fica cara e imprecisa. As outras perguntas, se não respondidas, podem ficar "não informado" e a investigação segue mesmo assim.

## Fase 1 — Triagem pela base de conhecimento já existente (grátis ou quase)

Se `.github/copilot-knowledge/` existir:

1. Leia `INDEX.md` e busque, pelos termos de negócio da Fase 0, quais `projects/*.md` e `deep-dives/*.md` já mencionam esses termos.
2. **Se já existir um `deep-dive` cobrindo o método/classe candidato:** leia-o. O fluxograma já documentado é a ferramenta mais rápida daqui — compare o sintoma relatado com cada ramo: qual ramo, se seguido, produziria o resultado errado descrito? Isso pode resolver a investigação sem abrir nenhum código novo.
3. Se não houver deep-dive, mas os `projects/*.md` já identificam a camada/classe provável (ex: pela seção "Core funcional"), isso já estreita bastante — vá para a Fase 3 direto nesse candidato, pulando a Fase 2.

## Fase 2 — Busca dirigida no código (ainda barata)

Se a base de conhecimento não apontar candidato nenhum (ou não existir): busque por texto os termos de negócio da Fase 0 direto no código — nomes de método, nomes de campo, mensagens de erro/exception que contenham esses termos. Gere uma lista curta de candidatos (arquivos/classes/métodos), não abra o conteúdo completo ainda.

## Fase 3 — Aprofundamento seletivo só nos candidatos mais prováveis (a fase cara)

Escolha **no máximo 1-3 candidatos** mais prováveis (pelos nomes/contexto da Fase 1-2) e leia o corpo completo deles — mesmo rigor do módulo `deep-dive.md` da skill `analyze-legacy-solution`, se ela estiver disponível neste repositório (reaproveite o mesmo padrão: separar fato de interpretação, ramificações explícitas). Objetivo aqui não é documentar tudo, é achar **qual ramo/condição específica bate com o sintoma relatado**.

**Regra obrigatória:** registre toda descoberta estrutural reaproveitável na seção `knowledge_updates` de `INVESTIGATION-{YYYYMMDD}-{slug}.md`, com evidência e destino sugerido. Esta skill não cria nem edita `DEEP-DIVE`, `PROJECT` ou `INDEX`: esses artefatos possuem outro owner conforme `.github/skill-contracts/ownership.md`.

Se ao ler o candidato ele claramente não pode ser a causa (ex: o caminho de código nunca produziria o sintoma descrito), **descarte explicitamente e registre por quê** — isso economiza retrabalho de quem for investigar depois.

## Fase 4 — Se o problema pode atravessar projetos/serviços

Se o dado atravessa serviços, use `SOLUTION-OVERVIEW.md`. Destinos fora do repositório são limites explícitos.

## Fase 5 — Gerar o relatório

Siga `investigation-report-format.md`. Nunca proponha correção — só o ponto da falha, a evidência, e o próximo passo pra confirmar.

## Construção orgânica do harness

Isso não é opcional nem um "extra bacana" — é o que faz a skill escalar bem com o tempo, especialmente sem uma análise macro prévia:

- **A primeira vez que uma área do código é investigada, o custo é real e inevitável** — alguém precisa ler código nunca lido. Nenhum desenho de skill evita isso.
- **Mas essa leitura nunca é jogada fora.** Ela fica no relatório de investigação e, quando for conhecimento estrutural, também em `knowledge_updates`. A skill proprietária pode promover a descoberta a `DEEP-DIVE` ou `PROJECT`; o script compartilhado reconstrói o `INDEX.md`.
- **Consequência prática:** bug hoje na área de Faturamento, bug amanhã também em Faturamento → o segundo já nasce mais barato, porque parte do terreno já foi mapeado no primeiro. Ao longo de várias investigações espalhadas pelo sistema, a base cresce organicamente, sem nunca ter sido preciso rodar uma análise completa e cara de uma vez só.
- **O que continua custando:** a primeira investigação numa área **totalmente nova** do sistema. Isso é esperado e não tem solução mágica — só fica mais barato a cada repetição na mesma área, não na primeira.
