# Integração com o Spec Kit oficial

Este pacote **não substitui** os artefatos ou comandos do Spec Kit. Ele prepara contexto AS-IS antes deles.

## Adoção em repositório existente

Antes de inicializar o Spec Kit em um repositório não vazio, crie uma baseline revisável (commit/stash/branch). Depois, use o fluxo oficial apropriado à integração instalada.

Exemplo para GitHub Copilot:

```bash
specify init --here --force --integration copilot
```

Revise o diff gerado antes de continuar.

## Fluxo SDD recomendado para legado

```text
prepare-speckit-context
        ↓
SPECKIT_HANDOFF
        ↓
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.implement
/speckit.converge
```

O `SPECKIT_HANDOFF` não deve ser copiado inteiro para `spec.md`. Ele funciona como evidência/contexto do AS-IS. A spec define a mudança desejada.

## Constitution

Em projeto existente, a constitution deve capturar guardrails reais já aceitos pelo time, por exemplo:

- preservar compatibilidade de APIs/contratos públicos existentes;
- respeitar boundaries atuais salvo decisão explícita no plan;
- reutilizar frameworks e padrões de teste já presentes;
- não adicionar dependência sem justificativa;
- tratar integrações externas e consumidores fora do repositório como risco explícito;
- exigir regressão proporcional ao raio de impacto.

Não invente princípios apenas para preencher template.

Ao escrever a constitution, preserve o AS-IS real do projeto. Nao reescreva historico tecnico e nao introduza padroes novos sem evidencias do contexto atual.

## Plan

Em projeto legado, o `/speckit.plan` deve respeitar a arquitetura existente e explicitar qualquer excecao como decisao deliberada do time.

Regras praticas:

- partir das restricoes e evidencias do `SPECKIT_HANDOFF`;
- privilegiar evolucao incremental sobre substituicao ampla;
- manter compatibilidade por padrao;
- enriquecer o plano com conhecimento ja absorvido pelas skills, sem inventar fatos nao observados.

## Extensão oficial de bug

O Spec Kit possui extensão opt-in de bug:

```bash
specify extension add bug
```

Fluxo:

```text
/speckit.bug.assess
→ /speckit.bug.fix
→ /speckit.bug.test
```

Use `target_flow: BUG` somente quando o usuário quiser explicitamente esse caminho. Para correções que exigem especificação, decisões arquiteturais ou decomposição revisável antes da implementação, use `target_flow: SDD`.
