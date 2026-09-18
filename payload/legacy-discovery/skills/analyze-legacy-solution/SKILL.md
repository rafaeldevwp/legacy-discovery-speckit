---
name: analyze-legacy-solution
description: Analisa uma solution .NET (C#) legada — moderna ou clássica — e persiste entendimento AS-IS de arquitetura, projetos, integrações e decisões existentes. Use para entender, documentar ou aprofundar um repositório legado. Reaproveita .github/copilot-knowledge/ e só abre source quando o conhecimento relevante estiver ausente, parcial ou stale. Não produz arquitetura TO-BE, plano de modernização, spec, design ou tasks.
---

# Analyze Legacy .NET Solution

Você entende e documenta o **AS-IS** de solutions .NET legadas com foco em economia de contexto, evidência e reuso.

## Privacidade e versionamento

Para repositórios com política de privacidade local, trate artefatos gerados por skill como
**não versionáveis**.

Regras obrigatórias neste modo:

1. Não executar ações de staging/commit para conteúdo gerado pela skill.
2. Considerar `.github/copilot-knowledge/` como conhecimento local de trabalho.
3. Quando necessário, orientar o uso de `.git/info/exclude` para bloquear versionamento dos artefatos da skill.
4. Artefatos do Spec Kit seguem a política normal do time.

Se a política local disser que conhecimento não pode subir para remoto, priorize essa política.

## Interacao com humano

Antes de iniciar discovery amplo, confirme em linguagem objetiva:

1. escopo funcional priorizado;
2. profundidade desejada (estrutural ou completa);
3. restricoes de tempo/custo de exploracao.

Se houver ambiguidade de dominio, pare e faca uma pergunta curta antes de prosseguir.

## Regra de entrada — índice primeiro, cobertura depois

Se existir `.github/copilot-knowledge/INDEX.md`:

1. leia **somente o INDEX primeiro**;
2. identifique os artefatos relacionados ao pedido;
3. leia apenas esses artefatos;
4. determine se o conhecimento é suficiente para a pergunta atual.

### Se estiver suficiente e atual

Responda usando a base persistida. **Não abra source apenas para reconfirmar fatos já cobertos.**

### Se estiver ausente, parcial ou stale

Carregue `references/discovery-process.md` e faça discovery incremental somente na área necessária.

### Se o usuário pedir refresh explícito

Atualize somente o escopo pedido, a menos que ele solicite reanálise completa.

A existência do `INDEX.md` não é, sozinha, motivo para parar. O critério é **cobertura do pedido atual**.

## Deep dive

Se o usuário pedir para aprofundar uma regra, classe ou método específico, use `references/deep-dive.md`. Esse modo pode ler função por função, mas continua restrito ao alvo e dependências necessárias.

## Referências

- `references/discovery-process.md` — discovery estrutural e incremental para monorepos, .NET moderno e .NET Framework clássico.
- `references/frontend-legacy-patterns.md` — anchors para Web Forms/AngularJS/híbridos.
- `references/output-format.md` — persistência de `SOLUTION-OVERVIEW`, `PROJECT`, `ADR` e `DEEP-DIVE`.
- `references/confidence-criteria.md` — classificação de confiança.
- `references/deep-dive.md` — aprofundamento sob demanda.
- `references/project-template.md` — template de projeto.
- `references/adr-format.md` — decisões **existentes/inferidas do código**, nunca decisões TO-BE.
- `.github/skill-contracts/` — nomes, lifecycle, ownership e validação.

## Fronteira com Spec Kit

Esta skill não cria RFC de modernização na V2 e não planeja mudanças futuras.

Quando o pedido evoluir de "como funciona hoje?" para "quero mudar isso", a próxima etapa é `prepare-speckit-context`, que produz um `SPECKIT_HANDOFF` para o Spec Kit.

## Persistência

Depois de gravar artefatos:

```bash
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
```

IDs de ADR legados continuam sendo alocados por `next_id.py`. Não edite `INDEX.md` manualmente.
