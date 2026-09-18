# Manual — Legacy Discovery + Spec Kit v5

> **Do pedido do PM ao código, sem adivinhar e sem regressão.**
> Este manual cobre a v5 inteira — instalação, cada comando, cada artefato — e acompanha **uma história real do começo ao fim**.

Versão do pacote: **bundle 1.3.0 · Legacy Discovery V2.3 · Spec Kit 1.0.1 · GitHub Copilot**.

---

## Índice

**Parte I — Entender**
1. [O que é este pacote, em 1 minuto](#1-o-que-é-este-pacote-em-1-minuto)
2. [As 5 ideias que você precisa saber](#2-as-5-ideias-que-você-precisa-saber)
3. [Quem faz o quê](#3-quem-faz-o-quê)

**Parte II — Instalar**
4. [Pré-requisitos](#4-pré-requisitos)
5. [Instalação nova](#5-instalação-nova)
6. [Atualizar a partir da v4](#6-atualizar-a-partir-da-v4)
7. [O que mudou no seu repositório](#7-o-que-mudou-no-seu-repositório)
8. [Conferir se deu certo](#8-conferir-se-deu-certo)
9. [Primeiro uso: constitution e primeiro mapa](#9-primeiro-uso-constitution-e-primeiro-mapa)

**Parte III — Usar no dia a dia**
10. [Os comandos `/legacy.*`](#10-os-comandos-legacy)
11. [Exemplo completo: uma história do PM do início ao fim](#11-exemplo-completo-uma-história-do-pm-do-início-ao-fim)
12. [Outros cenários](#12-outros-cenários)

**Parte IV — Por dentro**
13. [O refinamento, seção por seção](#13-o-refinamento-seção-por-seção)
14. [Ambiguidades: como o PO decide quem responde](#14-ambiguidades-como-o-po-decide-quem-responde)
15. [Guardrails de regressão e fatias](#15-guardrails-de-regressão-e-fatias)
16. [Status e ciclo de vida](#16-status-e-ciclo-de-vida)
17. [Governança: o que é bloqueado e por quem](#17-governança-o-que-é-bloqueado-e-por-quem)

**Parte V — Referência**
18. [Scripts de terminal](#18-scripts-de-terminal)
19. [Mensagens do validador e como corrigir](#19-mensagens-do-validador-e-como-corrigir)
20. [Onde fica cada coisa](#20-onde-fica-cada-coisa)
21. [Solução de problemas](#21-solução-de-problemas)
22. [Boas práticas e armadilhas](#22-boas-práticas-e-armadilhas)
23. [Cola rápida](#23-cola-rápida)

---

# Parte I — Entender

## 1. O que é este pacote, em 1 minuto

Você trabalha com um sistema legado. O PM manda uma história. Se a IA for direto para o código, ela **supõe** o que o sistema faz e **supõe** o que o PM quis dizer — e é daí que vem a regressão.

Este pacote coloca três etapas antes do código:

```text
  1. ENTENDER O HOJE          2. ESCLARECER O PEDIDO          3. ESPECIFICAR E FAZER
  (Legacy Discovery)          (PO técnico)                    (Spec Kit)

  "Como o sistema faz         "O que exatamente o PM          "Como vamos mudar,
   isso hoje?"                 quer? O que não pode            em que ordem?"
                               quebrar?"
        │                            │                               │
        ▼                            ▼                               ▼
     HANDOFF          ─────►     REFINEMENT         ─────►     spec → plan → tasks → código
```

E tudo isso por **comandos**, como o Spec Kit:

```text
/legacy.story <história do PM>   →   responde as perguntas   →   /legacy.approve   →   /speckit.specify
```

## 2. As 5 ideias que você precisa saber

### Ideia 1 — AS-IS × TO-BE

| | Significa | Quem cuida |
|---|---|---|
| **AS-IS** | Como o sistema funciona **hoje** | Skills de Discovery |
| **TO-BE** | Como o sistema vai funcionar **depois** da mudança | Spec Kit |

As skills deste pacote **nunca** decidem o TO-BE. Elas levantam fatos e esclarecem o pedido.

### Ideia 2 — Artefato

Um arquivo Markdown com cabeçalho (frontmatter) que registra o resultado de uma skill. Exemplos: `HANDOFF-0003-...md`, `REFINEMENT-0001-...md`. Ficam em `.github/copilot-knowledge/`.

### Ideia 3 — Status

Todo artefato tem um status em inglês e maiúsculas (`READY_FOR_SPECKIT`, `AWAITING_HUMAN`, `BLOCKED`...). O status é o que libera ou trava a próxima etapa.

### Ideia 4 — Um dono por artefato

Cada tipo de artefato tem **uma** skill que pode escrevê-lo. As outras só leem. Isso evita que uma skill "conserte" o trabalho de outra em silêncio.

### Ideia 5 — O código responde "como é". Só o humano responde "como deve ser".

Essa é a regra do PO técnico. Se a dúvida é sobre o presente, ele procura no conhecimento e no código. Se é sobre intenção, regra nova ou escopo, **ele pergunta para você** — e não segue sem resposta.

## 3. Quem faz o quê

| Quem | Faz | Nunca faz |
|---|---|---|
| **Você / o PM** | Decide regra de negócio, escopo, responde perguntas, aprova o refinamento | — |
| `analyze-legacy-solution` | Mapeia projetos, dependências, decisões existentes | Planejar modernização |
| `investigate-legacy-bug` | Localiza a causa provável de um bug, com evidência | Corrigir código |
| `analyze-change-impact` | Mostra quem depende do que vai mudar | Dizer se a mudança é boa |
| `prepare-speckit-context` | Gera o **HANDOFF**: o AS-IS da mudança | Propor solução |
| `refine-user-story` (**novo**) | PO técnico: gera o **REFINEMENT** | Decidir negócio, arquitetura ou aprovar sozinho |
| `prepare-feature-branch` | Cria a branch `feature/mmYYYY/...` a partir da `main` | Stash, reset, merge, force, push |
| **Spec Kit** | spec, plan, tasks, implementação | — |

---

# Parte II — Instalar

## 4. Pré-requisitos

| Item | Versão | Como conferir |
|---|---|---|
| Git | qualquer recente | `git --version` |
| Python | **3.11 ou superior** | `python --version` |
| VS Code + GitHub Copilot | Copilot Chat em **Agent Mode** | abrir o chat e ver o seletor "Agent" |
| Internet | só na primeira instalação | baixa o `specify-cli` oficial |
| `uv` | opcional | `uv --version` (sem ele, usa `pip`) |

> ⚠️ **Windows:** descompacte o pacote num **caminho curto**, como `C:\Ferramentas\`. Caminhos com mais de 260 caracteres fazem o Python ignorar arquivos em silêncio.

## 5. Instalação nova

**Passo 1 — Proteja seu código.** Na raiz do repositório legado:

```bash
git status
```

Se houver alteração pendente, faça commit ou stash antes.

**Passo 2 — Descompacte** `legacy-discovery-speckit-v5.zip` em `C:\Ferramentas\`.

**Passo 3 — Execute** `C:\Ferramentas\legacy-discovery-speckit-v5\INSTALAR-WINDOWS.bat` (dois cliques) e informe a raiz do repositório:

```text
Repositorio: C:\Projetos\ConsultaVeiculos
```

A saída termina assim:

```text
Comandos instalados: 13 (/legacy.*) em .github/prompts/
...
INSTALAÇÃO CONCLUÍDA.

Comandos das skills: digite /legacy.help no chat do Copilot.
Primeiro uso recomendado:
  1) /speckit.constitution
  2) Peça: 'Use analyze-legacy-solution para iniciar o mapa deste legado.'
  3) Para uma US do PM: /legacy.story <história literal>
     Responda com /legacy.answer e aprove com /legacy.approve (só você aprova)
  4) Acompanhe com /legacy.status
  5) Com o REFINEMENT em READY_FOR_SPECKIT: /legacy.branch <descrição>
  6) Depois execute /speckit.specify
```

**Alternativas ao `.bat`:**

```powershell
# PowerShell
.\install.ps1 -TargetPath "C:\Projetos\ConsultaVeiculos"
```

```bash
# Python direto (qualquer SO)
python install.py --target "C:\Projetos\ConsultaVeiculos"

# Linux/macOS
./install.sh /caminho/do/repositorio
```

## 6. Atualizar a partir da v4

Se o repositório já tem a v4 com Spec Kit, **não reinstale o Spec Kit**:

```bash
python C:\Ferramentas\legacy-discovery-speckit-v5\install.py --target "C:\Projetos\ConsultaVeiculos" --skip-speckit-install --skip-speckit-init
```

O que acontece na atualização:

| Item | Resultado |
|---|---|
| `.github/copilot-knowledge/` (seu conhecimento) | **preservado**, nada é apagado |
| As 5 skills da v4 | reinstaladas **idênticas** (byte a byte) |
| `refine-user-story` | adicionada |
| `.github/prompts/legacy.*.prompt.md` | adicionados; **outros prompts não são tocados** |
| `.git/info/exclude` | bloco local-only mantido, sem duplicar |
| Backup | cópia prévia em `<pacote>\backups\<repo>-AAAAmmdd-HHMMSS\` |

**Todas as opções do instalador:**

| Opção | Efeito |
|---|---|
| `--target <repo>` | raiz do repositório (precisa ter `.git`) |
| `--skip-speckit-install` | não instala o `specify-cli` |
| `--skip-speckit-init` | não roda `specify init` |
| `--keep-legacy-v1` | mantém ativas as skills V1 (`coordinate-fix`, etc.) |
| `--spec-kit-version X` | outra versão do Spec Kit (padrão `1.0.1`) |

## 7. O que mudou no seu repositório

```text
SEU-REPO/
├── .github/
│   ├── prompts/
│   │   ├── legacy.help.prompt.md        ← 13 comandos /legacy.* (novos)
│   │   ├── legacy.story.prompt.md
│   │   └── ...                          ← seus prompts e os do Spec Kit ficam como estavam
│   ├── skills/
│   │   ├── analyze-legacy-solution/
│   │   ├── investigate-legacy-bug/
│   │   ├── analyze-change-impact/
│   │   ├── prepare-speckit-context/
│   │   ├── prepare-feature-branch/
│   │   └── refine-user-story/           ← novo (PO técnico)
│   ├── skill-contracts/                 ← regras + scripts de validação
│   ├── copilot-knowledge/               ← LOCAL-ONLY (não vai para o Git)
│   │   ├── INDEX.md
│   │   ├── handoffs/
│   │   ├── refinements/                 ← novo
│   │   └── ...
│   └── legacy-discovery/                ← docs + installation.json
├── .specify/                            ← Spec Kit
└── specs/                               ← features do Spec Kit
```

Revise sempre:

```bash
git status
git diff
```

## 8. Conferir se deu certo

**No terminal**, na raiz do repositório:

```bash
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/story_status.py
```

Esperado:

```text
validation passed: 0 artifact(s)
# Status das histórias

Nenhuma história em andamento. Comece com `/legacy.story <história do PM>`.
```

**No VS Code:** abra o Copilot Chat em **Agent Mode**, digite `/legacy.` — devem aparecer os 13 comandos. Rode:

```text
/legacy.help
```

**Opcional — provar a não-regressão do pacote** (na pasta do pacote, não no repo):

```bash
cd C:\Ferramentas\legacy-discovery-speckit-v5
python -m unittest discover -s tests -v
```

```text
Ran 61 tests in 11.2s
OK
```

## 9. Primeiro uso: constitution e primeiro mapa

Faça **uma vez** por repositório.

**9.1 — Regras do projeto.** No chat:

```text
/speckit.constitution
Este é um sistema legado crítico.
Preserve contratos e compatibilidade existentes.
Não modernize tecnologia sem justificativa explícita.
Trate HANDOFFs como contexto factual AS-IS e REFINEMENTs como requisitos confirmados pelo PO/PM.
Decisões TO-BE pertencem ao Spec Kit. Não trate inferência como fato.
Toda mudança começa pelos testes de caracterização dos guardrails sem cobertura.
```

**9.2 — Primeiro mapa do legado.** No chat:

```text
/legacy.analyze Estrutura geral: projetos, responsabilidades, dependências e integrações externas.
Profundidade estrutural. Não aprofunde classes ainda.
```

A skill vai perguntar escopo, profundidade e limites antes de começar. Responda curto. Ao final você terá `SOLUTION-OVERVIEW.md` e `projects/PROJECT-*.md` — e os próximos pedidos reaproveitam isso em vez de reler o código.

> Não peça para "estudar o repositório inteiro a fundo". O pacote trabalha por **descoberta progressiva**: aprofunda só onde a história precisa.

---

# Parte III — Usar no dia a dia

## 10. Os comandos `/legacy.*`

Todos são digitados no **Copilot Chat em Agent Mode**. O texto depois do comando é a entrada.

### Mapa rápido

| Quero... | Comando |
|---|---|
| ver o que existe e o próximo passo | `/legacy.help` |
| levar uma história do PM até o refinamento pronto | `/legacy.story` |
| entender uma parte do sistema | `/legacy.analyze` |
| investigar um bug | `/legacy.bug` |
| saber o que uma mudança afeta | `/legacy.impact` |
| gerar só o AS-IS de uma mudança | `/legacy.handoff` |
| só refinar uma história | `/legacy.refine` |
| responder perguntas do PO | `/legacy.answer` |
| aprovar o refinamento | `/legacy.approve` |
| criar a branch | `/legacy.branch` |
| ver o andamento | `/legacy.status` |
| checar se está tudo válido | `/legacy.validate` |
| limpar artefatos locais | `/legacy.archive` |

### 10.1 `/legacy.help`

**Quando:** sempre que não souber o próximo passo.
**Sintaxe:** `/legacy.help [ID]`

```text
/legacy.help
```

Mostra a tabela de comandos e, para cada história em andamento, o próximo comando. **Não altera nada.**

### 10.2 `/legacy.story` — o fluxo guiado

**Quando:** chegou uma história do PM. É o comando mais usado.
**Sintaxe:** `/legacy.story <história literal>` (+ quem decide negócio)

```text
/legacy.story
US-4821 — Como atendente da central, quero que a consulta de veículos continue mostrando a última
situação conhecida quando o serviço da PBH demorar, para não deixar o cidadão sem resposta.
Critério: não mostrar tela de erro quando der timeout.

Quem decide regra de negócio: Marina (PM).
```

**O que ele faz, em ordem:**

```text
1. /legacy.status  →  já existe algo desta história? retoma de onde parou
2. sem HANDOFF pronto  →  prepare-speckit-context
       PARTIAL/BLOCKED  →  PARA e mostra o que falta
3. HANDOFF pronto  →  refine-user-story
       AWAITING_HUMAN  →  PARA e mostra as perguntas
       BLOCKED         →  PARA e mostra como destravar
       sem bloqueio    →  PARA e sugere /legacy.approve
```

**O que ele nunca faz:** aprovar, criar branch, chamar o Spec Kit.

### 10.3 `/legacy.analyze`

**Quando:** quer entender uma área, sem mudança em vista.

```text
/legacy.analyze Como funciona o cálculo de multa por atraso no projeto Financeiro?
```

Saída: resumo curto + artefatos (`PROJECT-*`, `DEEP-DIVE-*`, `ADR-*`). Próximo: `/legacy.handoff` se houver mudança pretendida.

### 10.4 `/legacy.bug`

**Quando:** algo está errado e você não sabe onde.

```text
/legacy.bug
Sintoma: segunda via do boleto sai com vencimento no domingo.
Esperado: próximo dia útil.
Ambiente: produção, desde 01/09. Urgência alta, afeta cobrança.
```

Saída: hipóteses rankeadas com evidência e confiança. **Nunca corrige.** Próximo: `/speckit.bug.assess` (correção pontual) ou `/legacy.impact` → `/legacy.handoff` (precisa de spec).

### 10.5 `/legacy.impact`

**Quando:** vai mexer em algo e quer saber quem depende.

```text
/legacy.impact Método HistoricoRepository.Gravar — mudança de comportamento — só este repositório.
```

Saída: nível de risco com critério, dependentes diretos/indiretos, o que não foi possível ver.

### 10.6 `/legacy.handoff`

**Quando:** quer só o AS-IS da mudança (o `/legacy.story` já chama isto por você).

```text
/legacy.handoff Consulta de veículos deve mostrar a última situação conhecida no timeout da PBH.
```

A skill confirma objetivo, critério de pronto e fluxo (SDD/BUG). Gera `handoffs/HANDOFF-NNNN-slug.md`.

### 10.7 `/legacy.refine`

**Quando:** já tem o HANDOFF e quer só o refinamento.

```text
/legacy.refine
<história literal do PM>
Use o HANDOFF-0003. Quem decide: Marina (PM).
```

Gera `refinements/REFINEMENT-NNNN-slug.md`. **Nunca marca como pronto** — isso é `/legacy.approve`.

### 10.8 `/legacy.answer`

**Quando:** o PO fez perguntas (`AWAITING_HUMAN`).
**Sintaxe:** `/legacy.answer <REFINEMENT> AMB-NN: <resposta>; AMB-NN: <resposta>`

```text
/legacy.answer REFINEMENT-0001
AMB-03: até 24 horas; acima disso mostrar aviso de dado desatualizado.
AMB-04: mostrar "serviço indisponível, tente em alguns minutos".
AMB-05: aceito a sugestão (sim, data e hora).
Respondido por: Marina (PM).
```

O PO grava a resposta **literal**, com quem e quando, atualiza AC/fatias e faz nova rodada se surgir dúvida nova.

> Se a resposta for vaga ("o normal"), o PO **pergunta de novo** — ele não interpreta.

### 10.9 `/legacy.approve`

**Quando:** não há mais pergunta bloqueante e você revisou o refinamento.
**Sintaxe:** `/legacy.approve <REFINEMENT> revisor: <seu nome>`

```text
/legacy.approve REFINEMENT-0001 revisor: Rafael Lima
```

Fluxo:

```text
mostra resumo (AC, GR, fatias, não decidido)
   → "Aprovar REFINEMENT-0001 como Rafael Lima?"  → você: sim
   → grava reviewed_by / reviewed_at / READY_FOR_SPECKIT
   → roda o validador
        passou  → APPROVED
        falhou  → DESFAZ a aprovação e mostra por quê (NOT_APPROVED)
```

É o **único** caminho de aprovação. O agente não pode se autoaprovar.

### 10.10 `/legacy.branch`

**Quando:** refinamento aprovado.

```text
/legacy.branch consulta-veiculos-timeout
```

Antes de criar, confere o status. **Se a história tem refinamento ainda não aprovado, recusa.** Depois segue a skill `prepare-feature-branch`: worktree limpo, `git fetch`, `main` atualizada por fast-forward, branch nova:

```text
BRANCH_READY
branch: feature/092026/consulta-veiculos-timeout
base_commit: 4f2a9c1
Próximo: /speckit.specify ...
```

### 10.11 `/legacy.status`

```text
/legacy.status
```

Saída real (do exemplo deste manual):

```text
# Status das histórias

## Refinamentos

| Refinamento | História | Status | Rev. | Handoff | Perguntas abertas | Próximo comando |
|---|---|---|---|---|---|---|
| REFINEMENT-0001 | US-4821 — Refinamento — Consulta de veículos não perde o último estado no timeout | READY_FOR_SPECKIT | 3 | HANDOFF-0003 (READY_FOR_SPECKIT) | 1 | /legacy.branch -> /speckit.specify |

## Handoffs sem refinamento

| Handoff | Pedido | Status | Próximo comando |
|---|---|---|---|
| HANDOFF-0004 | segunda via do boleto | READY_FOR_SPECKIT | /legacy.refine |
```

Somente leitura. Filtrar: `/legacy.status REFINEMENT-0001`.

### 10.12 `/legacy.validate`

```text
/legacy.validate
```

Roda validar → reconstruir INDEX → validar. Se falhar, lista cada erro com o dono do artefato e o comando que corrige. **Não corrige sozinho.** Veja o [capítulo 19](#19-mensagens-do-validador-e-como-corrigir).

### 10.13 `/legacy.archive`

```text
/legacy.archive           ← só arquiva (ZIP fora do repo)
/legacy.archive limpar    ← arquiva e remove, após sua confirmação
```

Mexe só em `.github/copilot-knowledge/` e `installation.json`. Nunca em código ou em `specs/`.

### E sem comandos?

Continua funcionando como antes: `Use a skill refine-user-story para ...`. Os comandos são atalhos, não substitutos.

---

## 11. Exemplo completo: uma história do PM do início ao fim

Vamos seguir a **US-4821** do começo ao merge. Sistema: `ConsultaVeiculos`, .NET Framework, chama um serviço SOAP da PBH.

### Passo 0 — A história chega

A PM Marina escreve no board:

> **US-4821** — Como atendente da central, quero que a consulta de veículos continue mostrando a última situação conhecida quando o serviço da PBH demorar, para não deixar o cidadão sem resposta.
> Critério: não mostrar tela de erro quando der timeout.

Parece clara. Não é: *quanto* é "demorar"? *Quão velha* pode ser a "última situação"? E se *não houver* situação anterior?

### Passo 1 — Iniciar o fluxo guiado

```text
/legacy.story
US-4821 — Como atendente da central, quero que a consulta de veículos continue mostrando a última
situação conhecida quando o serviço da PBH demorar, para não deixar o cidadão sem resposta.
Critério: não mostrar tela de erro quando der timeout.

Quem decide regra de negócio: Marina (PM).
```

### Passo 2 — O AS-IS (handoff)

Sem handoff para essa história, o comando chama `prepare-speckit-context`. Ela confirma com você:

```text
1. Objetivo: exibir última situação conhecida no timeout da PBH. Correto?
2. Pronto quando: comportamento atual de timeout, histórico e consumidores mapeados.
3. Fluxo: SDD (feature com spec). Confirma?
```

Você: `sim, sim, SDD`.

Ela lê o `INDEX.md` primeiro, reaproveita `PROJECT-consulta` e `IMPACT-20260915-historico-consulta`, abre só 3 arquivos para fechar lacunas e grava `HANDOFF-0003`:

```text
Status: READY_FOR_SPECKIT
Acesso a código: BOUNDED (3 arquivos)
Unknowns bloqueantes: NONE
Handoff: .github/copilot-knowledge/handoffs/HANDOFF-0003-timeout-consulta-veiculos.md
```

Fatos que ficaram registrados (resumo):

- chamada SOAP síncrona à PBH, **sem retry**;
- timeout de **30 s** no `Web.config` (`PbhTimeoutSeconds`);
- no timeout, o controller mostra a tela `ErroConsulta`;
- toda consulta bem-sucedida **já é gravada** em `HistoricoConsulta`;
- o relatório diário lê `HistoricoConsulta`.

### Passo 3 — O PO refina (revisão 1)

Com o handoff pronto, o comando chama `refine-user-story`. O PO:

1. copia a história **literalmente**;
2. avalia INVEST + DoR → acha `GAP` em *Testable* e em *critérios de aceite*;
3. levanta as ambiguidades e passa cada uma pela escada:

| Dúvida | Escada | Resultado |
|---|---|---|
| AMB-01 Hoje tem retry? | STORY ✗ → **KNOWLEDGE** ✓ | Resolvido: HANDOFF-0003 diz que não |
| AMB-02 O que é "demorar"? | STORY ✗ → KNOWLEDGE ✗ → **CODE** ✓ | Resolvido: `PbhClient.cs:41`, 30 s |
| AMB-03 Até quantas horas mostrar a última situação? | é **regra de negócio** → direto ao HUMAN | **Pergunta** (bloqueante) |
| AMB-04 E se não houver histórico? | caso **não descrito** → HUMAN | **Pergunta** (bloqueante) |
| AMB-05 O aviso mostra data/hora? | intenção de UX → HUMAN | **Pergunta** (não bloqueante) |

Resposta no chat:

```text
REFINEMENT-0001 — AWAITING_HUMAN (revisão 1)
Resolvidas: 2 (conhecimento: 1, código: 1). Abertas ao humano: 3 (2 bloqueantes).
Acesso a código: BOUNDED (1 arquivo)

### AMB-03 — Até quantas horas a "última situação" pode ser exibida? (BLOQUEANTE)
Contexto: HistoricoConsulta guarda todas as consultas com data (HANDOFF-0003).
A história não limita a idade da informação.
- A) Sem limite → atendente pode informar situação de meses atrás.
- B) Limite de N horas → acima disso, o quê? (esconder / mostrar com aviso)
- C) Outro.
Sugestão do PO (não aplicada): B com aviso, 24 h.

### AMB-04 — Sem nenhum histórico, o que mostrar? (BLOQUEANTE)
- A) Tela de erro atual → contraria o critério da história.
- B) Mensagem amigável sem erro → qual texto?
- C) Outro.

### AMB-05 — O aviso deve informar data/hora da informação? (não bloqueante)
- A) Sim  - B) Não
Sugestão do PO (não aplicada): A.

Próximo: /legacy.answer REFINEMENT-0001 AMB-03: ...; AMB-04: ...; AMB-05: ...
```

Repare: o PO **sugere**, mas **não aplica**. O status é `AWAITING_HUMAN` e nada avança.

### Passo 4 — Você leva para a PM e responde

```text
/legacy.answer REFINEMENT-0001
AMB-03: até 24 horas; acima disso, mostrar aviso de dado desatualizado.
AMB-04: mostrar "serviço indisponível, tente em alguns minutos".
AMB-05: aceito a sugestão (sim, data e hora).
Respondido por: Marina (PM).
```

O PO grava as respostas literais, escreve os critérios de aceite a partir delas e faz a revisão 2. Surge uma dúvida nova — o texto exato do aviso — que ele registra como **AMB-06, não bloqueante** (pode ser decidida no `/speckit.clarify`).

```text
REFINEMENT-0001 — revisão 2
Perguntas bloqueantes abertas: 0. Não bloqueantes: 1 (AMB-06).
Próximo: revise o arquivo e rode /legacy.approve REFINEMENT-0001 revisor: <nome>
```

### Passo 5 — Revisar e aprovar

Abra `.github/copilot-knowledge/refinements/REFINEMENT-0001-timeout-consulta-veiculos.md` (conteúdo completo no [capítulo 13](#13-o-refinamento-seção-por-seção)) e confira:

- os AC dizem o que a Marina quis?
- os guardrails cobrem o que não pode quebrar?
- a ordem das fatias faz sentido?

Então:

```text
/legacy.approve REFINEMENT-0001 revisor: Rafael Lima
```

```text
Resumo: 5 AC · 3 guardrails (1 exige teste de caracterização) · 3 fatias
Não decidido: onde tratar o timeout; texto do aviso (AMB-06); índice em HistoricoConsulta.
Aprovar REFINEMENT-0001 como Rafael Lima?
```

Você: `sim`.

```text
APPROVED — REFINEMENT-0001 (revisão 3) por Rafael Lima em 2026-09-18T16:40:00Z
validation passed: 3 artifact(s)
Próximo: /legacy.branch <descrição>
```

**E se você tentasse aprovar cedo demais?** Por exemplo, com a AMB-03 ainda aberta. O validador recusa e a aprovação é desfeita. Saída real:

```text
ERROR: ...REFINEMENT-0001-timeout-consulta-veiculos.md: open_questions is 1 but register has 2 OPEN_HUMAN
ERROR: ...REFINEMENT-0001-timeout-consulta-veiculos.md: READY_FOR_SPECKIT with blocking open questions: AMB-03
ERROR: ...REFINEMENT-0001-timeout-consulta-veiculos.md: READY_FOR_SPECKIT requires human reviewed_by and reviewed_at
ERROR: ...REFINEMENT-0001-timeout-consulta-veiculos.md: AC-01 derives from AMB-03, which has no human answer
ERROR: ...REFINEMENT-0001-timeout-consulta-veiculos.md: AC-02 derives from AMB-03, which has no human answer
ERROR: ...REFINEMENT-0001-timeout-consulta-veiculos.md: AC-02 is not covered by any SLICE
validation failed: 6 error(s)
```

```text
NOT_APPROVED — status restaurado para AWAITING_HUMAN.
```

### Passo 6 — Conferir o status

```text
/legacy.status REFINEMENT-0001
```

```text
| REFINEMENT-0001 | US-4821 — ... | READY_FOR_SPECKIT | 3 | HANDOFF-0003 (READY_FOR_SPECKIT) | 1 | /legacy.branch -> /speckit.specify |
```

O "1" em *Perguntas abertas* é a AMB-06, não bloqueante — ela segue para o `/speckit.clarify`.

### Passo 7 — Criar a branch

```text
/legacy.branch consulta-veiculos-timeout
```

```text
BRANCH_READY
branch: feature/092026/consulta-veiculos-timeout
base_commit: 4f2a9c1
```

### Passo 8 — Especificar no Spec Kit

```text
/speckit.specify US-4821 — Como atendente da central, quero que a consulta de veículos continue
mostrando a última situação conhecida quando o serviço da PBH demorar, para não deixar o cidadão
sem resposta.

Antes de escrever a spec, leia:
- .github/copilot-knowledge/handoffs/HANDOFF-0003-timeout-consulta-veiculos.md (AS-IS)
- .github/copilot-knowledge/refinements/REFINEMENT-0001-timeout-consulta-veiculos.md
Trate os AC-01..AC-05 e GR-01..GR-03 como requisitos. As considerações técnicas não são vinculantes.
```

### Passo 9 — O resto do Spec Kit

```text
/speckit.clarify     ← decide AMB-06 (texto do aviso)
/speckit.plan        ← decide onde tratar o timeout (controller? client?)
/speckit.tasks       ← respeite a ordem: SLICE-01 (testes de caracterização) primeiro
/speckit.analyze
/speckit.implement
/speckit.converge
```

Dica para o `/speckit.tasks`:

```text
/speckit.tasks Siga a ordem das fatias do REFINEMENT-0001. A primeira task cria o teste de
caracterização do GR-01 contra o comportamento atual, antes de qualquer mudança.
```

### Resumo do exemplo

```text
/legacy.story          → HANDOFF-0003 (READY) → REFINEMENT-0001 rev.1 (AWAITING_HUMAN, 3 perguntas)
/legacy.answer         → rev.2 (0 bloqueantes, AMB-06 não bloqueante)
/legacy.approve        → rev.3 READY_FOR_SPECKIT, revisado por Rafael Lima
/legacy.branch         → feature/092026/consulta-veiculos-timeout
/speckit.specify → clarify → plan → tasks → analyze → implement → converge
```

Tempo gasto por você: ler 3 perguntas, levar à PM, responder, revisar um arquivo. O que você **evitou**: implementar "sem limite de idade" e descobrir em produção que o atendente informou multa de 6 meses atrás.

---

## 12. Outros cenários

### 12.1 "Só quero entender uma parte do sistema"

```text
/legacy.analyze Como a emissão de segunda via do boleto calcula o vencimento?
```

Nenhuma história, nenhum refinamento. O conhecimento fica salvo para depois.

### 12.2 Bug simples (sei onde é, correção pontual)

```text
/legacy.bug Segunda via sai com vencimento no domingo; esperado próximo dia útil. Produção, desde 01/09.
```

Com a causa localizada e correção pontual:

```bash
specify extension add bug      # uma vez
```

```text
/speckit.bug.assess → /speckit.bug.fix → /speckit.bug.test
```

### 12.3 Bug complexo (muda regra, precisa de spec)

```text
/legacy.bug ...
/legacy.impact <método suspeito>
/legacy.story Corrigir cálculo de vencimento da segunda via para o próximo dia útil.
```

A partir daí, igual ao capítulo 11.

### 12.4 Retomar uma história parada

```text
/legacy.status
```

Olhe a coluna *Próximo comando* e siga. Ou simplesmente repita o `/legacy.story` com a mesma história — ele detecta o que existe e **retoma** em vez de recomeçar.

### 12.5 A história é grande demais

O PO marca `Small: GAP` e propõe fatias. Se as fatias mudarem **o que o usuário recebe em cada entrega**, ele pergunta:

```text
### AMB-07 — Posso entregar em 2 partes? (BLOQUEANTE)
- A) Parte 1: consulta por placa; Parte 2: consulta por RENAVAM.
- B) Tudo junto.
```

Se a PM preferir dividir em histórias separadas, cada uma ganha seu próprio `/legacy.story`.

### 12.6 A história contradiz o sistema atual

O HANDOFF diz: "o desconto máximo hoje é 10%". A história diz: "aplicar desconto de 15%" sem dizer que o limite muda. O PO **não escolhe**:

```text
### AMB-02 — O limite de 10% (DescontoService.cs:57) passa a ser 15% para todos? (BLOQUEANTE)
Motivo: STORY_CONFLICTS_WITH_AS_IS
- A) Sim, para todos → afeta relatório de margem (IMPACT-...)
- B) Só para o novo canal
- C) Não, 15% está errado na história
```

### 12.7 Não existe handoff

Se você usar `/legacy.refine` direto, sem handoff:

```text
REFINEMENT-0002 — BLOCKED (HANDOFF_MISSING)
Fiz apenas a triagem da história (2 perguntas de negócio registradas).
Próximo: /legacy.handoff <história literal>
```

O PO **não faz discovery no lugar do dono do AS-IS**. Por isso prefira `/legacy.story`, que já faz na ordem certa.

### 12.8 O handoff veio PARTIAL

```text
HANDOFF-0005 — PARTIAL
Bloqueante: não foi possível ver o consumidor externo do arquivo de remessa (outro repositório).
```

O refinamento **não pode** ficar pronto sobre um handoff PARTIAL. Opções: pedir a informação ao time dono do outro sistema e rodar `/legacy.handoff` de novo, ou registrar a decisão com a PM (que vira pergunta no refinamento).

### 12.9 Quem respondeu não é o dono da decisão

Se o `decision_owner` é a Marina e quem respondeu foi o Pedro, o PO registra "Pedro" na resposta e **avisa** no chat. Você decide se basta.

### 12.10 Mudou de ideia depois de aprovado

Rode `/legacy.refine` para a mesma história com o motivo. O PO atualiza **o mesmo arquivo** (mesmo ID, `revision` + 1), volta a `AWAITING_HUMAN` se houver pergunta, e exige nova `/legacy.approve`. Nunca cria `-v2` ou `-final`.

---

# Parte IV — Por dentro

## 13. O refinamento, seção por seção

Arquivo: `.github/copilot-knowledge/refinements/REFINEMENT-0001-timeout-consulta-veiculos.md`.
O conteúdo abaixo é o do exemplo do capítulo 11 e **passa no validador**.

### 13.1 Cabeçalho (frontmatter)

```yaml
---
schema_version: 1
artifact_type: STORY_REFINEMENT
id: REFINEMENT-0001
status: READY_FOR_SPECKIT
owner_skill: refine-user-story
created_at: 2026-09-18T14:10:00Z
updated_at: 2026-09-18T16:40:00Z
story_ref: "US-4821"
handoff: HANDOFF-0003
revision: 3
decision_owner: "Marina (PM)"
open_questions: 1
source_access: BOUNDED
reviewed_by: "Rafael Lima"
reviewed_at: 2026-09-18T16:40:00Z
block_reason: null
---
```

| Campo | O que é | Regra |
|---|---|---|
| `story_ref` | ID do item no board | ou `UNSPECIFIED` |
| `handoff` | AS-IS usado | precisa existir; em READY, precisa estar READY |
| `revision` | rodada | sobe a cada resposta/aprovação |
| `decision_owner` | quem decide negócio | obrigatório |
| `open_questions` | nº de perguntas `OPEN_HUMAN` | **tem que bater** com o registro |
| `source_access` | abriu código? | `NONE` ou `BOUNDED` |
| `reviewed_by/at` | quem aprovou | só via `/legacy.approve` |
| `block_reason` | por que travou | obrigatório em `BLOCKED` |

### 13.2 `## Story (verbatim)` — a história intocada

```markdown
> US-4821 — Como atendente da central, quero que a consulta de veículos continue mostrando a última
> situação conhecida quando o serviço da PBH demorar, para não deixar o cidadão sem resposta.
>
> Critério: não mostrar tela de erro quando der timeout.
```

Nunca é editada. Toda interpretação fica **fora** deste bloco.

### 13.3 `## Story Quality Assessment` — INVEST + DoR

```markdown
| Critério | Resultado | Observação |
|---|---|---|
| Testable | GAP | "demorar" não tem limite; "última situação" não tem validade → AMB-02, AMB-03 |
| DoR: critérios de aceite do PM | GAP | Só o critério negativo "não mostrar erro" → AMB-04 |
```

Todo `GAP` aponta para uma ambiguidade. O checklist não autoriza reescrever a história.

### 13.4 `## AS-IS Basis` — fatos rotulados

```markdown
- `FACT` — o timeout atual é 30 s, lido de `PbhTimeoutSeconds` no Web.config — `src/Consulta/PbhClient.cs:41`
- `INFERRED` — o relatório diário lê `HistoricoConsulta` — IMPACT-20260915-historico-consulta
- `UNKNOWN` — volume de timeouts em produção
```

`FACT` tem evidência citável. `INFERRED` é dedução. `UNKNOWN` é honestidade.

### 13.5 `## Scope` — dentro e fora

```markdown
### Out of scope
- Retry automático ao serviço da PBH.
- Alterar o valor do timeout de 30 s.
```

O "fora de escopo" lista o que alguém **poderia supor** que está dentro.

### 13.6 `## Ambiguity Register` — o coração

```markdown
| ID | Question | Why it matters | Source | Status | Blocking | Evidence / Answer |
|---|---|---|---|---|---|---|
| AMB-01 | Hoje existe retry na chamada à PBH? | ... | KNOWLEDGE | RESOLVED_BY_EVIDENCE | NO | HANDOFF-0003 § Current Behavior: chamada única, sem retry |
| AMB-02 | O que é "demorar"...? | ... | CODE | RESOLVED_BY_EVIDENCE | NO | `src/Consulta/PbhClient.cs:41` — 30 s ... |
| AMB-03 | Até quantas horas...? | ... | HUMAN | ANSWERED_BY_HUMAN | YES | "Até 24 horas; ..." — Marina (PM), 2026-09-18 |
| AMB-05 | O aviso deve informar a data/hora? | ... | HUMAN | ASSUMPTION_ACCEPTED | NO | Sugestão aceita: "sim, data e hora" — Marina (PM), 2026-09-18 |
| AMB-06 | Qual o texto exato do aviso? | ... | HUMAN | OPEN_HUMAN | NO | - |
```

| Coluna | Valores |
|---|---|
| Source | `STORY` · `KNOWLEDGE` · `CODE` · `HUMAN` |
| Status | `RESOLVED_BY_EVIDENCE` · `OPEN_HUMAN` · `ANSWERED_BY_HUMAN` · `ASSUMPTION_ACCEPTED` |
| Blocking | `YES` · `NO` |

### 13.7 `## Human Decisions Required`

As perguntas abertas no formato fechado (ver capítulo 14). Sem perguntas: `NONE`.

### 13.8 `## Acceptance Criteria` — cada AC tem origem

```markdown
| ID | Given / When / Then | Origin |
|---|---|---|
| AC-01 | Dado histórico com até 24 h, quando a PBH exceder o timeout, então exibe a última situação com aviso e data/hora | HUMAN:AMB-03 |
| AC-04 | Dado a PBH respondendo no prazo, quando consultar, então o comportamento é o atual | AS-IS:HANDOFF-0003 § Current Behavior |
| AC-05 | Dado timeout, quando consultar, então a tela `ErroConsulta` não é exibida | STORY |
```

| Origin | Significa |
|---|---|
| `STORY` | está escrito na história |
| `HUMAN:AMB-NN` | veio de uma resposta humana (**tem que estar respondida**) |
| `AS-IS:<evidência>` | preserva um comportamento atual |

AC sem origem ou vindo de pergunta sem resposta → **o validador recusa**.

### 13.9 `## Regression Guardrails`

```markdown
| ID | Preserved behavior | Evidence | Proof |
|---|---|---|---|
| GR-01 | Consulta bem-sucedida continua gravando em `HistoricoConsulta` | HANDOFF-0003 § Compatibility Constraints | CHARACTERIZATION_TEST_REQUIRED |
| GR-02 | Contrato SOAP com a PBH inalterado | HANDOFF-0003 § External Boundaries | EXISTING_TEST:tests/Consulta.Tests/PbhClientTests.cs::Envelope_Mantem_Contrato |
| GR-03 | Relatório diário continua lendo `HistoricoConsulta` igual | IMPACT-20260915-historico-consulta | MANUAL_CHECK:gerar relatório D-1 em homologação e comparar totais |
```

Detalhes no capítulo 15.

### 13.10 `## Risks and Dependencies`

```markdown
- `HistoricoConsulta` sem índice por placa — impacto médio em performance — `src/Consulta/HistoricoRepository.cs:17` — avaliar no `/speckit.plan`.
```

### 13.11 `## Execution Plan` — o planejamento de execução

```markdown
| Slice | Goal | AC | GR | Toolchain | Depends on |
|---|---|---|---|---|---|
| SLICE-01 | Rede de proteção: caracterizar o comportamento atual | AC-04 | GR-01, GR-02 | /speckit.tasks → testes de caracterização primeiro | - |
| SLICE-02 | Timeout com histórico recente | AC-01, AC-05 | GR-01, GR-02 | /speckit.specify → ... → /speckit.implement | SLICE-01 |
| SLICE-03 | Histórico antigo e ausência de histórico | AC-02, AC-03 | GR-01, GR-03 | /speckit.implement → /speckit.converge | SLICE-02 |

### Non-binding technical considerations
- O timeout é tratado no controller (`VeiculoController.cs:88`) e não no client; o `/speckit.plan` decide onde tratar.

### Size signals
- 1 projeto tocado; 1 integração externa; 1 consumidor indireto (relatório); 1 guardrail sem teste.
```

### 13.12 `## Explicitly Not Decided`

```markdown
- Onde tratar o timeout (controller, client ou nova camada) — `/speckit.plan`.
- Texto final do aviso — AMB-06, `/speckit.clarify`.
- Criação de índice em `HistoricoConsulta`.
```

Isso protege o Spec Kit de herdar decisões que ninguém tomou.

### 13.13 `## Next Steps`

```markdown
1. `/legacy.branch consulta-veiculos-timeout`
2. `/speckit.specify US-4821 …` lendo HANDOFF-0003 e REFINEMENT-0001.
```

## 14. Ambiguidades: como o PO decide quem responde

### 14.1 A escada

```text
1. STORY      o texto da história responde, sem interpretar?
2. KNOWLEDGE  HANDOFF / IMPACT / INVESTIGATION / DEEP-DIVE respondem?
3. CODE       leitura limitada responde um FATO de hoje?   (até 2 rodadas, 8 arquivos, 3 buscas)
4. HUMAN      ninguém respondeu → pergunta, registra, bloqueia se relevante
```

### 14.2 Vão direto para o humano

| Tipo | Exemplo |
|---|---|
| intenção / valor / prioridade | "isso é para todos os clientes ou só PJ?" |
| comportamento futuro não descrito | "e se não houver histórico?" |
| conflito história × AS-IS | "hoje o limite é 10%, a história diz 15%" |
| contrato externo | "o arquivo de remessa muda de layout?" |
| dado pessoal / regulatório / financeiro | "podemos logar o CPF?" |
| qualquer coisa que exigiria "assumir" | — |

### 14.3 Exemplos de cada degrau

| Dúvida | Degrau | Por quê |
|---|---|---|
| "Critério: não mostrar tela de erro" — mostra erro ou não? | STORY | está escrito |
| "Hoje tem retry?" | KNOWLEDGE | o handoff documentou |
| "Qual o timeout atual?" | CODE | é fato de hoje, está no código |
| "Qual deveria ser o timeout?" | HUMAN | é decisão, não fato |

### 14.4 Bloqueante ou não?

**YES** quando, sem a resposta: um AC não pode ser escrito/testado; pode mudar comportamento existente sem querer; envolve contrato externo, dado sensível, regra financeira; a história conflita com o AS-IS.
**NO** só quando dá para decidir no `/speckit.clarify` sem mudar escopo, AC ou guardrail (texto de mensagem, ordem de colunas).
**Na dúvida: YES.**

### 14.5 Pergunta boa × pergunta ruim

❌ Ruim:

```text
Como deve funcionar o timeout?
```

✅ Boa:

```text
### AMB-03 — Até quantas horas a "última situação" pode ser exibida? (BLOQUEANTE)
Contexto: HistoricoConsulta guarda todas as consultas (HANDOFF-0003). A história não limita a idade.
- A) Sem limite → atendente pode informar situação de meses atrás.
- B) Limite de N horas → acima disso, esconder ou mostrar com aviso?
- C) Outro.
Sugestão do PO (não aplicada): B com aviso, 24 h.
```

Fechada, com contexto, opções e consequência. Uma decisão por pergunta. Máximo 7 por rodada.

### 14.6 O que o PO nunca faz

- escolher "o mais comum";
- transformar sugestão em AC antes da resposta;
- rebaixar `Blocking` de YES para NO para aprovar mais rápido;
- apagar pergunta sem resposta;
- reinterpretar a resposta — se veio ambígua, pergunta de novo.

## 15. Guardrails de regressão e fatias

### 15.1 Guardrail = "isto não pode mudar, e eu provo assim"

| Situação | Proof | Exemplo |
|---|---|---|
| já existe teste automatizado | `EXISTING_TEST:<caminho::teste>` | `EXISTING_TEST:tests/Consulta.Tests/PbhClientTests.cs::Envelope_Mantem_Contrato` |
| não existe, mas dá para automatizar | `CHARACTERIZATION_TEST_REQUIRED` | vira a **primeira fatia** |
| não dá para automatizar agora | `MANUAL_CHECK:<o quê e onde>` | `MANUAL_CHECK:gerar relatório D-1 em homologação` |

Teste de caracterização = teste que **fotografa o comportamento atual** antes da mudança. Nasce verde. Se ficar vermelho depois, houve regressão.

Consumidor externo que não está no repositório **sempre** vira `MANUAL_CHECK` ou pergunta — nunca é ignorado.

Genuinamente nada existente é tocado? Em vez da tabela:

```markdown
NO_EXISTING_BEHAVIOR_AFFECTED — tela nova, sem consumidores (HANDOFF-0007 § Impact Surface)
```

### 15.2 Fatias

Ordem padrão:

```text
1. Rede de proteção (testes de caracterização)
2. Caminho feliz mínimo
3. Variações de regra
4. Erros e bordas
5. Dados existentes (migração), se a PM decidiu que existe
```

Regras verificadas pelo validador:

- toda fatia cobre ao menos 1 AC;
- **todo AC** e **todo GR** aparecem em alguma fatia;
- `Depends on` só cita fatias que existem;
- sem ciclo (`SLICE-01` → `SLICE-02` → `SLICE-01` é recusado).

### 15.3 O que o refinamento **não** planeja

| No refinamento ✅ | No Spec Kit ✅ |
|---|---|
| fatias de valor e ordem | arquitetura, classes, camadas |
| AC e GR por fatia | tasks de código, arquivos a alterar |
| pontos de atenção **não vinculantes** | decisão sobre esses pontos |
| sinais de tamanho | estimativa |

## 16. Status e ciclo de vida

### 16.1 HANDOFF

| Status | Significa | Próximo |
|---|---|---|
| `READY_FOR_SPECKIT` | AS-IS suficiente, sem unknown bloqueante | `/legacy.refine` |
| `PARTIAL` | útil, mas com lacuna relevante | fechar lacuna / `/legacy.handoff` |
| `BLOCKED` | falta evidência indispensável | resolver e `/legacy.handoff` |

### 16.2 REFINEMENT

```text
(intake) ──► AWAITING_HUMAN ◄──► /legacy.answer (revision+1)
                  │
                  ▼  (sem pergunta bloqueante)
             /legacy.approve ──► READY_FOR_SPECKIT
                  │ validador recusa
                  └──► volta ao status anterior

      qualquer momento ──► BLOCKED (sem handoff, conhecimento stale, conflito)
```

| Status | Significa | Próximo |
|---|---|---|
| `AWAITING_HUMAN` | há pergunta `OPEN_HUMAN` | `/legacy.answer` |
| `READY_FOR_SPECKIT` | claro, rastreável, protegido, aprovado | `/legacy.branch` |
| `BLOCKED` | pré-condição faltando | depende do `block_reason` |

### 16.3 Códigos de bloqueio

| Código | Significa | O que fazer |
|---|---|---|
| `HANDOFF_MISSING` | refinamento sem AS-IS | `/legacy.handoff` |
| `HUMAN_DECISION_REQUIRED` | decisão de negócio pendente | responder |
| `STORY_CONFLICTS_WITH_AS_IS` | história contradiz o sistema | PM decide qual vence |
| `KNOWLEDGE_STALE` | conhecimento salvo desatualizado | `/legacy.analyze` (refresh) |
| `DISCOVERY_BUDGET_EXHAUSTED` | orçamento de leitura acabou | responder ou ampliar escopo |
| `EVIDENCE_INSUFFICIENT` | não há evidência confiável | investigar / perguntar |

## 17. Governança: o que é bloqueado e por quem

| Regra | Quem garante |
|---|---|
| Refinamento só fica pronto com handoff pronto | validador |
| Nenhuma pergunta bloqueante aberta em READY | validador |
| AC não nasce de pergunta sem resposta | validador |
| Aprovação exige revisor humano | validador + `/legacy.approve` |
| Aprovação é desfeita se o validador recusar | `/legacy.approve` |
| Todo AC e GR estão em alguma fatia; sem ciclos | validador |
| Um dono por artefato | validador (`owner_skill`) |
| Nome e pasta canônicos | validador |
| Branch não nasce de refinamento não aprovado | `/legacy.branch` |
| Branch sem stash/reset/merge/force/push | `prepare-feature-branch` |
| Fluxo guiado não aprova, não cria branch, não chama Spec Kit | `/legacy.story` |
| Artefatos de skill não vão para o Git | `.git/info/exclude` + regra de todas as skills |
| Skills nunca escrevem em `.specify/` ou `specs/` | contrato de ownership |
| Pacote não regride em relação à v4 | suíte `tests/` (61 testes) |

**Privacidade.** Tudo em `.github/copilot-knowledge/` é **local-only**: não faça stage, commit ou push. O que vai para o Git é o que o Spec Kit gera (`specs/`). Se algo da knowledge foi rastreado por engano:

```bash
git rm --cached -r .github/copilot-knowledge
```

Nunca coloque dado pessoal real (CPF, nome de cidadão) em história, pergunta ou exemplo — use dados sintéticos.

---

# Parte V — Referência

## 18. Scripts de terminal

Rodar na **raiz do repositório**. Todos são Python puro (sem dependências).

| Comando | Faz | Escreve? |
|---|---|---|
| `python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge` | valida todos os artefatos | não |
| `python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge` | reconstrói o `INDEX.md` | só o INDEX |
| `python .github/skill-contracts/scripts/story_status.py [--id X]` | status das histórias + próximo comando | não |
| `python .github/skill-contracts/scripts/next_id.py --type REFINEMENT` | próximo ID livre (`HANDOFF`, `ADR`, `FIX`, `RFC` também) | não |
| `python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive` | arquiva artefatos de skill em ZIP fora do repo | cria ZIP |
| `python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive-and-clean` | arquiva e remove | **remove** |
| `python .github/skills/prepare-feature-branch/scripts/create_feature_branch.py --slug "x"` | cria a branch (a skill chama por você) | Git |

**Ordem obrigatória após editar artefato à mão:**

```bash
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
python .github/skill-contracts/scripts/sync_index.py        --root .github/copilot-knowledge
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
```

Nunca edite o `INDEX.md` à mão.

## 19. Mensagens do validador e como corrigir

Mensagens do `STORY_REFINEMENT` (as do handoff e demais artefatos seguem o mesmo padrão).

| Mensagem | Significa | Como corrigir |
|---|---|---|
| `READY_FOR_SPECKIT with blocking open questions: AMB-03` | tentou aprovar com pergunta bloqueante aberta | `/legacy.answer` |
| `AC-01 derives from AMB-03, which has no human answer` | AC construído sobre suposição | responder a AMB-03 |
| `READY_FOR_SPECKIT requires human reviewed_by and reviewed_at` | sem revisão humana | `/legacy.approve ... revisor: <nome>` |
| `READY_FOR_SPECKIT requires HANDOFF-0003 to be READY_FOR_SPECKIT (is PARTIAL)` | AS-IS incompleto | fechar lacuna, `/legacy.handoff` |
| `READY_FOR_SPECKIT requires an existing handoff` | `handoff: NONE` | `/legacy.handoff` |
| `handoff HANDOFF-0009 not found in knowledge base` | referência quebrada | corrigir o ID no refinamento |
| `open_questions is 1 but register has 2 OPEN_HUMAN` | contador desatualizado | `/legacy.refine` para atualizar |
| `AWAITING_HUMAN requires at least one OPEN_HUMAN ambiguity` | status errado | aprovar ou reabrir pergunta |
| `BLOCKED refinement lacks block_reason` | bloqueio sem motivo | informar código (cap. 16.3) |
| `AMB-01 resolved by evidence cannot have Source HUMAN` | humano não é "evidência" | usar `ANSWERED_BY_HUMAN` |
| `AMB-01 resolved by evidence lacks evidence` | resolvido sem citar fonte | citar artefato ou `arquivo:linha` |
| `AMB-02 lacks the recorded human answer` | status respondido sem resposta | registrar resposta literal |
| `AC-01 has invalid Origin ...` | origem fora do padrão | `STORY`, `HUMAN:AMB-NN`, `AS-IS:...` |
| `GR-01 has invalid Proof ...` | prova fora do padrão | `EXISTING_TEST:`, `CHARACTERIZATION_TEST_REQUIRED`, `MANUAL_CHECK:` |
| `requires GR-NN rows or NO_EXISTING_BEHAVIOR_AFFECTED` | sem guardrail | listar o que não pode quebrar |
| `AC-02 is not covered by any SLICE` | AC fora do plano | incluir numa fatia |
| `GR-01 is not covered by any SLICE` | guardrail fora do plano | incluir numa fatia |
| `SLICE-02 references unknown AC-09` | ID inexistente | corrigir referência |
| `Execution Plan has a dependency cycle between slices` | fatias dependem em ciclo | reordenar |
| `STORY_REFINEMENT missing section ## ...` | seção obrigatória faltando | ver capítulo 13 |
| `owner ... must be refine-user-story` | outra skill escreveu | refazer pelo dono |
| `STORY_REFINEMENT must be stored under refinements` | pasta errada | mover para `refinements/` |
| `non-canonical filename for STORY_REFINEMENT` | nome fora do padrão | `REFINEMENT-NNNN-slug-minusculo.md` |

## 20. Onde fica cada coisa

| O quê | Onde | Vai para o Git? |
|---|---|---|
| Comandos | `.github/prompts/legacy.*.prompt.md` | sim (ferramental do time) |
| Skills | `.github/skills/<nome>/SKILL.md` | sim |
| Contratos e scripts | `.github/skill-contracts/` | sim |
| Índice | `.github/copilot-knowledge/INDEX.md` | **não** |
| Handoffs | `.github/copilot-knowledge/handoffs/` | **não** |
| Refinamentos | `.github/copilot-knowledge/refinements/` | **não** |
| Mapa do sistema | `.github/copilot-knowledge/projects/`, `decisions/`, `deep-dives/` | **não** |
| Instalação | `.github/legacy-discovery/installation.json` | **não** |
| Spec Kit | `.specify/`, `specs/` | sim (política do time) |

Nomes:

| Artefato | Nome |
|---|---|
| Handoff | `HANDOFF-0003-timeout-consulta-veiculos.md` |
| Refinamento | `REFINEMENT-0001-timeout-consulta-veiculos.md` |
| Investigação | `INVESTIGATION-20260918-vencimento-domingo.md` |
| Impacto | `IMPACT-20260915-historico-consulta.md` |
| Branch | `feature/092026/consulta-veiculos-timeout` |

## 21. Solução de problemas

| Problema | Causa provável | Solução |
|---|---|---|
| `/legacy.` não aparece no chat | chat não está em Agent Mode, VS Code/Copilot desatualizado ou prompt files desabilitados | trocar para Agent; atualizar; conferir a configuração `chat.promptFiles` nas Settings; recarregar a janela |
| Aparecem os comandos do Spec Kit como `/speckit-specify` em vez de `/speckit.specify` | nome depende da integração do Spec Kit instalada | use o nome que aparece no menu `/` |
| `Python 3.11+ não encontrado` | Python ausente ou antigo | instalar Python 3.11+ e marcar "Add to PATH" |
| Instalador: `não parece ser a raiz de um repositório Git` | pasta errada | informar a pasta que contém `.git` |
| Testes do pacote falham com arquivos "faltando" no Windows | caminho longo (>260) | mover o pacote para `C:\Ferramentas\` |
| `SHA256SUMS.txt` não confere após clonar do GitHub | conversão CRLF | a pasta tem `.gitattributes`; se copiou manualmente, baixe o `.zip` |
| `validation failed` depois de editar à mão | contrato quebrado | ver capítulo 19; rodar `/legacy.validate` |
| `/legacy.branch` recusa | refinamento não aprovado ou worktree sujo | `/legacy.status`; commit/stash; aprovar |
| O PO "não sabe" algo que está no código | orçamento de leitura (8 arquivos) acabou | responder a pergunta, ou `/legacy.analyze` na área e refinar de novo |
| Refinamento travado em `BLOCKED: HANDOFF_MISSING` | refinou antes do handoff | `/legacy.handoff <história>` e depois `/legacy.refine` |
| Acentos estranhos no terminal do instalador | página de código do console | apenas visual; não afeta os arquivos |
| Artefato de skill apareceu no `git status` | `.git/info/exclude` removido | reinstalar com `--skip-speckit-install --skip-speckit-init` |

## 22. Boas práticas e armadilhas

**Faça**

- cole a história **literal** do PM — o valor do PO está em comparar com o original;
- diga sempre quem decide negócio (`Quem decide: Marina (PM)`);
- leve as perguntas à PM como estão: já vêm com opções e consequências;
- leia o refinamento antes de aprovar — a assinatura é sua;
- comece o `/speckit.tasks` pelos testes de caracterização (SLICE-01);
- use `/legacy.status` no início do dia;
- rode `/legacy.analyze` em áreas novas antes da primeira história delas.

**Evite**

- responder "faz o que achar melhor" — o PO vai perguntar de novo, e deve;
- editar o refinamento à mão para "passar" no validador;
- pular o handoff chamando `/legacy.refine` direto;
- aprovar com pressa só porque "não tem bloqueante" — revise os AC;
- colocar dado real de cliente em história ou exemplo;
- commitar `.github/copilot-knowledge/`.

## 23. Cola rápida

```text
┌──────────────────────── HISTÓRIA DO PM ────────────────────────┐
│ /legacy.story <história literal>  Quem decide: <PM>            │
│      ↓ perguntas?                                              │
│ /legacy.answer REFINEMENT-NNNN AMB-02: ...; AMB-03: ...        │
│      ↓ sem bloqueantes, arquivo revisado                       │
│ /legacy.approve REFINEMENT-NNNN revisor: <seu nome>            │
│      ↓                                                         │
│ /legacy.branch <descricao-curta>                               │
│      ↓                                                         │
│ /speckit.specify <história>. Leia HANDOFF-NNNN e REFINEMENT-NNNN│
│ /speckit.clarify → plan → tasks → analyze → implement → converge│
└────────────────────────────────────────────────────────────────┘

ENTENDER      /legacy.analyze <área>
BUG           /legacy.bug <sintoma + esperado + ambiente>
IMPACTO       /legacy.impact <alvo + tipo de mudança>
ONDE ESTOU?   /legacy.status      ·   /legacy.help
CONFERIR      /legacy.validate
LIMPAR        /legacy.archive [limpar]

REGRA DE OURO: o código diz como é. Só o humano diz como deve ser.
```
