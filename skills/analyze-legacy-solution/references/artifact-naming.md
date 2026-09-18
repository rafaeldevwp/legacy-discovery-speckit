# Convenção de nomes dos artefatos

Todos os artefatos em `.github/copilot-knowledge/` seguem **tipo primeiro**, em maiúsculas, com segmentos separados por hífen:

```text
{TIPO}-{IDENTIFICADOR}-{slug}.md
```

## Regras gerais

- `TIPO`: prefixo reservado da tabela abaixo.
- Identificadores sequenciais usam quatro dígitos (`0001`).
- Datas usam `YYYYMMDD`, sem separadores.
- `slug`: minúsculo, sem acentos, com palavras separadas por hífen; preserve nomes técnicos reconhecíveis quando necessário.
- O nome do arquivo não muda quando título, status ou conteúdo mudam.
- Antes de alocar número sequencial, verifique arquivos e pastas existentes para evitar colisão.
- Não crie variantes como `final`, `novo`, `v2`, `revisado` ou cópias com timestamps. Atualize o artefato canônico e preserve histórico no Git.

## Tipos

| Artefato | Nome canônico |
|---|---|
| Índice geral | `INDEX.md` |
| Visão da solution | `SOLUTION-OVERVIEW.md` |
| Projeto | `PROJECT-{project-slug}.md` |
| Decisão arquitetural | `ADR-{NNNN}-{slug}.md` |
| Proposta/RFC | `RFC-{NNNN}-{slug}.md` |
| Aprofundamento | `DEEP-DIVE-{project-slug}-{class-slug}.md` |
| Investigação | `INVESTIGATION-{YYYYMMDD}-{slug}.md` |
| Análise de impacto | `IMPACT-{YYYYMMDD}-{slug}.md` |
| Pasta de correção | `FIX-{NNNN}-{slug}/` |
| Requisitos da FIX | `SPEC-FIX-{NNNN}.md` |
| Design da FIX | `DESIGN-FIX-{NNNN}.md` |
| Tarefas da FIX | `TASKS-FIX-{NNNN}.md` |
| Execução da FIX | `EXECUTION-FIX-{NNNN}.md` |
| Regressão da FIX | `REGRESSION-FIX-{NNNN}.md` |
| Verificação da FIX | `VERIFICATION-FIX-{NNNN}.md` |

Os seis documentos de uma FIX reutilizam o mesmo número da pasta. Não aloque IDs separados para SPEC, DESIGN ou TASKS.

## Compatibilidade com artefatos antigos

Não renomeie automaticamente conhecimento preexistente só porque usa convenção anterior: renomear em massa pode quebrar links e histórico. Ao tocar um artefato antigo, proponha a migração com atualização atômica de todas as referências e do `INDEX.md`. Todo artefato novo usa obrigatoriamente a convenção canônica.

