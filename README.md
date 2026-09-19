# Legacy Discovery + Spec Kit

**Deixe a IA entender o seu sistema antigo *antes* de mexer nele.**

Quando você pede uma mudança para a IA num sistema legado, ela costuma chutar como o sistema funciona hoje e chutar o que o pedido quis dizer. É assim que nascem os bugs novos.

Esta ferramenta obriga a IA a seguir três passos antes de escrever código:

```text
1. ENTENDER            2. TIRAR AS DÚVIDAS           3. SÓ ENTÃO FAZER
"Como o sistema        "O que o pedido quer dizer?   Especificar, planejar
 funciona hoje?"        O que não pode quebrar?"     e programar (Spec Kit)
```

E tem uma **trava de segurança**: a IA não consegue aprovar nada sozinha, nem mexer no código de produção durante a análise, nem publicar nada. Quem aprova é você.

**[⬇️ Baixar a última versão](https://github.com/rafaeldevwp/legacy-discovery-speckit/releases/latest)** · **[📖 Manual passo a passo](docs/MANUAL.md)**

---

## Como isso ajuda no seu dia a dia

**Sem a ferramenta**, a IA lê alguns arquivos, acha que entendeu e sai programando. Em sistema legado isso costuma dar errado, porque a regra de verdade está espalhada, sem documentação, e o pedido do PM quase sempre é vago.

**Com a ferramenta**, antes de qualquer código a IA:

| Faz | Você ganha |
|---|---|
| Mapeia como o sistema funciona hoje, citando `arquivo:linha` | Você confere a evidência em vez de confiar num palpite |
| Lista o que o pedido não deixa claro | As dúvidas vão para o PM **antes** de virar retrabalho |
| Separa fato, suposição e o que ninguém sabe | Você sabe o que é certo e o que ainda é aposta |
| Aponta o que pode quebrar | Você já sabe o que testar |
| Espera a sua aprovação | Nada avança sem uma pessoa decidir |

### Cenários reais

Os exemplos abaixo são ilustrativos, mas as situações são as que você vive em sistemas antigos.

#### 1. "É só trocar o limite de desconto de 10% para 15%"

**A situação:** o PM acha que é uma linha de código. Só que o 10% aparece em três lugares: no serviço de negócio, numa procedure do banco e num relatório que o financeiro usa.

**Sem a ferramenta:** a IA troca no serviço, o teste passa e vai para produção. O relatório continua calculando com 10%, e o financeiro só descobre no fechamento do mês.

**Com a ferramenta:**
```text
/legacy.story
US-310: Aumentar o limite de desconto de 10% para 15%.
Quem decide regra de negócio: Marina (PM).
```
A ferramenta encontra os três pontos, cita o arquivo e a linha de cada um, e devolve perguntas para a Marina que a IA não pode responder sozinha:
- o 15% vale para **todos** os clientes ou só para alguns?
- o relatório do financeiro deve mudar junto?

Nada avança até essas respostas estarem registradas.

#### 2. Bug que só acontece em produção

**A situação:** "A segunda via do boleto às vezes sai com vencimento no domingo." Ninguém sabe onde é. O cálculo passa por quatro classes e por uma regra de tolerância.

**Sem a ferramenta:** a IA aponta uma causa com toda a confiança e "corrige". O bug continua, porque a causa era outra.

**Com a ferramenta:**
```text
/legacy.bug
Sintoma: segunda via sai com vencimento no domingo.
Esperado: próximo dia útil. Ambiente: produção, desde 01/09.
```
Você recebe uma lista de hipóteses **ordenadas por confiança**, cada uma com a evidência que a sustenta e as que foram descartadas (com o motivo). Ela **não corrige nada**. Você decide o próximo passo já sabendo qual é a causa mais provável e qual teste prova isso.

#### 3. História do PM vaga demais

**A situação:** "Quando o serviço externo demorar, o cidadão não pode ficar sem resposta." Demorar quanto? Sem resposta como? Mostrar o quê?

**Sem a ferramenta:** a IA decide sozinha (por exemplo, 30 segundos e uma mensagem genérica). Na homologação o PM diz que não era isso, e o trabalho é refeito.

**Com a ferramenta:** `/legacy.story` devolve as perguntas numeradas (AMB-01, AMB-02…), marcando quais impedem o início. Você leva ao PM, cola as respostas com `/legacy.answer`, e elas ficam registradas com o nome de quem respondeu. Se a resposta for "o normal", a IA pergunta de novo.

#### 4. Módulo que ninguém conhece mais

**A situação:** quem escreveu saiu da empresa, não há documentação e você precisa alterar o cálculo de multa por atraso.

**Sem a ferramenta:** você passa dias lendo código antes de arriscar uma alteração.

**Com a ferramenta:**
```text
/legacy.analyze Como funciona o cálculo de multa por atraso?
```
Você recebe um mapa do módulo (quem chama quem, onde ficam as regras, o que depende de quê), salvo no repositório. O mapa é reaproveitado nas próximas histórias, então a IA não relê tudo de novo.

#### 5. Método usado por sistemas que você nem enxerga

**A situação:** você vai alterar um método de gravação de histórico. Ele é chamado por três telas, um serviço WCF e talvez por integrações de outras equipes.

**Sem a ferramenta:** você descobre os consumidores quando eles quebram.

**Com a ferramenta:**
```text
/legacy.impact Método HistoricoRepository.Gravar, mudança de comportamento
```
Você recebe o nível de risco com critério objetivo, quem depende do método direta e indiretamente, e uma lista do que **não foi possível ver** (por exemplo, consumidores externos ao repositório). Esse aviso já diz com quem conversar antes de mexer.

#### 6. A IA "ajudando" além da conta

**A situação:** a IA, tentando ser útil, marca o refinamento como aprovado, edita as próprias regras para passar na validação ou faz `git push`.

**Com a ferramenta:** a trava de segurança nega. Aprovar só é possível por um comando que **você** roda no seu terminal, e o que a IA tentou fica registrado. Quando alguém pergunta "quem aprovou isso?", a resposta é uma pessoa, com nome e data.

### Resumo do ganho

```text
Menos retrabalho    perguntas resolvidas antes de programar
Menos regressão     você sabe o que pode quebrar e o que testar
Menos dependência   o conhecimento do sistema fica registrado no repositório
Mais controle       a IA ajuda, mas quem decide e aprova é você
```

---

## O que você precisa ter

| Item | Como saber se você tem |
|---|---|
| Windows (Linux e macOS também funcionam, veja o Manual) | — |
| **Git** | abra o terminal e digite `git --version` |
| **Python 3.11 ou mais novo** | `python --version` |
| **VS Code** com **GitHub Copilot** | o ícone do Copilot aparece no VS Code |
| Internet (só na instalação) | — |

Não sabe se tem? Digite os comandos acima. Se aparecer um número de versão, está ok.

---

## Instalar (3 passos, uns 5 minutos)

**1. Salve seu trabalho.** Na pasta do seu sistema, faça commit do que estiver pendente. (Se não sabe fazer isso, peça a alguém do time. É só para garantir que nada se misture.)

**2. Baixe e descompacte.** Na página de [Releases](https://github.com/rafaeldevwp/legacy-discovery-speckit/releases/latest), baixe o arquivo `.zip` e descompacte numa pasta **curta**, por exemplo `C:\Ferramentas\`.

> Pasta curta importa: caminhos muito compridos no Windows fazem arquivos serem ignorados sem aviso.

**3. Dê dois cliques em `INSTALAR-WINDOWS.bat`.** Quando ele pedir o repositório, cole o caminho da pasta do seu sistema (a que tem a pasta `.git`):

```text
Repositorio: C:\Projetos\MeuSistemaLegado
```

Espere aparecer **INSTALAÇÃO CONCLUÍDA**. Ele faz backup do que altera, então é seguro.

---

## Conferir se funcionou (1 minuto)

1. Abra a pasta do seu sistema no **VS Code**.
2. Abra o chat do **Copilot** e troque o modo para **Agent**.
3. Digite `/legacy.help` e envie.

Apareceu uma lista de comandos? Pronto, está instalado.

---

## Seu primeiro dia

Faça isto **uma única vez** por sistema.

**1. Diga as regras do projeto.** No chat:

```text
/speckit.constitution
Este é um sistema legado crítico. Preserve o que já existe e não modernize
nada sem justificativa. Não trate palpite como fato.
```

**2. Peça o primeiro mapa do sistema.**

```text
/legacy.analyze Visão geral: projetos, o que cada um faz e integrações externas.
```

A IA fará algumas perguntas rápidas (o que olhar, até onde ir). Responda curto. Ela guarda o que aprendeu e reaproveita depois, sem reler tudo.

> Não peça "estude o sistema inteiro a fundo". Comece pela visão geral e aprofunde só a parte de que a história precisa.

---

## Uso diário: chegou uma história do PM

Este é o caminho que você vai repetir sempre. **Você só digita comandos; a IA faz o trabalho pesado e para quando precisa de você.**

| # | Você digita | O que acontece |
|---|---|---|
| 1 | `/legacy.story` + a história do PM, copiada como veio | A IA descobre como o sistema faz isso hoje e monta um refinamento, com perguntas para o PM se houver dúvida |
| 2 | Leve as perguntas ao PM. Depois: `/legacy.answer REFINEMENT-0001 AMB-01: <resposta do PM>` | A IA registra as respostas. Se surgir dúvida nova, volta ao passo 2 |
| 3 | `/legacy.approve REFINEMENT-0001` | A IA resume tudo e te entrega **um comando**. Leia o resumo |
| 4 | **Você** cola esse comando no terminal do VS Code | Isso é a sua aprovação. A IA não consegue fazer isso por você |
| 5 | `/legacy.branch nome-curto-da-mudanca` | Cria a branch de trabalho, do jeito certo |
| 6 | `/speckit.specify` + a história | A partir daqui é o Spec Kit: `clarify`, `plan`, `tasks`, `implement` |

**Exemplo real do passo 1:**

```text
/legacy.story
US-4821: Como atendente, quero que a consulta de veículos mostre a última
situação conhecida quando o serviço externo demorar, para não deixar o
cidadão sem resposta.

Quem decide regra de negócio: Marina (PM).
```

**Perdido? Digite `/legacy.status`.** Ele mostra em que passo cada história está e qual é o próximo comando.

---

## Outros usos comuns

| Eu quero... | Digite |
|---|---|
| Entender como uma parte funciona | `/legacy.analyze Como funciona o cálculo de multa?` |
| Achar a causa de um bug | `/legacy.bug` + o que acontece, o que deveria acontecer, onde |
| Saber o que quebra se eu mexer numa coisa | `/legacy.impact` + o que vai mudar |
| Ver o andamento das histórias | `/legacy.status` |
| Ver todos os comandos | `/legacy.help` |
| Checar se está tudo em ordem | `/legacy.validate` |

`/legacy.bug` **só investiga, nunca corrige.** Ele devolve as causas mais prováveis, com a evidência de cada uma.

---

## Regras que a ferramenta impõe (e por quê)

| A IA **não pode** | Motivo |
|---|---|
| Aprovar um refinamento | Só uma pessoa decide que o pedido está claro |
| Escrever código de produção durante a análise | Análise é para entender, não para alterar |
| Fazer `git commit`, `push` ou trocar de branch por conta própria | Nada é publicado sem você |
| Mexer nas próprias regras | Senão ela poderia afrouxá-las para passar |

Se ela tentar e a trava negar, é normal: ela explica o motivo e diz o que **você** precisa fazer. Não tente contornar.

Os arquivos que a IA gera na análise ficam **só no seu computador** (`.github/copilot-knowledge/`) e não vão para o Git.

---

## Deu problema?

| Sintoma | O que fazer |
|---|---|
| `/legacy.` não mostra nenhum comando | Confirme que o chat está em **Agent**; feche e reabra o VS Code |
| "python não é reconhecido" | Instale o Python 3.11+ marcando **Add to PATH** e reabra o VS Code |
| A instalação falhou no meio | Rode o `.bat` de novo; ele é seguro de repetir. Os backups ficam em `backups/` |
| A IA parou e não avança | Digite `/legacy.status`: ele diz o que está esperando de você |
| Mensagem de erro que você não entende | Digite `/legacy.validate` e veja o capítulo 34 do Manual |

Mais casos no [capítulo 37 do Manual](docs/MANUAL.md#37-solução-de-problemas).

---

## Quer saber mais?

- **[Manual](docs/MANUAL.md)**: começa por um guia prático para iniciantes e depois aprofunda cada comando, exemplos completos e referência.
- **Instalação por linha de comando, Linux/macOS, atualização de versão anterior:** capítulos 8 a 10 do Manual.
- **Como a trava de segurança funciona por dentro:** capítulo 31 do Manual.

<sub>Bundle 1.4.1 · Legacy Discovery V2.4 · Spec Kit oficial 1.0.1 · GitHub Copilot · Python 3.11+ · mais de 100 testes automatizados em Windows e Linux</sub>
