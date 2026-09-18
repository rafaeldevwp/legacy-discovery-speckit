# Legacy Discovery + Spec Kit

> **Um jeito seguro de trabalhar com IA em sistemas legados sem sair alterando código no escuro.**

Este projeto combina duas coisas:

* uma camada de **Discovery**, responsável por entender o sistema atual;
* o **GitHub Spec Kit**, responsável por organizar mudanças, especificações, planos, tarefas e implementação.

A ideia principal é muito simples:

```text
ENTENDER PRIMEIRO
       ↓
GUARDAR O QUE DESCOBRIU
       ↓
ESPECIFICAR A MUDANÇA
       ↓
PLANEJAR
       ↓
IMPLEMENTAR
```

---

# 1. Para quem é este projeto?

Este projeto é útil principalmente para quem trabalha com:

* sistemas legados;
* projetos grandes;
* código pouco documentado;
* muitas regras de negócio;
* integrações externas;
* manutenção de sistemas existentes;
* GitHub Copilot;
* desenvolvimento assistido por IA.

O objetivo é evitar um comportamento muito comum:

```text
Recebe uma demanda
        ↓
IA procura qualquer coisa no código
        ↓
abre vários arquivos
        ↓
faz suposições
        ↓
altera o código
        ↓
aparecem regressões
```

Com este projeto, o fluxo muda para:

```text
Recebe uma demanda
        ↓
consulta conhecimento existente
        ↓
investiga somente se faltar informação
        ↓
cria contexto confiável
        ↓
cria branch
        ↓
especifica
        ↓
planeja
        ↓
implementa
```

---

# 2. Se você não entende nada disso, comece aqui

Você não precisa decorar todos os nomes.

Pense apenas nestas situações.

```text
O QUE VOCÊ QUER FAZER?

├── Quero entender uma parte do sistema
│
│      use:
│      analyze-legacy-solution
│
├── Tenho uma pergunta sobre o sistema
│
│      use:
│      Persistent Knowledge primeiro
│
├── Recebi uma User Story
│
│      use:
│      prepare-speckit-context
│          ↓
│      prepare-feature-branch
│          ↓
│      Spec Kit
│
├── Encontrei um bug
│
│      use:
│      investigate-legacy-bug
│
├── Já descobri onde está o bug
│
│      use:
│      prepare-speckit-context
│          ↓
│      prepare-feature-branch
│          ↓
│      Spec Kit
│
└── Quero saber o que uma mudança pode quebrar

       use:
       analyze-change-impact
```

---

# 3. Regra principal

Existe uma divisão muito importante.

## Discovery

Discovery responde:

> **Como o sistema funciona hoje?**

É o chamado:

```text
AS-IS
```

Discovery pode descobrir:

* classes;
* métodos;
* fluxos;
* chamadas;
* regras;
* integrações;
* dependências;
* comportamento atual;
* riscos;
* evidências;
* pontos ainda desconhecidos.

Discovery não deve decidir a solução futura.

---

## Spec Kit

Spec Kit responde:

> **Como o sistema deverá funcionar depois da mudança?**

Depois disso, ele ajuda a definir:

```text
SPEC
 ↓
PLAN
 ↓
TASKS
 ↓
IMPLEMENTAÇÃO
```

Isso é o:

```text
TO-BE
```

---

# 4. A frase mais importante deste projeto

```text
Discovery descobre fatos.

Spec Kit governa mudanças.
```

---

# 5. O que está instalado?

Depois da instalação, você terá estas Skills:

```text
.github/
└── skills/
    ├── analyze-legacy-solution/
    ├── investigate-legacy-bug/
    ├── analyze-change-impact/
    ├── prepare-speckit-context/
    └── prepare-feature-branch/
```

Cada uma possui uma responsabilidade.

---

# 6. O que cada Skill faz?

## analyze-legacy-solution

Use quando quiser entender o sistema ou uma parte dele.

Exemplos:

```text
Como funciona a atualização de veículos?
```

```text
Quero entender o módulo de pagamento.
```

```text
Quero mapear a integração com a PBH.
```

---

## investigate-legacy-bug

Use quando existe um problema e você ainda não sabe exatamente a causa.

Exemplo:

```text
Quando a API da PBH demora, o Worker para de atualizar.
```

A Skill tenta descobrir:

* onde está o problema;
* qual fluxo participa;
* qual comportamento atual provoca o erro;
* quais evidências comprovam isso.

Ela não deve corrigir o código durante a investigação.

---

## analyze-change-impact

Use quando quiser saber:

> Se eu mudar isso, o que mais pode ser afetado?

Exemplo:

```text
Se eu alterar VehicleService,
quais componentes podem sofrer impacto?
```

---

## prepare-speckit-context

Use antes de começar uma mudança importante.

Ela prepara o contexto do sistema atual para o Spec Kit.

Ela responde:

```text
O que precisamos saber sobre o sistema atual
antes de especificar esta mudança?
```

---

## prepare-feature-branch

Use depois que o contexto estiver pronto.

Ela prepara uma branch segura a partir da `main`.

Padrão:

```text
feature/mmYYYY/descricao
```

Exemplo:

```text
feature/082026/tratar-timeout-pbh
```

---

# 7. O que é Persistent Knowledge?

É a memória técnica do projeto.

Fica em:

```text
.github/copilot-knowledge/
```

Exemplo:

```text
.github/copilot-knowledge/
├── INDEX.md
├── projects/
├── decisions/
├── deep-dives/
├── investigations/
├── impact-analyses/
└── handoffs/
```

A ideia é simples:

```text
IA descobre algo importante
        ↓
guarda
        ↓
outra demanda aparece
        ↓
reutiliza
```

Em vez de:

```text
IA descobre
        ↓
esquece
        ↓
descobre tudo novamente
```

---

# 8. O que significa COVERED?

Imagine que você pergunta:

> Quem chama a API da PBH?

Se isso já foi investigado e existe evidência suficiente:

```text
COVERED
```

Nesse caso:

```text
não precisa abrir o código novamente
```

---

# 9. Outros estados

O conhecimento pode estar em diferentes estados.

## COVERED

Já sabemos o suficiente.

```text
Não investigar novamente.
```

---

## PARTIAL

Sabemos uma parte, mas ainda existem gaps.

```text
Investigar somente o que está faltando.
```

---

## UNKNOWN

Ainda não temos informação suficiente.

```text
Discovery necessário.
```

---

## STALE

Existe conhecimento, mas ele pode estar desatualizado.

```text
Revalidar somente o necessário.
```

---

# 10. Primeira vez usando o projeto

Quando instalar em um sistema legado pela primeira vez, faça um Discovery inicial.

No GitHub Copilot Agent Mode:

```text
Use a skill analyze-legacy-solution.

Quero iniciar o conhecimento deste sistema legado.

Comece pela visão estrutural do repositório.

Identifique:

- projetos;
- responsabilidades principais;
- dependências;
- integrações externas;
- arquivos importantes;
- pontos de entrada.

Faça Discovery progressivo.

Não tente analisar profundamente todo o código.

Persista o conhecimento relevante em
.github/copilot-knowledge.

Não proponha mudanças ou arquitetura futura.
```

O objetivo inicial não é compreender 100% do sistema.

O objetivo é criar um mapa.

```text
REPOSITÓRIO
    ↓
PROJETOS
    ↓
COMPONENTES
    ↓
INTEGRAÇÕES
    ↓
PONTOS DE ENTRADA
```

---

# 11. Quero entender uma parte do sistema

Exemplo:

> Quero saber como funciona a atualização dos veículos.

Use:

```text
Use a skill analyze-legacy-solution.

Quero entender o fluxo de atualização dos veículos.

Consulte primeiro o Persistent Knowledge.

Se já existir conhecimento suficiente, reutilize.

Se faltar informação, investigue somente os gaps.

Quero saber:

- quem inicia o fluxo;
- quais componentes participam;
- quais chamadas são realizadas;
- quais integrações existem;
- quais regras aparecem no fluxo;
- quais evidências comprovam as conclusões.

Não proponha implementação futura.
```

Fluxo:

```text
PERGUNTA
   ↓
KNOWLEDGE
   ↓
já sabemos?
 /        \
sim        não
 │          │
responde   investiga gap
```

---

# 12. Só quero fazer uma pergunta

Nem toda pergunta precisa de Spec Kit.

Exemplo:

> Quem chama a PBH?

Você pode dizer:

```text
Consulte primeiro o Persistent Knowledge
e me diga quem chama a API da PBH.

Abra código-fonte somente se o conhecimento existente
não tiver evidência suficiente.
```

Não precisa executar:

```text
/specify
/plan
/tasks
```

Porque você não está pedindo uma mudança.

Você está pedindo conhecimento.

---

# 13. Recebi uma nova User Story

Imagine esta User Story:

> Como operador, quero visualizar a previsão de chegada do veículo.

Não comece dizendo:

```text
Implemente esta User Story.
```

Primeiro prepare o contexto.

---

# 14. Passo 1 da User Story — preparar contexto

Use:

```text
Use prepare-speckit-context para esta User Story:

Como operador,
quero visualizar a previsão de chegada do veículo
para conseguir informar o usuário.

Reutilize primeiro o Persistent Knowledge.

Investigue código somente se houver gaps relevantes.

Não proponha solução técnica.

Não implemente nada.

Gere o SPECKIT_HANDOFF.
```

A Skill irá verificar coisas como:

```text
CURRENT_BEHAVIOR
BUSINESS_RULES
DEPENDENCIES
IMPACT_SURFACE
EXTERNAL_BOUNDARIES
```

---

# 15. O que você quer receber?

Idealmente:

```text
READY_FOR_SPECKIT
```

Isso significa:

```text
sabemos o suficiente sobre o sistema atual
para começar a especificar a mudança
```

---

# 16. O que é HANDOFF?

O HANDOFF é um documento que entrega o conhecimento do sistema atual ao Spec Kit.

Exemplo:

```text
.github/copilot-knowledge/handoffs/
HANDOFF-0042-previsao-chegada.md
```

Pense nele assim:

```text
Discovery
    ↓
HANDOFF
    ↓
Spec Kit
```

O HANDOFF pode conter:

* comportamento atual;
* fluxos;
* componentes;
* dependências;
* restrições;
* integrações;
* impactos;
* evidências;
* unknowns.

Ele não deve decidir a solução futura.

---

# 17. Passo 2 da User Story — criar a branch

Depois de:

```text
READY_FOR_SPECKIT
```

peça:

```text
Use prepare-feature-branch para esta User Story.
```

A Skill fará:

```text
git fetch origin
        ↓
git switch main
        ↓
git pull --ff-only origin main
        ↓
cria branch
```

Exemplo:

```text
feature/082026/previsao-chegada
```

---

# 18. Segurança da branch

A Skill não deve executar automaticamente operações perigosas como:

```text
git stash
git merge
git rebase
git reset
git push --force
git branch -D
```

Se existir uma situação perigosa, ela deve parar.

Exemplos:

```text
WORKTREE_DIRTY
```

```text
MAIN_DIVERGED
```

```text
BRANCH_ALREADY_EXISTS
```

```text
ORIGIN_NOT_FOUND
```

---

# 19. Passo 3 da User Story — criar o SPEC

Agora começa o Spec Kit.

Use:

```text
/speckit.specify
```

Exemplo:

```text
/speckit.specify

Implementar a seguinte User Story:

Como operador,
quero visualizar a previsão de chegada do veículo
para conseguir informar o usuário.

Use como contexto AS-IS o HANDOFF gerado anteriormente.

Considere os fatos, restrições e evidências existentes.

Não transforme decisões atuais do legado
automaticamente em decisões da nova solução.
```

---

# 20. O que o SPEC deve responder?

O SPEC responde:

```text
O QUE o sistema deve fazer?
```

e:

```text
POR QUE isso precisa existir?
```

---

# 21. O SPEC não deveria decidir código

Errado:

```text
Adicionar método GetArrivalPrediction()
na classe VehicleService.
```

Isso já é solução técnica.

Certo:

```text
O operador deve conseguir visualizar
uma estimativa de chegada do veículo.
```

---

# 22. Depois do SPEC

O fluxo normal é:

```text
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

---

# 23. O que cada etapa significa?

## specify

Define:

```text
O QUE queremos?
```

---

## clarify

Resolve dúvidas importantes.

```text
O requisito está claro?
```

---

## plan

Define:

```text
COMO tecnicamente vamos fazer?
```

Aqui aparecem coisas como:

* classes;
* serviços;
* contratos;
* componentes;
* arquitetura;
* estratégia técnica.

---

## tasks

Transforma o plano em tarefas executáveis.

Exemplo:

```text
TASK-001
Criar contrato.

TASK-002
Alterar serviço.

TASK-003
Adicionar teste.

TASK-004
Atualizar endpoint.
```

---

## analyze

Verifica se:

```text
SPEC
PLAN
TASKS
```

estão coerentes entre si.

---

## implement

Agora sim:

```text
ALTERE O CÓDIGO
```

---

## converge

Depois da implementação verifica:

```text
ficou alguma coisa faltando?
```

---

# 24. Fluxo completo de uma User Story

```text
USER STORY
    ↓
prepare-speckit-context
    ↓
Persistent Knowledge
    ↓
Discovery somente para gaps
    ↓
HANDOFF
    ↓
READY_FOR_SPECKIT
    ↓
prepare-feature-branch
    ↓
feature/mmYYYY/descricao
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

---

# 25. Encontrei um BUG

Imagine:

> Quando a PBH demora para responder, o Worker para de atualizar.

Primeiro investigue.

Use:

```text
Use investigate-legacy-bug.

Bug:

Quando a PBH demora para responder,
a atualização de veículos é interrompida.

Consulte primeiro o Persistent Knowledge.

Investigue somente o necessário.

Quero descobrir:

- comportamento atual;
- fluxo afetado;
- causa provável;
- evidências;
- componentes envolvidos;
- impacto;
- unknowns.

Não altere código.
```

---

# 26. O que você espera descobrir?

Algo parecido com:

```text
BUG

Timeout durante consulta externa.

FLUXO

Worker
 ↓
VehicleService.UpdateAsync()
 ↓
DownloadFileAsync()
 ↓
TimeoutException
 ↓
ciclo interrompido

CAUSA

VehicleService.UpdateAsync()

EVIDENCE

VehicleService.cs
Worker.cs
```

---

# 27. Já descobri exatamente onde está o BUG

Esta situação é muito importante.

Imagine que você descobriu:

```text
O bug está em:

VehicleService.UpdateAsync()
```

Não peça:

```text
Faça um SPEC para alterar VehicleService.UpdateAsync().
```

Isso mistura problema com solução.

---

# 28. O que fazer quando já sabe o método com problema?

Primeiro:

```text
Use prepare-speckit-context para preparar
a correção deste bug.

Problema:

Quando ocorre timeout durante a consulta à PBH,
o ciclo de atualização dos veículos é interrompido.

A investigação já identificou como causa:

VehicleService.UpdateAsync()

Use a investigação existente e o Persistent Knowledge.

Não redescubra fatos já comprovados.

Identifique:

- comportamento atual;
- comportamento esperado;
- dependências;
- impacto;
- restrições;
- evidências;
- unknowns.

Não proponha solução técnica.

Gere o SPECKIT_HANDOFF.
```

---

# 29. Depois crie a branch

```text
Use prepare-feature-branch para esta correção.
```

Exemplo:

```text
feature/082026/tratar-timeout-pbh
```

---

# 30. Depois crie o SPEC do bug

Use:

```text
/speckit.specify
```

Mas descreva comportamento.

Exemplo:

```text
/speckit.specify

Corrigir o comportamento de atualização dos veículos
quando ocorrer uma falha temporária de comunicação
com a PBH.

Uma falha temporária não deve impedir
os próximos ciclos de atualização.

Use o HANDOFF desta investigação
como contexto AS-IS.
```

---

# 31. Exemplo errado de SPEC para bug

```text
Adicionar try/catch no método
VehicleService.UpdateAsync().
```

Por quê?

Porque você já está dizendo:

```text
COMO corrigir
```

Isso pertence ao PLAN.

---

# 32. Exemplo correto de SPEC para bug

```text
Quando uma falha temporária ocorrer durante
a consulta externa, o processo periódico
de atualização deve continuar operacional.

Uma falha em um ciclo não deve impedir
os ciclos posteriores.

A falha deve ser observável para diagnóstico.
```

Isso descreve:

```text
COMPORTAMENTO ESPERADO
```

---

# 33. Quando o método aparece?

No:

```text
/speckit.plan
```

Agora sim pode aparecer algo como:

```text
Componente:

VehicleService

Método:

UpdateAsync()

Abordagem:

- tratar falha temporária;
- preservar estado válido;
- garantir retorno do Worker;
- registrar erro;
- preservar comportamento de retry existente.
```

---

# 34. Regra fácil para BUG

Guarde isto:

```text
INVESTIGATION

ONDE está quebrando?
POR QUE está quebrando?


SPEC

COMO o sistema deveria se comportar?


PLAN

COMO tecnicamente vamos corrigir?


TASKS

O QUE exatamente será alterado?


IMPLEMENT

ALTERE O CÓDIGO.
```

---

# 35. Bug simples ou bug complexo?

Nem todo bug precisa obrigatoriamente do fluxo completo.

---

## Bug simples

Exemplo:

```text
if invertido
null não tratado
mapping incorreto
validação localizada
```

Fluxo possível:

```text
investigate-legacy-bug
        ↓
causa comprovada
        ↓
baixo impacto
        ↓
correção controlada
```

---

## Bug complexo

Se a correção exige:

* mudança de comportamento;
* mudança de contrato;
* nova regra;
* vários componentes;
* alteração arquitetural;
* refatoração importante;

use:

```text
investigate-legacy-bug
        ↓
analyze-change-impact
        ↓
prepare-speckit-context
        ↓
prepare-feature-branch
        ↓
Spec Kit
```

---

# 36. Quero saber o impacto de uma mudança

Imagine:

> Quero mudar a forma como o cache de veículos funciona.

Antes de implementar:

```text
Use analyze-change-impact.

Mudança pretendida:

Alterar o comportamento do cache de veículos.

Consulte primeiro o Persistent Knowledge.

Quero identificar:

- projetos afetados;
- classes;
- consumidores;
- integrações;
- contratos;
- riscos;
- possíveis regressões;
- evidências;
- unknowns.

Não implemente.
```

---

# 37. Resultado esperado de impacto

Algo semelhante a:

```text
MUDANÇA
   ↓
Vehicle Cache
   ↓
Impact Surface
   ├── VehicleService
   ├── Worker
   ├── API
   ├── Controller
   ├── consumers
   └── testes
```

---

# 38. O que são Evidências?

Uma conclusão importante deve ter alguma prova.

Exemplo:

```text
FATO

Worker chama VehicleService.UpdateAsync()

EVIDÊNCIA

Worker.cs
linha / método correspondente
```

Isso permite saber:

```text
de onde veio essa informação?
```

---

# 39. O que é UNKNOWN?

Às vezes não é possível comprovar alguma coisa.

Nesse caso, deve ser registrado:

```text
UNKNOWN
```

ou:

```text
UNK-001
```

É muito melhor dizer:

```text
não foi possível comprovar
```

do que inventar uma resposta.

---

# 40. Discovery não deve ser infinito

Não queremos isto:

```text
busca
 ↓
arquivo
 ↓
outra busca
 ↓
mais arquivo
 ↓
mais busca
 ↓
mais arquivo
 ↓
...
```

O Discovery possui limites.

Se não conseguir concluir:

```text
PARTIAL
+
UNKNOWNS
```

Isso é aceitável.

O princípio é:

```text
conhecimento suficiente
>
conhecimento perfeito
```

---

# 41. O que NÃO fazer

## Não faça isto com uma User Story

```text
Implemente esta US.
```

Sem antes entender o contexto.

---

## Não comece diretamente com

```text
/speckit.implement
```

em uma mudança importante de sistema legado.

---

## Não use Discovery para inventar arquitetura

Errado:

```text
Essa classe está grande,
então devemos criar Repository,
Strategy e Factory.
```

Discovery deveria dizer apenas:

```text
Esta classe atualmente possui estas responsabilidades...
```

A decisão sobre arquitetura fica no:

```text
/speckit.plan
```

---

# 42. Não reabra código por curiosidade

Se existe conhecimento:

```text
COVERED
```

com evidência suficiente:

```text
não abra os mesmos arquivos novamente
apenas para confirmar.
```

---

# 43. Fluxos rápidos

## Quero entender algo

```text
analyze-legacy-solution
```

---

## Quero fazer uma pergunta

```text
Persistent Knowledge primeiro
        ↓
source somente se faltar informação
```

---

## Recebi uma User Story

```text
prepare-speckit-context
        ↓
prepare-feature-branch
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

---

## Encontrei um bug

```text
investigate-legacy-bug
```

---

## Já sei onde está o bug

```text
prepare-speckit-context
        ↓
prepare-feature-branch
        ↓
/speckit.specify
```

---

## Quero saber o impacto

```text
analyze-change-impact
```

---

# 44. Tabela rápida

| Situação                             | Use                           |
| ------------------------------------ | ----------------------------- |
| Não sei como algo funciona           | `analyze-legacy-solution`     |
| Tenho uma pergunta                   | Persistent Knowledge primeiro |
| Recebi uma User Story                | `prepare-speckit-context`     |
| Encontrei um bug                     | `investigate-legacy-bug`      |
| Já encontrei a causa do bug          | `prepare-speckit-context`     |
| Quero saber o impacto                | `analyze-change-impact`       |
| Preciso criar a branch               | `prepare-feature-branch`      |
| Quero definir comportamento          | `/speckit.specify`            |
| Tenho ambiguidades                   | `/speckit.clarify`            |
| Quero definir a solução técnica      | `/speckit.plan`               |
| Quero gerar tarefas                  | `/speckit.tasks`              |
| Quero validar Spec/Plan/Tasks        | `/speckit.analyze`            |
| Quero programar                      | `/speckit.implement`          |
| Quero verificar o que ficou faltando | `/speckit.converge`           |

---

# 45. Instalação

## Pré-requisitos

Tenha instalado:

* Git;
* Visual Studio Code;
* GitHub Copilot;
* Python 3.11 ou superior;
* PowerShell no Windows.

---

# 46. Instalação no Windows

Descompacte o pacote.

Execute:

```text
INSTALAR-WINDOWS.bat
```

Informe o caminho do seu repositório.

Exemplo:

```text
C:\Projetos\SistemaLegado
```

---

# 47. Atualizando uma versão já instalada

Se você já tem uma versão anterior instalada, não precisa reinicializar o Spec Kit.

Use:

```powershell
.\install.ps1 `
  -TargetPath "C:\Projetos\SistemaLegado" `
  -SkipSpecKitInstall `
  -SkipSpecKitInit
```

---

# 48. Windows bloqueou o script

Se aparecer mensagem relacionada a assinatura digital:

```powershell
Unblock-File .\install.ps1
```

Se quiser desbloquear todos os `.ps1` do pacote:

```powershell
Get-ChildItem -Recurse -Filter *.ps1 | Unblock-File
```

Depois execute novamente.

---

# 49. Verificando as Skills instaladas

No PowerShell:

```powershell
Get-ChildItem .github\skills
```

Você deve encontrar:

```text
analyze-legacy-solution
investigate-legacy-bug
analyze-change-impact
prepare-speckit-context
prepare-feature-branch
```

---

# 50. Mentalidade final

Se você esquecer todo o README, lembre apenas isto:

```text
QUERO ENTENDER
      ↓
Discovery


QUERO MUDAR
      ↓
prepare-speckit-context
      ↓
branch
      ↓
Spec Kit


TENHO UM BUG
      ↓
investigate-legacy-bug


JÁ DESCOBRI O BUG
      ↓
prepare-speckit-context
      ↓
branch
      ↓
Spec Kit


QUERO PROGRAMAR
      ↓
somente depois de:
SPEC + PLAN + TASKS
```

---

# 51. O fluxo completo

```text
                  SISTEMA LEGADO
                        │
                        ▼
               Persistent Knowledge
                        │
                        ▼
                 Knowledge Preflight
                        │
                   já sabemos?
                   /       \
                 SIM       NÃO
                  │         │
              reutiliza   Discovery
                  │         │
                  └────┬────┘
                       │
                       ▼
                     AS-IS
                       │
                       ▼
                    HANDOFF
                       │
                       ▼
              prepare-feature-branch
                       │
                       ▼
                  feature/...
                       │
                       ▼
                 /speckit.specify
                       │
                       ▼
                 /speckit.clarify
                       │
                       ▼
                   /speckit.plan
                       │
                       ▼
                  /speckit.tasks
                       │
                       ▼
                 /speckit.analyze
                       │
                       ▼
                /speckit.implement
                       │
                       ▼
                /speckit.converge
```

---

# 52. Por que fazemos tudo isso?

Porque em sistemas legados:

```text
mudar código
```

é fácil.

O difícil é saber:

```text
o que aquela mudança pode quebrar.
```

Por isso trabalhamos assim:

```text
Descubra uma vez.

Guarde o conhecimento.

Reutilize muitas vezes.

Investigue somente gaps.

Especifique antes de alterar.

Planeje antes de implementar.

Implemente com contexto.
```

---

# Legacy Discovery + Spec Kit

> **Discovery descobre fatos.
> Persistent Knowledge evita redescobertas.
> HANDOFF conecta o legado à mudança.
> Spec Kit governa o TO-BE.
> Branch isola a alteração.
> Implementação só acontece depois do entendimento.**
