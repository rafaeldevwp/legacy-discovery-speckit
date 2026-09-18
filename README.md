# Legacy Discovery + Spec Kit — pacote único

Este ZIP existe para você **não precisar instalar e juntar duas coisas manualmente**.

Ele combina:

1. **GitHub Spec Kit oficial** — fixado em `specify-cli 1.0.1`;
2. **Legacy Discovery V2.2** — suas Skills para entender o AS-IS de sistemas legados grandes;
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
5. instala suas 5 Skills ativas (4 de Discovery + 1 de Git)
6. instala os contratos e scripts do Knowledge Store
7. cria .github/copilot-knowledge
8. arquiva skills antigas da V1, sem apagá-las
9. valida a estrutura instalada
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
│   ├── prompts/                  ← Spec Kit / Copilot
│   ├── skills/
│   │   ├── analyze-legacy-solution/
│   │   ├── investigate-legacy-bug/
│   │   ├── analyze-change-impact/
│   │   ├── prepare-speckit-context/
│   │   └── prepare-feature-branch/
│   ├── skill-contracts/
│   ├── copilot-knowledge/
│   │   ├── INDEX.md
│   │   ├── projects/
│   │   ├── decisions/
│   │   ├── deep-dives/
│   │   ├── investigations/
│   │   ├── impact-analyses/
│   │   └── handoffs/
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

primeiro crie a branch de trabalho:

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

# Quando usar cada Skill?

| Quero... | Use |
|---|---|
| entender uma área do legado | `analyze-legacy-solution` |
| investigar bug complexo | `investigate-legacy-bug` |
| saber o raio de impacto | `analyze-change-impact` |
| preparar uma US para o Spec Kit | `prepare-speckit-context` |
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
Bundle:              1.2.0
Legacy Discovery:    V2.2
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
