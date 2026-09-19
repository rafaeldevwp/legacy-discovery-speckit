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
