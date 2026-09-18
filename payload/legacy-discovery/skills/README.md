# Legacy Discovery Skills + Spec Kit — V2

Conjunto de skills para **compreender e investigar repositórios .NET legados grandes** e transferir contexto AS-IS confiável ao **Spec Kit oficial**, sem transformar o Discovery em outro framework de especificação.

A V2 separa responsabilidades de forma explícita:

```text
LEGADO / AS-IS
    ↓
analyze-legacy-solution
investigate-legacy-bug
analyze-change-impact
    ↓
.github/copilot-knowledge/
    ↓
prepare-speckit-context
    ↓
SPECKIT_HANDOFF
    ↓
SPEC KIT / TO-BE
    ↓
specify → clarify → plan → tasks → analyze → implement → converge
```

## Por que esta V2 existe

A versão anterior também gerava e executava um workflow próprio de `SPEC → DESIGN → TASKS`. Isso funcionava isoladamente, mas passava a competir com o Spec Kit quando os dois eram usados juntos.

Na V2:

- o **Discovery** continua sendo responsabilidade destas skills;
- a **Persistent Knowledge** continua em `.github/copilot-knowledge/`;
- o **Spec Kit** passa a ser a única fonte de verdade para especificação, plano técnico, tarefas e implementação da mudança;
- o contrato entre os dois lados é o `SPECKIT_HANDOFF`.

## Politica global de privacidade

Neste repositorio, todo artefato gerado por skill e local-only.

- Nao publicar artefatos de skill em remoto, independentemente da pasta.
- Caminhos com bloqueio minimo de versionamento: `.github/copilot-knowledge/` e `.github/legacy-discovery/installation.json`.
- Artefatos de Spec Kit (`.specify/` e `specs/`) seguem a politica normal de versionamento da equipe.
- Se artefatos de skill estiverem rastreados pelo Git, remova do indice (`git rm --cached`) antes de push.
- Para reduzir risco de stage acidental, use o configurador local em `.git/info/exclude` fornecido pelo instalador.

## Skills ativas

### `analyze-legacy-solution`

Mapeia a estrutura e o comportamento arquitetural observável da solution/repositório. Trabalha com progressive disclosure e persistência local.

Principais saídas:

- `SOLUTION-OVERVIEW.md`;
- `projects/PROJECT-*.md`;
- `decisions/ADR-*.md` quando uma decisão existente puder ser inferida com evidência;
- `deep-dives/DEEP-DIVE-*.md` sob demanda.

Não planeja modernização e não produz artefatos TO-BE na V2.

### `investigate-legacy-bug`

Investiga um comportamento inesperado no legado e registra hipóteses/evidências sem corrigir o source.

Principais saídas:

- `investigations/INVESTIGATION-*.md`;
- evidência de reprodução/teste quando explicitamente solicitada;
- `knowledge_updates` para conhecimento estrutural descoberto.

### `analyze-change-impact`

Mapeia o raio de impacto antes da mudança.

Principal saída:

- `impact-analyses/IMPACT-*.md`.

### `prepare-speckit-context`

É a ponte oficial da V2.

Ela:

1. lê `INDEX.md` primeiro;
2. mede cobertura da solicitação atual;
3. evita source access quando o conhecimento salvo já é suficiente;
4. investiga apenas gaps relevantes quando necessário;
5. produz `handoffs/HANDOFF-*.md`;
6. recomenda o próximo comando do Spec Kit, sem executá-lo automaticamente.

### `prepare-feature-branch`

Mantem o gate de governanca Git e cria branch de trabalho no padrao `feature/mmYYYY/descricao-curta` a partir de `main` atualizada por fast-forward.

Principal saída:

- `handoffs/HANDOFF-{NNNN}-{slug}.md` (`artifact_type: SPECKIT_HANDOFF`).

## Persistent Knowledge

```text
.github/copilot-knowledge/
├── INDEX.md
├── SOLUTION-OVERVIEW.md
├── projects/
├── decisions/
├── deep-dives/
├── investigations/
├── impact-analyses/
└── handoffs/
```

Diretórios antigos como `proposals/` e `fix-plans/` continuam aceitos pelos scripts para compatibilidade com repositórios que já possuem histórico da V1, mas não são produzidos pelo fluxo ativo da V2.

## Knowledge Gate

A nova regra é **suficiência**, não simplesmente existência de conhecimento.

```text
INDEX
  ↓
artefatos relevantes
  ↓
coverage por dimensão
  ↓
COVERED? ── sim ──→ não abrir source
  │
  não
  ↓
PARTIAL / UNKNOWN / STALE
  ↓
discovery incremental limitado ao gap
  ↓
HANDOFF
```

Dimensões avaliadas:

- `STRUCTURE`;
- `CURRENT_BEHAVIOR`;
- `BUSINESS_RULES`;
- `DEPENDENCIES`;
- `IMPACT_SURFACE`;
- `EXTERNAL_BOUNDARIES`;
- `TEST_SAFETY_NET`.

## Fluxo recomendado para uma feature/mudança

```text
1. Entenda/reuse o legado
2. Analise impacto quando necessário
3. prepare-speckit-context
4. Revise HANDOFF
5. /speckit.specify
6. /speckit.clarify
7. /speckit.plan
8. /speckit.tasks
9. /speckit.analyze
10. /speckit.implement
11. /speckit.converge
```

## Fluxo de bug

Há dois caminhos válidos:

### Bug complexo que precisa passar por SDD

```text
investigate-legacy-bug
→ analyze-change-impact
→ prepare-speckit-context (target_flow: SDD)
→ Spec Kit core
```

### Bug pontual usando a extensão oficial de bug do Spec Kit

```text
prepare-speckit-context (opcional, especialmente útil em legado grande)
→ /speckit.bug.assess
→ /speckit.bug.fix
→ /speckit.bug.test
```

A extensão de bug é opt-in no Spec Kit. Consulte `prepare-speckit-context/references/speckit-integration.md`.

## Instalação destas skills

Copie para o repositório:

```text
.github/
├── skills/
│   ├── analyze-legacy-solution/
│   ├── investigate-legacy-bug/
│   ├── analyze-change-impact/
│   ├── prepare-speckit-context/
│   └── prepare-feature-branch/
└── skill-contracts/
```

Não copie `legacy-workflow/skills/` para `.github/skills/` se você pretende usar o Spec Kit como SDD oficial.

## Spec Kit em projeto existente

Inicialize o Spec Kit separadamente e revise o diff gerado. Exemplo para integração GitHub Copilot:

```bash
specify init --here --force --integration copilot
```

Depois capture guardrails reais do projeto em `/speckit.constitution`.

## Princípios da V2

- **AS-IS não é TO-BE.** Discovery descreve o presente; Spec Kit projeta a mudança.
- **Knowledge first.** O índice e os artefatos persistidos vêm antes do source.
- **Source access precisa de motivo.** Código só é aberto para fechar gaps concretos.
- **Evidência > confiança verbal.** Fato, inferência e unknown são separados.
- **Progressive disclosure.** Monorepo grande não deve ser aprofundado inteiro por padrão.
- **Uma fonte de verdade por responsabilidade.** A V2 não cria um segundo `SPEC/PLAN/TASKS`.
- **Compatibilidade histórica.** Scripts continuam reconhecendo artefatos V1 existentes.
- **Interatividade objetiva.** Skills confirmam escopo e ambiguidades com o humano antes de expandir investigacoes custosas.

## Arquivamento de artefatos da skill

Para reduzir poluicao local sem tocar artefatos do projeto, use:

```bash
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive
python .github/skill-contracts/scripts/archive_skill_artifacts.py --root . --mode archive-and-clean
```

O comando arquiva somente dados gerados pela skill.

## Workflow V1 arquivado

As skills abaixo foram movidas para `legacy-workflow/skills/`:

- `coordinate-fix`;
- `execute-fix-plan`;
- `run-solution-regression`.

Elas foram preservadas, não apagadas. Veja `MIGRATION-V2.md`.


## Git workflow V2.1

A skill `prepare-feature-branch` restaura o gate Git do workflow original sem reativar `execute-fix-plan`. Ela cria `feature/mmYYYY/descricao-curta` exclusivamente a partir de `main` atualizada por `git pull --ff-only origin main`, bloqueando em worktree sujo, divergência ou branch existente.
