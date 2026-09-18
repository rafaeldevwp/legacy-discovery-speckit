# Processo de mapeamento de impacto

Execute na ordem, parando assim que tiver resposta suficiente pra classificar o risco (ver `risk-report-format.md`). Cenário simples (método usado só dentro do próprio projeto, sem chamada de serviço) pode resolver nas Fases 1-2; cenário espalhado por múltiplos projetos/serviços precisa ir até a Fase 4.

## Fase 0 — Delimitar o alvo exato da mudança

Pergunte-se (ou confirme com o usuário se não estiver claro): a mudança é numa **classe inteira**, um **método específico**, ou um **contrato público** (assinatura, endpoint de serviço)? O raio de impacto muda muito dependendo disso — mudar o corpo de um método privado é diferente de mudar a assinatura de um método público exposto via WS.

## Fase 1 — Dependentes diretos, via base de conhecimento já existente (barata)

Se o alvo já aparece em `projects/*.md` ou `decisions/*.md`: veja quem lista esse projeto/classe como dependência ("Projetos internos" nos arquivos de projeto) e quais ADRs mencionam esse componente. Isso já responde boa parte sem abrir código novo.

## Fase 2 — Dependentes diretos, via código (se a base não cobrir)

- **Grafo de compilação:** consulte `SOLUTION-OVERVIEW.md`; se ausente, leia os `.csproj` necessários.
- **Uso real, não só referência de projeto:** ter `ProjectReference` não significa que a classe/método específico é usado — busque (grep) pelo nome da classe/método nos projetos que referenciam o projeto do alvo, pra confirmar uso real e não falso positivo.

## Fase 3 — Dependentes indiretos, via chamada de serviço (frequentemente o mais importante, e o mais fácil de esquecer)

Use o grafo de chamadas de serviço em `SOLUTION-OVERVIEW.md` para identificar consumidores indiretos.

Se o consumidor identificado não bater com nenhum projeto deste repositório, registre como **"dependente externo — fora do escopo desta análise, mas existe"** — não finja que não existe só porque não dá pra confirmar os detalhes.

## Fase 4 — Contexto adicional: decisões, cobertura de teste, documentação existente

- **ADRs relacionados** (`decisions/*.md`): se a mudança contradiz um padrão já registrado como deliberado, isso é um sinal de risco a mais, não só um FYI.
- **Deep-dive existente** (`deep-dives/*.md`): se o alvo já foi aprofundado antes, a mudança provavelmente vai tornar aquele documento desatualizado — sinalize isso no relatório, mesmo que atualizar o documento não seja parte desta skill.
- **Teste de regressão existente:** procure se já existe um teste cobrindo esse método (gerado por `investigate-legacy-bug` ou não). Ausência de teste é, sozinha, um fator de risco (mudança sem rede de segurança).
- **Front-end (se aplicável):** se o alvo é consumido por AngularJS/Web Forms (ver `frontend-legacy-patterns.md` da outra skill, se disponível), telas específicas podem depender do contrato — verifique se a mudança altera algo que o front-end consome diretamente.

## Depois de mapear

Siga `risk-report-format.md` para estruturar a saída.
