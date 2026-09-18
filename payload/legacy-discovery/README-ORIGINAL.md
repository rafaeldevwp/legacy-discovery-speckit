# Legacy Discovery + Spec Kit — Guia para começar do zero

> Um guia simples para usar **GitHub Copilot + Agent Skills + Persistent Knowledge + Spec Kit** em um sistema legado grande, sem pedir para a IA redescobrir o repositório inteiro a cada mudança.

---

## 1. O que é este pacote?

Este pacote adiciona ao seu repositório uma camada de **Discovery para sistemas legados**.

A ideia é separar duas responsabilidades:

```text
DISCOVERY DO LEGADO                         SPEC KIT
"Como o sistema funciona hoje?"            "O que vamos mudar?"

        AS-IS                                  TO-BE
          │                                      │
          ▼                                      ▼
Persistent Knowledge                     Spec / Plan / Tasks
          │                                      │
          └──────────► HANDOFF ──────────────────┘
```

Em linguagem simples:

- as **Skills de Discovery** estudam o sistema atual;
- o conhecimento descoberto é salvo no próprio repositório;
- antes de uma nova mudança, a IA tenta **reutilizar o que já sabe**;
- se faltar informação, ela investiga apenas o necessário;
- depois gera um **HANDOFF**;
- o **Spec Kit** recebe esse HANDOFF e conduz a especificação e a implementação da mudança.

O objetivo é evitar este comportamento:

```text
Nova tarefa
   ↓
IA abre dezenas de arquivos
   ↓
redescobre o sistema
   ↓
gasta contexto/tokens
   ↓
começa a implementar
```

E substituir por:

```text
Nova tarefa
   ↓
consulta conhecimento existente
   ↓
conhecimento suficiente?
   ├─ SIM → reutiliza
   └─ NÃO → investiga somente o gap
   ↓
HANDOFF
   ↓
Spec Kit
```

---

# 2. O que você precisa instalar

Para o cenário deste guia, vamos considerar **GitHub Copilot no VS Code**.

Você precisa de:

1. **Git**
2. **Visual Studio Code**
3. **GitHub Copilot** funcionando no VS Code
4. **Python 3.11 ou superior**
5. **uv** (gerenciador usado/recomendado pelo Spec Kit)
6. **Spec Kit / Specify CLI**
7. As **Legacy Discovery Skills** deste pacote

> O Spec Kit suporta Windows diretamente. Não é obrigatório usar WSL.

---

# 3. Antes de instalar: proteja seu repositório

O Spec Kit será inicializado dentro de um repositório que já possui código.

Por isso, antes de qualquer instalação:

```bash
git status
```

Se houver alterações importantes ainda não salvas, faça **commit** ou **stash**.

Exemplo:

```bash
git add .
git commit -m "chore: baseline antes de instalar Spec Kit"
```

Isso é importante porque depois você poderá revisar exatamente quais arquivos foram adicionados pela instalação.

---

# 4. Instalar o `uv`

Primeiro verifique se já está instalado:

```bash
uv --version
```

Se aparecer uma versão, pule para a próxima etapa.

## Windows — opção simples com WinGet

Abra PowerShell:

```powershell
winget install --id=astral-sh.uv -e
```

Depois feche e abra novamente o terminal.

Teste:

```powershell
uv --version
```

## Windows — instalador PowerShell

Alternativamente:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Depois abra um terminal novo e execute:

```powershell
uv --version
```

---

# 5. Instalar o Spec Kit

A maneira mais simples para uso diário é instalar o pacote oficial `specify-cli`:

```bash
uv tool install specify-cli
```

Verifique:

```bash
specify version
```

Se o comando mostrar a versão do Spec Kit, a instalação funcionou.

Você pode também verificar o ambiente:

```bash
specify check
```

---

# 6. Inicializar o Spec Kit no seu legado

Entre na **raiz do repositório**.

Exemplo:

```powershell
cd C:\Projetos\MeuSistemaLegado
```

Confirme que está no lugar correto:

```bash
git status
```

Agora inicialize o Spec Kit usando GitHub Copilot:

```bash
specify init --here --force --integration copilot
```

### O que significam essas opções?

- `--here`: instalar no diretório atual;
- `--force`: permite instalar em uma pasta que já contém arquivos;
- `--integration copilot`: cria a integração para GitHub Copilot.

> `--force` não significa "apagar o seu projeto". Mesmo assim, em projeto existente, trabalhe sempre a partir de um commit/stash e revise o diff depois da inicialização.

Depois execute:

```bash
git status
```

Revise os arquivos criados antes de continuar.

---

# 7. Instalar as Legacy Discovery Skills

Descompacte o ZIP da V2 em uma pasta temporária.

Você verá principalmente:

```text
skills/
skill-contracts/
legacy-workflow/
```

Copie **somente**:

```text
skills/          → .github/skills/
skill-contracts/ → .github/skill-contracts/
```

O resultado deve ficar aproximadamente assim:

```text
SEU-REPOSITORIO/
│
├── .github/
│   ├── skills/
│   │   ├── analyze-legacy-solution/
│   │   │   └── SKILL.md
│   │   ├── investigate-legacy-bug/
│   │   │   └── SKILL.md
│   │   ├── analyze-change-impact/
│   │   │   └── SKILL.md
│   │   └── prepare-speckit-context/
│   │       └── SKILL.md
│   │
│   └── skill-contracts/
│       └── ...
│
├── .specify/
├── specs/
└── seu código...
```

### Não copie o `legacy-workflow` para `.github/skills`

A pasta:

```text
legacy-workflow/
```

existe apenas para preservar o workflow antigo da V1.

Se você está adotando o Spec Kit como fonte de verdade, **não coloque essas skills antigas na pasta ativa `.github/skills/`**.

---

# 8. Se você já utilizava a V1

Preserve sua base existente:

```text
.github/copilot-knowledge/
```

Não apague seus:

- `INDEX.md`;
- `SOLUTION-OVERVIEW.md`;
- projetos documentados;
- deep-dives;
- ADRs;
- investigações;
- análises de impacto;
- artefatos históricos da V1.

Remova da pasta ativa `.github/skills/`, se ainda existirem:

```text
coordinate-fix/
execute-fix-plan/
run-solution-regression/
```

Essas três skills pertencem ao workflow antigo e gerariam uma segunda sequência de SPEC/DESIGN/TASKS concorrendo com o Spec Kit.

---

# 9. Como saber se o Copilot reconheceu as Skills?

No VS Code, Agent Skills de projeto são descobertas a partir de:

```text
.github/skills/<nome-da-skill>/SKILL.md
```

O nome do arquivo precisa ser exatamente:

```text
SKILL.md
```

Depois de copiar as skills:

1. abra a **raiz do repositório** no VS Code;
2. abra o Copilot Chat;
3. utilize **Agent Mode**;
4. se necessário, recarregue/reabra o VS Code;
5. no VS Code atual, você também pode usar `/skills` para acessar a configuração de Skills.

Para testar, envie:

```text
Use a skill analyze-legacy-solution e me diga qual é a responsabilidade dela.
Não investigue o código ainda.
```

Se o Copilot reconhecer a skill, a instalação está correta.

---

# 9.1. Criar a Constitution do projeto (recomendado)

Antes da primeira feature, defina as regras que o Spec Kit não pode ignorar.

No Copilot Chat:

```text
/speckit.constitution

Este é um sistema legado. Defina princípios de trabalho que incluam:
- preservar compatibilidade e contratos existentes;
- não modernizar ou trocar tecnologia sem justificativa explícita;
- respeitar padrões arquiteturais existentes quando ainda forem válidos;
- exigir rastreabilidade entre requisito, plano, tarefa e implementação;
- considerar regressão e consumidores existentes;
- tratar o HANDOFF de Discovery como contexto AS-IS, não como decisão TO-BE;
- não tratar inferência como fato.
```

A Constitution funciona como um conjunto de **regras do projeto** que os demais comandos do Spec Kit devem respeitar.

Revise o arquivo gerado antes de seguir.

---

# 10. Primeiro uso em um sistema legado grande

Você **não precisa pedir para a IA estudar profundamente o repositório inteiro**.

Comece pelo mapa estrutural.

No Copilot Chat em Agent Mode, envie:

```text
Use a skill analyze-legacy-solution para iniciar o conhecimento deste repositório legado.

Faça discovery progressivo.
Comece pela estrutura da solution/repositório, projetos, responsabilidades,
dependências, integrações e arquivos-âncora.

Persista o conhecimento em .github/copilot-knowledge.

Não proponha modernização.
Não implemente código.
Não tente aprofundar todos os projetos de uma vez.
```

A partir daí deverá começar a surgir:

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

Essa pasta é a **memória técnica persistente do legado**.

---

# 11. Como usar no dia a dia

Esta é a parte mais importante.

Para uma nova feature ou alteração, **não comece pedindo implementação**.

Use primeiro:

```text
prepare-speckit-context
```

## Exemplo

Imagine esta necessidade:

> Alterar a consulta de veículos para tratar timeout da API externa sem perder o último estado conhecido.

Envie ao Copilot:

```text
Use a skill prepare-speckit-context para esta mudança:

Alterar a consulta de veículos para tratar timeout da API externa
sem perder o último estado conhecido.

Reutilize primeiro o Persistent Knowledge existente.
Abra source somente para gaps relevantes.
Não proponha solução TO-BE.
Não implemente código.
Gere o SPECKIT_HANDOFF.
```

---

# 12. O que `prepare-speckit-context` fará?

Primeiro ela lê o conhecimento existente.

Ela avalia dimensões como:

```text
STRUCTURE
CURRENT_BEHAVIOR
BUSINESS_RULES
DEPENDENCIES
IMPACT_SURFACE
EXTERNAL_BOUNDARIES
TEST_SAFETY_NET
```

Cada dimensão recebe um status:

```text
COVERED         já sabemos o suficiente
PARTIAL         sabemos uma parte
UNKNOWN         ainda não sabemos
STALE           informação pode estar desatualizada
NOT_APPLICABLE  não importa para esta mudança
```

## Se já houver conhecimento suficiente

```text
Knowledge
    ↓
COVERED
    ↓
NÃO abre source novamente
    ↓
HANDOFF
```

## Se faltar conhecimento

```text
Knowledge
    ↓
PARTIAL / UNKNOWN / STALE
    ↓
investiga somente o gap
    ↓
atualiza contexto necessário
    ↓
HANDOFF
```

Por padrão, a investigação incremental possui limites para evitar exploração infinita:

- até 3 rodadas de expansão;
- até 12 arquivos de source;
- até 4 expansões de busca após o preflight.

Se a evidência ainda não for suficiente, a skill registra o ponto como desconhecido em vez de inventar uma resposta.

---

# 13. O que é o HANDOFF?

O HANDOFF é a ponte entre o legado e o Spec Kit.

Exemplo:

```text
.github/copilot-knowledge/handoffs/
└── HANDOFF-0007-timeout-consulta-veiculos.md
```

Ele contém informações como:

```text
Pedido da mudança
Comportamento atual
Regras existentes
Dependências
Superfície de impacto
Limites externos
Evidências
Unknowns
Restrições de compatibilidade
```

Ele **não deve decidir a solução futura**.

Por exemplo, isto é correto:

```text
O VehicleService atualmente chama a API externa e mantém o último estado em memória.
```

Isto não pertence ao Discovery:

```text
Devemos criar um Circuit Breaker usando biblioteca X e extrair um novo adapter.
```

A segunda decisão pertence ao **Spec Kit / Plan**.

---

# 14. Depois do HANDOFF: usar o Spec Kit

Se o Discovery retornar:

```text
READY_FOR_SPECKIT
```

comece a especificação.

Exemplo:

```text
/speckit.specify

Quero alterar a consulta de veículos para tratar timeout da API externa
sem perder o último estado conhecido.

Antes de escrever a especificação, leia:
.github/copilot-knowledge/handoffs/HANDOFF-0007-timeout-consulta-veiculos.md

Trate Current Behavior, Compatibility Constraints, Impact Surface,
External Boundaries e Evidence como contexto factual AS-IS.

Não transforme automaticamente a arquitetura atual em solução futura.
```

Depois siga o fluxo:

```text
/speckit.specify
        ↓
/speckit.clarify
        ↓
/speckit.plan
        ↓
/speckit.checklist   (opcional, mas útil em mudanças críticas)
        ↓
/speckit.tasks
        ↓
/speckit.analyze
        ↓
/speckit.implement
        ↓
/speckit.converge
```

---

# 15. O que cada comando do Spec Kit significa?

## `/speckit.specify`

Define **o que precisa mudar** e quais comportamentos/requisitos são esperados.

Pergunta principal:

> O que queremos construir ou alterar?

---

## `/speckit.clarify`

Procura ambiguidades, lacunas ou decisões de requisito ainda não claras.

Pergunta principal:

> Existe algo importante que ainda não está claro?

---

## `/speckit.plan`

Cria o plano técnico da mudança.

É aqui que decisões de arquitetura futura podem aparecer.

Pergunta principal:

> Como vamos implementar isso tecnicamente?

---

## `/speckit.checklist` — opcional

Gera uma lista de verificação de qualidade para avaliar se os requisitos estão claros e completos antes de transformar o plano em tarefas.

É particularmente útil em mudanças críticas ou com muitas regras de negócio.

---

## `/speckit.tasks`

Quebra o plano em tarefas executáveis.

Pergunta principal:

> Quais passos precisam ser executados?

---

## `/speckit.analyze`

Verifica a consistência entre especificação, plano e tarefas antes da implementação.

Pergunta principal:

> Os artefatos concordam entre si?

---

## `/speckit.implement`

Executa as tarefas e modifica o código.

É **somente aqui** que a implementação deve começar no fluxo normal.

---

## `/speckit.converge`

Ajuda a verificar a convergência da implementação e dos artefatos após a execução, quando disponível no workflow instalado.

---

# 16. Fluxo diário resumido

Para **feature ou mudança de comportamento**:

```text
USER STORY
    ↓
prepare-speckit-context
    ↓
HANDOFF
    ↓
/speckit.specify
    ↓
/speckit.clarify
    ↓
/speckit.plan
    ↓
/speckit.tasks
    ↓
/speckit.analyze
    ↓
/speckit.implement
    ↓
/speckit.converge
```

Na prática, você precisa lembrar principalmente desta regra:

> **Antes de mudar o legado, prepare o contexto AS-IS. Depois deixe o Spec Kit conduzir o TO-BE.**

---

# 17. E quando eu só quero entender alguma coisa?

Não precisa usar Spec Kit.

Exemplo:

> Quem chama a API da prefeitura e o que acontece antes e depois?

Use:

```text
Use a skill analyze-legacy-solution.

Primeiro consulte .github/copilot-knowledge/INDEX.md e o conhecimento relacionado.

Quero descobrir quem chama a API da prefeitura, quem inicia esse fluxo
e o que acontece imediatamente antes e depois da chamada.

Abra source apenas se o conhecimento persistido não for suficiente.
Não implemente nada.
```

Fluxo:

```text
PERGUNTA
   ↓
Persistent Knowledge
   ↓
já sabemos?
 ├─ SIM → responde usando conhecimento
 └─ NÃO → discovery incremental
```

---

# 18. E quando existe um bug?

Para um bug difícil no legado, use primeiro:

```text
Use a skill investigate-legacy-bug para investigar este problema:

[descreva o bug]

Primeiro reutilize o Persistent Knowledge.
Investigue evidências e hipóteses.
Não corrija o source ainda.
```

Se precisar descobrir o raio de impacto:

```text
Use a skill analyze-change-impact para analisar o impacto de corrigir este comportamento.
```

Depois, se a correção exigir especificação/mudança relevante:

```text
investigate-legacy-bug
        ↓
analyze-change-impact
        ↓
prepare-speckit-context
        ↓
Spec Kit
```

---

# 19. Quando usar cada Skill?

| Eu quero... | Use |
|---|---|
| Entender uma área desconhecida do legado | `analyze-legacy-solution` |
| Investigar um bug sem sair corrigindo | `investigate-legacy-bug` |
| Saber o que pode quebrar com uma mudança | `analyze-change-impact` |
| Começar uma nova mudança/feature com Spec Kit | `prepare-speckit-context` |
| Criar requisitos | `/speckit.specify` |
| Resolver ambiguidades | `/speckit.clarify` |
| Definir a solução técnica | `/speckit.plan` |
| Criar tarefas | `/speckit.tasks` |
| Validar SPEC/PLAN/TASKS | `/speckit.analyze` |
| Alterar o código | `/speckit.implement` |

---

# 20. Três regras para não se perder

## Regra 1 — Quero entender

```text
DISCOVERY
```

Use as Legacy Discovery Skills.

---

## Regra 2 — Quero mudar

```text
prepare-speckit-context
        ↓
Spec Kit
```

---

## Regra 3 — Não deixe os dois lados decidirem a mesma coisa

```text
Discovery = AS-IS
Spec Kit  = TO-BE
```

Não permita que Discovery crie outra `SPEC`, `DESIGN` ou `TASKS` paralela ao Spec Kit.

---

# 21. Prompt pronto — nova User Story

Copie e cole:

```text
Use a skill prepare-speckit-context para esta User Story:

[COLE A USER STORY AQUI]

Regras:
1. faça Knowledge Preflight antes de acessar source;
2. reutilize primeiro .github/copilot-knowledge;
3. investigue somente gaps relevantes;
4. não proponha arquitetura ou solução TO-BE;
5. não implemente código;
6. gere um SPECKIT_HANDOFF;
7. informe se o status ficou READY_FOR_SPECKIT, PARTIAL ou BLOCKED;
8. se estiver READY_FOR_SPECKIT, mostre o próximo comando recomendado do Spec Kit.
```

---

# 22. Prompt pronto — entender o legado

```text
Use a skill analyze-legacy-solution para responder esta pergunta sobre o legado:

[COLE A PERGUNTA AQUI]

Antes de acessar o código, consulte o Persistent Knowledge existente.
Se o conhecimento já for suficiente, não reabra o source.
Se houver gap, investigue apenas o necessário.
Não proponha mudança e não implemente nada.
```

---

# 23. Prompt pronto — investigar bug

```text
Use a skill investigate-legacy-bug para investigar:

[DESCREVA O BUG]

Reutilize primeiro o Persistent Knowledge.
Separe fatos, evidências, hipóteses e unknowns.
Não corrija o código durante a investigação.
```

---

# 24. Prompt pronto — analisar impacto

```text
Use a skill analyze-change-impact para avaliar o impacto desta mudança:

[DESCREVA A MUDANÇA]

Mapeie consumidores, dependências, contratos, integrações,
riscos de regressão e áreas potencialmente afetadas.
Reutilize o Persistent Knowledge antes de abrir source.
Não implemente nada.
```

---

# 25. Validar os artefatos do Discovery

O pacote inclui scripts auxiliares.

Na raiz do repositório:

```bash
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
```

Para sincronizar o índice:

```bash
python .github/skill-contracts/scripts/sync_index.py --root .github/copilot-knowledge
```

Depois valide novamente:

```bash
python .github/skill-contracts/scripts/validate_artifacts.py --root .github/copilot-knowledge
```

---

# 26. Estrutura final esperada

Depois que tudo estiver funcionando, o repositório tende a ficar assim:

```text
meu-legado/
│
├── .github/
│   ├── skills/
│   │   ├── analyze-legacy-solution/
│   │   ├── investigate-legacy-bug/
│   │   ├── analyze-change-impact/
│   │   └── prepare-speckit-context/
│   │
│   ├── skill-contracts/
│   │   └── scripts/
│   │
│   └── copilot-knowledge/
│       ├── INDEX.md
│       ├── SOLUTION-OVERVIEW.md
│       ├── projects/
│       ├── decisions/
│       ├── deep-dives/
│       ├── investigations/
│       ├── impact-analyses/
│       └── handoffs/
│
├── .specify/
│   ├── memory/
│   ├── scripts/
│   └── templates/
│
├── specs/
│   └── ...
│
└── código da aplicação...
```

---

# 27. Preciso executar `specify init` todos os dias?

**Não.**

Normalmente você executa:

```bash
specify init --here --force --integration copilot
```

uma vez para inicializar o projeto.

Depois, no dia a dia, você trabalha principalmente no Copilot Chat usando as Skills e os comandos `/speckit.*` gerados no projeto.

Para verificar a instalação da CLI:

```bash
specify version
specify check
```

---

# 28. Atualizar o Spec Kit

Consulte primeiro:

```bash
specify self check
```

Se você instalou via `uv tool install specify-cli`, a documentação oficial recomenda atualizar usando o mesmo gerenciador de instalação.

Para atualizar a integração do projeto, quando necessário:

```bash
specify integration upgrade copilot
```

Sempre revise mudanças geradas em infraestrutura antes de fazer commit.

---

# 29. Problemas comuns

## `uv` não é reconhecido

Feche o terminal e abra novamente.

Teste:

```bash
uv --version
```

Se continuar sem funcionar, reinstale o `uv` e confira se ele foi adicionado ao `PATH`.

---

## `specify` não é reconhecido

Teste:

```bash
uv tool list
```

Depois:

```bash
specify version
```

Se necessário, reinstale:

```bash
uv tool install --force specify-cli
```

---

## Copilot não reconhece minhas Skills

Confira se o caminho é exatamente:

```text
.github/skills/<nome-da-skill>/SKILL.md
```

Exemplo:

```text
.github/skills/prepare-speckit-context/SKILL.md
```

Depois:

1. confirme que abriu a raiz correta do repositório no VS Code;
2. use Agent Mode;
3. recarregue/reabra o VS Code;
4. abra `/skills` e confira as skills reconhecidas, quando disponível na sua versão.

---

## Copilot começa a implementar durante Discovery

Interrompa e reforce:

```text
Estamos em Discovery AS-IS.
Não implemente código.
Não proponha TO-BE.
Siga a skill selecionada e termine no HANDOFF.
```

---

## A IA quer abrir o código novamente mesmo com documentação existente

Use:

```text
Faça Knowledge Preflight primeiro.
Acesse source somente se existir um gap explícito PARTIAL, UNKNOWN ou STALE.
Não revalide código por curiosidade.
```

---

# 30. Checklist de instalação

Marque conforme concluir:

```text
[ ] Git funcionando
[ ] VS Code instalado
[ ] GitHub Copilot funcionando em Agent Mode
[ ] Python 3.11+ instalado
[ ] uv instalado
[ ] specify-cli instalado
[ ] `specify version` funcionando
[ ] commit/stash feito antes de alterar o legado
[ ] Spec Kit inicializado no repositório
[ ] `.github/skills/` contendo as 4 skills V2
[ ] `.github/skill-contracts/` copiado
[ ] workflow V1 não está ativo em `.github/skills/`
[ ] Copilot reconhece `prepare-speckit-context`
[ ] primeiro Discovery executado
[ ] `.github/copilot-knowledge/INDEX.md` criado/preservado
[ ] primeira User Story gerou um HANDOFF
[ ] HANDOFF foi usado por `/speckit.specify`
```

---

# 31. Resumo em 30 segundos

## Instalação

```text
Instalar uv
   ↓
Instalar specify-cli
   ↓
Commit/stash do legado
   ↓
specify init --here --force --integration copilot
   ↓
Copiar as 4 skills para .github/skills
   ↓
Copiar skill-contracts para .github/skill-contracts
```

## Trabalho diário

```text
NOVA MUDANÇA
    ↓
prepare-speckit-context
    ↓
HANDOFF
    ↓
/speckit.specify
    ↓
/speckit.clarify
    ↓
/speckit.plan
    ↓
/speckit.tasks
    ↓
/speckit.analyze
    ↓
/speckit.implement
```

## Regra principal

> **Discovery explica o sistema que existe. Spec Kit governa o sistema que queremos mudar.**

---

# Referências oficiais

- Spec Kit: https://github.com/github/spec-kit
- Instalação do Spec Kit: https://github.com/github/spec-kit/blob/main/docs/installation.md
- Spec Kit em projetos existentes: https://github.com/github/spec-kit/blob/main/docs/guides/existing-projects.md
- GitHub Copilot Agent Skills: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- VS Code Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills
- Instalação do uv: https://github.github.com/spec-kit/install/uv.html
