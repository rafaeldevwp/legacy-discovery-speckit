# Geração de teste de regressão a partir de uma hipótese (módulo OPCIONAL)

Diferente do resto desta skill (que só aponta, nunca corrige), este módulo **gera um artefato executável** — mas ainda não é correção de código. É prova: transforma "provavelmente é aqui" (estático) em "roda e confirma" (executável). A correção do bug em si continua fora do escopo desta skill.

## Quando usar

Só quando o usuário pedir explicitamente, depois de já ter uma hipótese de investigação (`investigation-report-format.md`) — ex: "monta um teste pra esse cenário", "gera um teste de regressão pra essa hipótese".

## Pré-requisitos — não prossiga sem isso

1. **Precisa existir uma hipótese com Confiança Média ou Alta** (ver `hypothesis-confidence.md`). Se a única hipótese disponível for Baixa, avise que o teste seria construído sobre uma suposição fraca e pergunte se o usuário quer prosseguir mesmo assim ou investigar mais primeiro.
2. **Precisa do cenário concreto** (dado de entrada real do caso relatado, e o resultado esperado vs o observado) — sem isso não dá pra montar `Arrange`/`Assert` de verdade. Se faltar, peça antes de gerar qualquer coisa.

## Regra inegociável sobre dados sensíveis

**Nunca copie CPF, CNPJ, nome de cliente, e-mail, telefone ou qualquer dado pessoal real para dentro de um arquivo de teste.** Testes vão para o controle de versão e ficam lá permanentemente — isso é exposição de dado pessoal (LGPD), não só má prática.

- Se o cenário relatado incluir dado real, **gere um equivalente sintético que preserve as mesmas propriedades relevantes pra regra de negócio** (ex: CPF sintético que passa no dígito verificador, mas não corresponde a pessoa real; código de produto no mesmo formato, mas claramente um valor de teste).
- Se o sistema já tiver uma convenção de dados de teste/sandbox (procure por isso — massas de teste, ambiente de homologação, CPFs de teste documentados), use essa convenção em vez de inventar uma nova.
- Deixe um comentário no teste gerado indicando que o dado é sintético e qual propriedade do dado real ele preserva (ex: `// CPF sintético válido — reproduz o mesmo cenário de cliente Premium do caso relatado, sem usar dado real`).

## Processo

1. **Detecte o framework de teste já usado na solution.** Procure por projetos de teste existentes (`*.Tests.csproj`, `*.Test.csproj`) e veja qual framework está referenciado (MSTest, xUnit, NUnit). **Use o que já existe** — não introduza um framework novo numa solution que já tem outro, mesmo que o usuário tenha mencionado um framework diferente ao pedir. Se o usuário pediu explicitamente um framework diferente do que já existe na solution, confirme antes de seguir.
2. **Se não existir nenhum projeto de teste na solution:** isso é uma mudança estrutural (novo projeto, entrada no `.sln`), não uma simples geração de arquivo — **confirme com o usuário antes de criar**, e pergunte qual framework/biblioteca de mock ele prefere se não houver preferência óbvia no restante do ecossistema da empresa.
3. **Detecte a biblioteca de mock em uso, com prioridade em camadas** (não escolha aleatoriamente se houver mais de uma referenciada na solution):
   - **Prioridade 1 — o que já é usado no mesmo arquivo de teste** que você está editando/estendendo (se o arquivo já existir). Olhe os `using` no topo do arquivo (`using Moq;`, `using NSubstitute;`, `using FakeItEasy;`) — use o mesmo.
   - **Prioridade 2 — o que já é usado em outros arquivos do mesmo projeto de teste.** Procure por `using Moq;`/`using NSubstitute;`/`using FakeItEasy;` em outros arquivos `*Tests.cs` do mesmo projeto.
   - **Prioridade 3 — o que está referenciado no `.csproj`/`packages.config` do projeto de teste**, mesmo que ainda não tenha sido usado em nenhum teste (`<PackageReference Include="Moq" .../>`, `<PackageReference Include="NSubstitute" .../>`, ou entrada equivalente em `packages.config` no formato clássico).
   - **Se houver mais de uma biblioteca de mock referenciada na solution** (acontece em monorepo com múltiplos projetos de teste, cada um migrado em época diferente): use a que já está no projeto de teste específico onde este teste vai ser adicionado — não misture duas bibliotecas de mock no mesmo arquivo, mesmo que a solution como um todo use as duas em projetos diferentes.
   - **Se nada disso encontrar nenhuma biblioteca de mock instalada:** não escolha uma sozinho — pergunte ao usuário qual ele prefere (Moq costuma ser o padrão de fato em .NET, mas não presuma).
4. **Verifique se já existe um arquivo de teste para a classe em questão** (ex: `{Classe}Tests.cs`). Se existir, **adicione o novo teste como um método novo nesse arquivo** — mesma lógica de não-duplicação que já usamos em `deep-dive.md`. Não crie um arquivo por cenário.
5. Monte o teste:
   - **Arrange:** instancie a classe sob teste; mocke as dependências que ela usa (camada de Dados, chamadas de WS/serviço — nunca deixe o teste bater em banco ou serviço real) com o cenário exato relatado, usando dado sintético conforme a regra acima.
   - **Act:** chame o método exatamente como o cenário descreve.
   - **Assert:** afirme o **resultado esperado pelo PO** (não o resultado atual/bugado). O teste deve nascer vermelho — isso é o comportamento correto neste momento, não um erro de construção do teste.
6. Nomeie o teste de forma que a intenção fique clara mesmo sem ler o corpo — ex: `CalcularDesconto_ClientePremiumComPedidoAcimaDoLimite_DeveAplicarDescontoDe10Porcento`.

## Formato do teste gerado (exemplo ilustrativo com Moq — adapte à biblioteca de mock detectada no passo 3, ex: NSubstitute usa `Substitute.For<T>()` em vez de `new Mock<T>()`)

```csharp
[TestMethod] // ou [Fact] para xUnit, [Test] para NUnit — conforme detectado no passo 1
public void {NomeDescritivoDoCenario}()
{
    // Arrange — cenário sintético equivalente ao caso relatado (ver regra de dados sensíveis acima)
    var cpfSintetico = "{CPF sintético válido}";
    var mockDados = new Mock<I{InterfaceDaCamadaDeDados}>(); // trocar pela sintaxe da biblioteca detectada
    mockDados.Setup(d => d.{MetodoUsado}(It.IsAny<...>())).Returns({retorno que reproduz o cenário});

    var sut = new {ClasseSobTeste}(mockDados.Object /*, outras dependências mockadas */);

    // Act
    var resultado = sut.{MetodoInvestigado}({parametros do cenário});

    // Assert — resultado ESPERADO conforme relatado pela PO (não o resultado atual/bugado)
    Assert.AreEqual({valor esperado}, resultado);
    // Nota: este teste deve falhar até a correção do bug identificado na investigação de {DATA}.
}
```

## Onde salvar

No projeto de teste já existente (ou criado no passo 2), seguindo a convenção de pastas que a solution já usa. Adicione — não substitua — se já houver um arquivo de teste pra essa classe.

## Registro de rastreabilidade

Depois de gerar o teste, atualize o relatório de investigação correspondente (`investigations/{DATA}-{slug}.md`) com uma seção:

```markdown
## Teste de regressão gerado
- Arquivo: {caminho do teste}
- Framework: {detectado}
- Resultado esperado: FALHA até a correção do bug identificado acima nesta investigação.
```

## Executar e registrar a evidência do ofensor

Quando o usuário pedir para confirmar a hipótese, ou autorizar a execução do teste:

1. Rode somente o menor escopo que prova o cenário (preferencialmente o teste gerado, não toda a solution). Use o comando compatível com o projeto legado; não presuma que `dotnet test` funciona em projetos .NET Framework clássicos se a solution usa runner/MSBuild diferente.
2. Não instale SDK, runner, pacote ou workload sem autorização. Se o ambiente não puder executar o teste, entregue o comando exato para o usuário rodar e peça apenas o resultado necessário.
3. Remova da evidência tokens, strings de conexão, dados pessoais e caminhos de usuário desnecessários. Registre a mensagem de assert e o identificador do teste, não o log inteiro.
4. Atualize a seção `Evidência de execução` do relatório de investigação:
   - teste **falha no assert esperado e reproduz o sintoma** → status `Ofensor confirmado por teste`;
   - teste **passa antes da correção** → status `Hipótese refutada por teste` e reduza a confiança; não declare que o bug não existe;
   - falha de build, ambiente ou infraestrutura → resultado `INCONCLUSIVO`; não confunda com confirmação do bug.
5. Depois da correção, um teste verde ajuda a comprovar o critério de aceite. Na V2, a mudança e sua validação seguem o fluxo escolhido no `SPECKIT_HANDOFF`: Spec Kit core (`implement`/`converge`) ou, quando explicitamente escolhido, a extensão oficial de bug (`bug.fix`/`bug.test`). Esta skill não assume a execução pós-correção.

## Limite explícito

Este módulo não corrige o código de produção, não decide como consertar, e não deve ser encadeado automaticamente após uma investigação — só quando pedido. Uma falha de compilação/ambiente não confirma a hipótese. Se o teste passar (verde) antes da correção, revise a hipótese; não assuma que o bug não existe.
