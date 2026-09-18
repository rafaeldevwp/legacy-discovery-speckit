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
