# Changelog V2

## Added

- `prepare-speckit-context` skill.
- `SPECKIT_HANDOFF` artifact and `handoffs/` knowledge group.
- Knowledge Coverage matrix: structure, current behavior, business rules, dependencies, impact, external boundaries and tests.
- Coverage states: `COVERED`, `PARTIAL`, `UNKNOWN`, `STALE`, `NOT_APPLICABLE`.
- Bounded source-access policy and default discovery budget.
- Spec Kit integration reference for core SDD and official bug extension.
- `HANDOFF` support in `next_id.py`, `validate_artifacts.py` and `sync_index.py`.
- Migration and installation guides.

## Changed

- `analyze-legacy-solution` is explicitly AS-IS only.
- Reuse is now based on sufficiency/coverage, not just existence of `INDEX.md`.
- `.csproj` modification time is treated only as a structural staleness signal, not proof that business behavior is current.
- `investigate-legacy-bug` and `analyze-change-impact` hand off planned changes through `prepare-speckit-context`.
- Shared ownership/handoff/lifecycle contracts now reserve `.specify/` artifacts to Spec Kit.

## Archived from active discovery

- `coordinate-fix`.
- `execute-fix-plan`.
- `run-solution-regression`.

Their files remain under `legacy-workflow/` for history and rollback. V1 artifact validation remains supported.


## 2.1 — Prepare Feature Branch

- adicionada skill `prepare-feature-branch`;
- restaurado padrão `feature/mmYYYY/descricao-curta`;
- branch nasce de `main` após `fetch` + `pull --ff-only`;
- worktree sujo, divergência e branch existente bloqueiam;
- proibidos stash/reset/merge/rebase/force/push automáticos;
- `prepare-speckit-context` agora recomenda branch antes de `/speckit.specify`.

## 2.2 — Governance hardening, local-only skill artifacts and archive command

- politica de versionamento refinada: artefatos gerados por skill ficam local-only por padrao;
- artefatos do Spec Kit (`.specify/` e `specs/`) permanecem sob politica normal de versionamento do time;
- fluxo de governanca Git mantido sob responsabilidade da skill `prepare-feature-branch`;
- adicionada configuracao automatica de `.git/info/exclude` para evitar stage acidental de artefatos de skill;
- novo comando `archive_skill_artifacts.py` para arquivar e opcionalmente limpar artefatos/metadados de skill sem tocar dados de codigo do repositorio;
- orientacoes reforcadas para `constitution` do Spec Kit respeitar o AS-IS real do projeto;
- orientacoes reforcadas para `plan` respeitar a arquitetura existente e enriquecer decisoes com evidencias do handoff;
- maior interatividade nas skills ativas com checkpoints de confirmacao para reduzir ambiguidades.

## 2.3 — PO técnico: refine-user-story (bundle 1.3.0)

- adicionada skill `refine-user-story`: analisa a história do PM contra o AS-IS e gera `STORY_REFINEMENT` (refinamento técnico / planejamento de execução);
- novo artefato `refinements/REFINEMENT-{NNNN}-{slug}.md`, owner único `refine-user-story`, status `READY_FOR_SPECKIT`, `AWAITING_HUMAN`, `BLOCKED`;
- escada de ambiguidades `STORY → KNOWLEDGE → CODE → HUMAN`; intenção de negócio sempre vai ao humano;
- `READY_FOR_SPECKIT` exige handoff pronto, nenhuma pergunta bloqueante aberta, revisão humana registrada e rastreabilidade AC/GR/SLICE — verificado por `validate_artifacts.py` (`refinement_rules.py`);
- `next_id.py --type REFINEMENT`; `sync_index.py` agrupa refinamentos após os handoffs;
- novos códigos em `failure-policy.md`: `HANDOFF_MISSING`, `HUMAN_DECISION_REQUIRED`, `STORY_CONFLICTS_WITH_AS_IS`;
- instalador cria `copilot-knowledge/refinements/` e faz backup de `.github/skills/refine-user-story`;
- **comandos `/legacy.*`** para todas as skills (prompt files em `.github/prompts/`), no mesmo espírito dos `/speckit.*`: `help`, `story`, `analyze`, `bug`, `impact`, `handoff`, `refine`, `answer`, `approve`, `branch`, `status`, `validate`, `archive`;
- `/legacy.story` encadeia handoff → refinamento e para em cada decisão humana; `/legacy.approve` é o único caminho de aprovação humana e desfaz a aprovação se o validador recusar;
- novo script somente-leitura `story_status.py` (estado das histórias e próximo comando);
- instalador grava apenas `legacy.*.prompt.md` e registra os comandos em `installation.json`; outros prompts não são tocados;
- **sem regressão**: as 5 skills anteriores e o workflow V1 não foram alterados; sem refinamentos, os scripts produzem saída idêntica à V2.2 — provado pela suíte `tests/` do pacote;
- `SHA256SUMS.txt` regenerado (o da V2.2 estava desatualizado em 27 arquivos); pastas `backups/` e `__pycache__/` removidas do pacote distribuído.

## 2.4 — Fechadura, lacre, fiscal e termômetro (bundle 1.4.0)

- **fechadura**: agente `legacy-discovery` com hook `PreToolUse` (`legacy_governance.py`, protocolo do AgentQA, falha fechada). Nega escrita fora das trilhas das skills, escrita em Spec Kit/skills/contratos/hook/agente/comandos/INDEX, gravação de aprovação pelo agente, `approve_refinement.py`, `archive-and-clean`, Git destrutivo/publicação, escrita por terminal em trilhas protegidas e execução codificada. Leitura, busca, build, testes e scripts de contrato seguem livres;
- **lacre**: novo status `READY_FOR_REVIEW`; aprovação só por `approve_refinement.py`, executado pelo humano, que grava `reviewed_by`, `reviewed_at` e `approval_digest` (SHA-256). Edição posterior invalida a aprovação. Corrige lacuna da V2.3: refinamento sem perguntas e ainda não aprovado não tinha status válido;
- **fiscal**: `validate_artifacts.py` confere `arquivo:linha`, `EXISTING_TEST:arquivo::Teste` e IDs de artefatos citados (erro em refinamentos, `WARNING` em handoffs);
- **termômetro**: `tools/build_release.py` (higiene, checksums, zip em ordem fixa e `--verify-zip`) e workflow de CI (Windows/Linux, Python 3.11/3.13);
- **sem regressão**: as 5 skills da V2.2 e o workflow V1 seguem byte a byte; sem refinamentos, os scripts dão saída idêntica à V2.2; refinamentos aprovados na V2.3 continuam válidos (com aviso). 106 testes.
