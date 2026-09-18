# Legacy Discovery + Spec Kit — pacote único

Este ZIP existe para você **não precisar instalar e juntar duas coisas manualmente**.

Ele combina:

1. **GitHub Spec Kit oficial** — fixado em `specify-cli 1.0.1`;
2. **Legacy Discovery V2.3** — suas Skills para entender o AS-IS de sistemas legados grandes e refinar histórias antes do Spec Kit;
3. **instalador único** — inicializa o Spec Kit e instala as Skills no mesmo repositório;
4. **Persistent Knowledge + HANDOFF** — a ponte entre Discovery e Spec Kit.

> Importante: este é um **bundle de instalação**, não um pacote air-gapped. Você baixa **um único ZIP**, mas na primeira execução o instalador usa a internet para obter o `specify-cli==1.0.1` oficial e suas dependências. Depois ele faz toda a montagem automaticamente.

---

## Para que serve?

Pense assim:

```text
SISTEMA LEGADO
     │
     ▼
Legacy Discovery
"Como funciona hoje?"
     │
     ▼
Persistent Knowledge
     │
     ▼
HANDOFF
     │
     ▼
Spec Kit
"O que vamos mudar?"
     │
     ▼
Spec → Plan → Tasks → Implement → Converge
```

O Discovery não decide a solução futura. O Spec Kit não precisa redescobrir o legado inteiro a cada User Story.

---

# Instalação rápida — Windows

## Você precisa ter

- Git;
- VS Code;
- GitHub Copilot funcionando;
- Python **3.11 ou superior**;
- internet na primeira instalação.

`uv` é recomendado, mas **não é obrigatório**: se o instalador não encontrar `uv`, usa `pip`.

## Passo 1 — proteja seu código

Na raiz do legado:

```bash
git status
```

Faça commit ou stash do que não quiser misturar com a instalação.

## Passo 2 — descompacte este ZIP

Pode ser fora do seu repositório, por exemplo:

```text
C:\Ferramentas\legacy-speckit-all-in-one\
```

## Passo 3 — execute

Dê dois cliques em:

```text
INSTALAR-WINDOWS.bat
```

Ele perguntará:

```text
Repositorio: C:\Projetos\MeuSistemaLegado
```

Informe a **raiz do repositório**, onde existe a pasta/arquivo `.git`.

Pronto. O instalador faz o restante.

---

# O que o instalador faz?

Automaticamente:

```text
1. cria backup preventivo
2. instala specify-cli 1.0.1 oficial
3. executa Spec Kit no repositório existente
4. configura integração GitHub Copilot
5. instala suas 6 Skills ativas (4 de Discovery + 1 de PO + 1 de Git)
6. instala os contratos e scripts do Knowledge Store
7. cria .github/copilot-knowledge
8. arquiva skills antigas da V1, sem apagá-las
9. instala os comandos `/legacy.*` em `.github/prompts/`
10. valida a estrutura instalada
```

O comando de inicialização equivalente é:

```bash
specify init --here --force --non-interactive --integration copilot --ignore-agent-tools
```

---

# O que ficará dentro do seu repositório?

A estrutura principal será semelhante a:

```text
SEU-LEGADO/
├── .github/
│   ├── prompts/                  ← Spec Kit / Copilot + comandos legacy.*.prompt.md
│   ├── skills/
│   │   ├── analyze-legacy-solution/
│   │   ├── investigate-legacy-bug/
│   │   ├── analyze-change-impact/
│   │   ├── prepare-speckit-context/
│   │   ├── prepare-feature-branch/
│   │   └── refine-user-story/
│   ├── skill-contracts/
│   ├── copilot-knowledge/
│   │   ├── INDEX.md
│   │   ├── projects/
│   │   ├── decisions/
│   │   ├── deep-dives/
│   │   ├── investigations/
│   │   ├── impact-analyses/
│   │   ├── handoffs/
│   │   └── refinements/
│   └── legacy-discovery/
├── .specify/                     ← Spec Kit
├── specs/                        ← features do Spec Kit
└── seu código...
```

Se forem encontradas as antigas skills:

```text
coordinate-fix
execute-fix-plan
run-solution-regression
```

elas são movidas para:

```text
.github/legacy-workflow-v1/
```

Nada é simplesmente descartado.

---

# Primeiro uso

Abra a raiz do repositório no VS Code e abra o Copilot em **Agent Mode**.

## 1. Defina as regras do projeto

Execute uma única vez:

```text
/speckit.constitution
```

Exemplo de pedido:

```text
Este é um sistema legado crítico.
Preserve contratos e compatibilidade existentes.
Não modernize tecnologia sem justificativa explícita.
Trate os HANDOFFs do Legacy Discovery como contexto factual AS-IS.
Decisões TO-BE pertencem ao Spec Kit.
Não trate inferência como fato.
```

Quando evoluir para `/speckit.plan`, preserve a arquitetura existente por padrão e use o HANDOFF apenas como base factual para enriquecer decisões.

## 2. Faça o primeiro mapa do legado

No Copilot:

```text
Use a skill analyze-legacy-solution para iniciar o conhecimento deste repositório.
Faça discovery progressivo.
Comece por estrutura, projetos, responsabilidades, dependências,
integrações e arquivos-âncora.
Persista em .github/copilot-knowledge.
Não implemente e não proponha modernização.
```

Não peça para estudar milhares de arquivos profundamente de uma vez.

---

# Comandos `/legacy.*` — suas skills como comandos

Assim como o Spec Kit tem `/speckit.*`, o pacote instala comandos `/legacy.*` no Copilot (prompt files em `.github/prompts/`). No chat em Agent Mode, digite `/legacy.` e escolha.

| Comando | O que faz | Skill / script |
|---|---|---|
| `/legacy.help` | Lista os comandos e sugere o próximo passo de cada história | `story_status.py` |
| `/legacy.story <história>` | **Fluxo guiado**: handoff → refinamento, parando em cada decisão humana | várias |
| `/legacy.analyze <área>` | Mapeia o AS-IS | `analyze-legacy-solution` |
| `/legacy.bug <sintoma>` | Investiga bug, sem corrigir | `investigate-legacy-bug` |
| `/legacy.impact <alvo>` | Raio de impacto | `analyze-change-impact` |
| `/legacy.handoff <mudança>` | Gera o HANDOFF (AS-IS da mudança) | `prepare-speckit-context` |
| `/legacy.refine <história>` | PO técnico gera o REFINEMENT | `refine-user-story` |
| `/legacy.answer <REFINEMENT> AMB-02: …` | Registra suas respostas às perguntas | `refine-user-story` |
| `/legacy.approve <REFINEMENT> revisor: <nome>` | Registra sua revisão e libera `READY_FOR_SPECKIT` | `refine-user-story` + validador |
| `/legacy.branch <descrição>` | Cria `feature/mmYYYY/...` a partir da `main` | `prepare-feature-branch` |
| `/legacy.status [ID]` | Estado das histórias e próximo comando (somente leitura) | `story_status.py` |
| `/legacy.validate` | Valida contratos e reconstrói o INDEX | `validate_artifacts.py`, `sync_index.py` |
| `/legacy.archive [limpar]` | Arquiva artefatos locais das skills | `archive_skill_artifacts.py` |

Fluxo completo de uma história do PM, só com comandos:

```text
/legacy.story <história do PM>
/legacy.answer REFINEMENT-0001 AMB-02: A; AMB-03: 24 horas
/legacy.approve REFINEMENT-0001 revisor: <seu nome>
/legacy.branch tratar-timeout-consulta
/speckit.specify <história do PM>. Leia o HANDOFF-0001 e o REFINEMENT-0001.
/speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.analyze → /speckit.implement → /speckit.converge
```

Os comandos **não** trocam as skills: são atalhos que carregam a skill certa com as entradas certas. Os guardrails continuam nas skills e nos scripts de contrato. Garantias:

- prefixo próprio `legacy.` — não colide com `/speckit.*`;
- o instalador só grava arquivos `legacy.*.prompt.md`; qualquer outro prompt em `.github/prompts/` fica intacto;
- `/legacy.story` nunca cria branch nem chama o Spec Kit, e nunca aprova;
- `/legacy.approve` é o único caminho de aprovação, é digitado por você e desfaz a aprovação se o validador recusar;
- `/legacy.branch` recusa seguir se a história tem refinamento ainda não aprovado.

Pedir as skills pelo nome (`Use a skill ... para ...`) continua funcionando como antes.

---

# Uso diário — nova User Story

Imagine:

> Alterar a consulta de veículos para tratar timeout sem perder o último estado conhecido.

Primeiro:

```text
Use a skill prepare-speckit-context para esta mudança:

Alterar a consulta de veículos para tratar timeout sem perder o último estado conhecido.

Reutilize primeiro o Persistent Knowledge.
Abra source somente para gaps.
Não proponha TO-BE.
Não implemente.
Gere o SPECKIT_HANDOFF.
```

A Skill verifica:

```text
já sabemos o suficiente?
      │
   ┌──┴──┐
  SIM   NÃO
   │      │
reusa   investiga apenas o gap
   └──┬───┘
      ▼
   HANDOFF
```

Quando retornar:

```text
READY_FOR_SPECKIT
```

refine a história com o PO técnico:

```text
Use a skill refine-user-story para refinar esta história do PM:

<história literal do PM>

Use o HANDOFF gerado como base AS-IS.
```

Responda as perguntas que ela devolver. Quando o refinamento estiver `READY_FOR_SPECKIT` (só acontece após sua revisão), crie a branch de trabalho:

```text
Use a skill prepare-feature-branch para esta mudança.
```

Ela atualiza `main` somente por fast-forward e cria:

```text
feature/mmYYYY/descricao-curta
```

Exemplo:

```text
feature/082026/tratar-timeout-pbh
```

Depois siga com:

```text
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.tasks
/speckit.analyze
/speckit.implement
/speckit.converge
```

---

# Branch Git antes do Spec Kit

Para mudanças que serão implementadas, o fluxo padrão inclui uma branch dedicada:

```text
HANDOFF READY
    ↓
prepare-feature-branch
    ↓
main atualizada com --ff-only
    ↓
feature/mmYYYY/descricao-curta
    ↓
/speckit.specify
```

A Skill nunca executa `stash`, `reset`, `merge`, `rebase`, `force` ou `push` automaticamente. Se o worktree estiver sujo, `main` estiver divergente ou a branch já existir, ela bloqueia e pede decisão humana.

# Política de versionamento (v4)

- Artefatos gerados por skill permanecem local-only por padrão.
- Escopo mínimo local-only: `.github/copilot-knowledge/` e `.github/legacy-discovery/installation.json`.
- Artefatos gerados pelo Spec Kit (`.specify/` e `specs/`) seguem a política normal de versionamento da equipe.
- O instalador configura `.git/info/exclude` local para reduzir stage acidental.

Comando para arquivar artefatos/metadados da skill e reduzir poluição local:

```bash
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive-and-clean
```

# Refinamento técnico com PO — `refine-user-story`

Quando o PM entrega uma User Story, a skill `refine-user-story` faz o papel de **PO técnico**: confronta a história com o AS-IS já descoberto e produz um `STORY_REFINEMENT` — o artefato de planejamento de execução (refinamento técnico) que o Spec Kit vai consumir.

```text
História do PM ──► prepare-speckit-context ──► HANDOFF (AS-IS)
                                                   │
                                                   ▼
                                          refine-user-story
                                                   │
                     ┌─────────────────────────────┼──────────────────────────┐
                     ▼                             ▼                          ▼
               AWAITING_HUMAN               READY_FOR_SPECKIT              BLOCKED
          perguntas ao humano ─resposta─►  (após revisão humana)      (falta handoff/…)
                                                   │
                                                   ▼
                              prepare-feature-branch ──► /speckit.specify …
```

Exemplo de pedido:

```text
Use a skill refine-user-story para refinar esta história do PM:

<cole a história exatamente como o PM escreveu>

Use o HANDOFF-0003 como base AS-IS.
Quem decide regra de negócio: <nome do PM>.
```

## O que o refinamento contém

- a história **literal** do PM, separada de qualquer interpretação;
- avaliação INVEST + Definition of Ready;
- registro de ambiguidades `AMB-NN`, cada uma com a fonte que a respondeu;
- critérios de aceite `AC-NN` (Given/When/Then), cada um com origem rastreável;
- guardrails de regressão `GR-NN`: o que não pode mudar e como será provado;
- plano de execução em fatias `SLICE-NN`, com ordem, AC/GR cobertos e o passo do ferramental;
- o que **não** foi decidido (fica para o humano e para o `/speckit.plan`).

## Ambiguidades: quem responde

**O código responde "como é hoje". Só o humano responde "como deve ser".**

```text
STORY → KNOWLEDGE (handoff/impact/…) → CODE (só fato AS-IS, até 8 arquivos) → HUMAN
```

Intenção de negócio, escopo, conflito entre história e AS-IS, contrato externo e dado sensível vão **direto** ao humano. A pergunta é fechada, com opções e consequência; a sugestão do PO nunca é aplicada sem resposta.

## Guardrails verificados por script

`validate_artifacts.py` recusa um refinamento `READY_FOR_SPECKIT` quando:

- o handoff relacionado não existe ou não está `READY_FOR_SPECKIT`;
- há pergunta `OPEN_HUMAN` bloqueante;
- não há revisão humana (`reviewed_by` / `reviewed_at`);
- um AC nasce de pergunta não respondida, ou não tem origem;
- algum AC ou guardrail não está coberto por nenhuma fatia, ou há ciclo entre fatias;
- faltam guardrails de regressão (ou a justificativa `NO_EXISTING_BEHAVIOR_AFFECTED`).

A skill não escreve em `.specify/`/`specs/`, não decide arquitetura, não cria tasks de código, não mexe em Git e não edita artefatos de outras skills. O refinamento é **local-only**, como os demais artefatos de skill.

---

# Testes de não-regressão do pacote

O pacote traz `tests/` (não é instalado no repositório). Rode na raiz do pacote:

```bash
python -m unittest discover -s tests -v
```

A suíte prova que:

- sem refinamentos, `validate_artifacts.py`, `sync_index.py` e `next_id.py` produzem **saída idêntica, byte a byte,** à da versão anterior (cópia congelada em `tests/baseline_v4_scripts/`);
- os arquivos das 5 skills anteriores e do workflow V1 são idênticos aos da versão anterior (`tests/baseline_v4_skill_digests.json`);
- o instalador preserva conhecimento existente, `.git/info/exclude` e o arquivamento V1;
- cada guardrail do refinamento recusa o caso que deveria recusar.

> No Windows, descompacte o pacote num caminho curto (ex.: `C:\Ferramentas\`). Caminhos acima de 260 caracteres fazem o Python ignorar arquivos profundos.

---

# Quando usar cada Skill?

| Quero... | Use |
|---|---|
| entender uma área do legado | `analyze-legacy-solution` |
| investigar bug complexo | `investigate-legacy-bug` |
| saber o raio de impacto | `analyze-change-impact` |
| preparar uma US para o Spec Kit | `prepare-speckit-context` |
| refinar a história do PM (PO técnico) | `refine-user-story` |
| criar a branch segura da mudança | `prepare-feature-branch` |
| especificar o TO-BE | `/speckit.specify` |
| definir arquitetura futura | `/speckit.plan` |
| decompor implementação | `/speckit.tasks` |
| implementar | `/speckit.implement` |

---

# Regra simples para não se perder

```text
QUERO ENTENDER
      ↓
Legacy Discovery

QUERO MUDAR
      ↓
prepare-speckit-context
      ↓
HANDOFF
      ↓
refine-user-story  ⇄  humano responde
      ↓
REFINEMENT
      ↓
prepare-feature-branch
      ↓
Spec Kit
```

---

# Backup

Antes de alterar arquivos controlados pelo bundle, o instalador cria um backup em:

```text
<PASTA-DESTE-INSTALADOR>/backups/<repositorio>-AAAAmmdd-HHMMSS/
```

Depois da instalação, sempre confira:

```bash
git status
git diff
```

---

# Instalação manual / avançada

PowerShell:

```powershell
.\install.ps1 -TargetPath "C:\Projetos\MeuSistemaLegado"
```

Python:

```bash
python install.py --target "C:\Projetos\MeuSistemaLegado"
```

Linux/macOS:

```bash
./install.sh /caminho/do/repositorio
```

Se o Spec Kit já estiver instalado e você quiser apenas atualizar o Discovery:

```bash
python install.py --target /caminho/repo --skip-speckit-install --skip-speckit-init
```

Para manter as skills V1 ativas durante uma migração temporária:

```bash
python install.py --target /caminho/repo --keep-legacy-v1
```

---

# Versões deste pacote

```text
Bundle:              1.3.0
Legacy Discovery:    V2.3
Spec Kit / CLI:      1.0.1
Integração padrão:   GitHub Copilot
Python mínimo:       3.11
```

Consulte também:

```text
bundle.json
vendor/spec-kit/README.md
payload/legacy-discovery/
```
