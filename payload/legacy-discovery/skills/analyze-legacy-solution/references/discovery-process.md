# Processo de descoberta (usar só quando NÃO houver conhecimento salvo reaproveitável)

Execute na ordem. Cada fase é mais cara que a anterior — não pule etapas, e pare de ir mais fundo assim que tiver informação suficiente.

## Passo 0 — Detectar o formato do projeto (obrigatório, condiciona tudo abaixo)

Antes de aplicar as fases, identifique, por projeto, qual formato de `.csproj` está em uso — os passos seguintes mudam dependendo disso:

- **SDK-style** (moderno, .NET Core/5+): `.csproj` curto, começa com `<Project Sdk="Microsoft.NET.Sdk">`, tag `<TargetFramework>` ou `<TargetFrameworks>`, dependências via `<PackageReference>`.
- **Legado clássico** (.NET Framework): `.csproj` longo/verboso, começa com `<Project ToolsVersion=... xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`, tag `<TargetFrameworkVersion>` (ex: `v4.7.2`), lista cada arquivo `.cs` explicitamente com `<Compile Include=...>`, dependências de NuGet em arquivo separado `packages.config` (não dentro do `.csproj`).

Isso também te diz se a solution é clássica, moderna ou híbrida. Registre em `SOLUTION-OVERVIEW.md`.

**Se o projeto for de UI/Web** (nome sugere `*.Web`, `*.UI`, `*.Site`, ou contém `.aspx`/pasta `Scripts`), carregue também `references/frontend-legacy-patterns.md` antes de prosseguir para a Fase 3 — front-end legado (Web Forms, AngularJS, ou a combinação dos dois) tem anchors próprios que não aparecem no `.csproj`.

## Passo 0.5 — Escopo: focar em projeto(s) específico(s), mesmo na primeira execução

Isso vale em dois cenários: **(a)** o `.sln` tem muitos projetos (regra prática: mais de ~15) e não faz sentido aprofundar tudo de uma vez; **(b)** o usuário pediu explicitamente para focar num projeto específico (ex: "analisa só o projeto X"), mesmo que seja a primeiríssima execução da skill neste repositório e não haja nenhum conhecimento salvo ainda.

Em ambos os casos, o processo é o mesmo:

1. Complete a Fase 1 (estrutural) e Fase 2/2.5 (dependências, inclusive chamadas de serviço) para **todos** os projetos da solution — isso é barato (só lê `.sln`/`.csproj`/config, não abre código de negócio) e é necessário pra saber com quem o projeto pedido se conecta, mesmo que você só queira entender um projeto.
2. Restrinja a Fase 3 (leitura de arquivos-âncora, a cara) **só ao(s) projeto(s) pedido(s) explicitamente.**
3. Registre `depth: COMPLETE` no frontmatter do projeto pedido e `depth: STRUCTURAL` nos demais. Reconstrua o `INDEX.md` pelo script compartilhado — nunca o edite manualmente.

Isso evita o pior cenário em monorepo: uma execução gigante e cara que ainda assim entrega pouca profundidade por projeto — e também atende quem só quer uma resposta rápida sobre um projeto específico sem pagar o custo de aprofundar a solution inteira de cara.

## Fase 1 — Descoberta estrutural (barata)

1. Localize `.sln` e liste todos os `.csproj` referenciados.
2. Liste a árvore de pastas de cada projeto (2-3 níveis). Não abra arquivos de código ainda.
3. Classifique cada projeto por convenção de nome/pasta. Reconheça tanto convenções modernas (`*.Domain`, `*.Application`, `*.Infra*`, `*.Api`, `*.Web`, `*.Tests`, `*.Worker`) quanto o padrão clássico em português comum em legado brasileiro: **Modelo** (entidades/POCOs das tabelas do banco), **Dados**/**DAL** (acesso a dados, queries, geralmente sufixo `.Dados`/`.DAL`), **Negócio**/**BLL** (regras de negócio, `.Negocio`/`.Business`/`.BLL`). Se não houver convenção clara, marque "a confirmar".

## Fase 2 — Mapeamento de dependências (barata)

- **SDK-style:** leia `<ProjectReference>` e `<PackageReference>` dentro do próprio `.csproj`.
- **Legado clássico:** leia `<ProjectReference>` no `.csproj` normalmente, mas os pacotes NuGet estão em `packages.config` na raiz do projeto — leia esse arquivo separadamente. Referências a DLLs soltas (`<Reference Include="...">` sem `HintPath` para pasta `packages\`) indicam dependência binária direta, sem NuGet — vale registrar como ponto de atenção.

Monte o grafo de dependências **em tempo de compilação** entre projetos — isso já revela boa parte da arquitetura, mas **não captura chamadas via serviço/rede** (ver Fase 2.5).

## Fase 2.5 — Mapeamento de chamadas de serviço entre projetos (runtime, diferente de ProjectReference)

Isso é **um segundo grafo, separado** do da Fase 2 — e costuma ser o mais revelador nesse tipo de legado: dois projetos sem nenhum `ProjectReference` entre si podem estar fortemente acoplados via WS sem isso aparecer em lugar nenhum do build.

Procure, **sem abrir código gerado automaticamente** (proxies de WS são enormes e não têm valor de leitura):

- **Pastas de proxy de serviço:** `Connected Services/`, `Service References/`, `Web References/` — não abra o `Reference.cs` gerado; só note a existência da pasta e leia `Reference.svcmap` ou o `.wsdl`/`.disco` associado para extrair o **nome/namespace do serviço referenciado**.
- **Configuração WCF:** em `Web.config`/`App.config`, seção `<system.serviceModel><client>` — cada `<endpoint address="..." contract="...">` diz exatamente qual serviço este projeto consome e onde.
- **Chamadas HTTP diretas:** `HttpClient`, `WebClient`, `WebRequest` com URL fixa ou vinda de config apontando para outro serviço — trate como "possível chamada a outro projeto/serviço".
- **ASMX/PageMethods entre projetos de backend** (não só consumidos pelo front-end, ver `frontend-legacy-patterns.md`): às vezes um `.asmx` de um projeto expõe a camada de Negócio para **outro projeto backend**, não só para UI.

Para cada chamada encontrada, tente casar o **serviço de destino** com um dos projetos já listados na Fase 1 (por nome/namespace). Se não bater com nenhum projeto desta solution, registre como **"dependência externa — fora do escopo desta análise"** (provavelmente outra solution/repositório que esta skill não enxerga).

## Fase 3 — Leitura seletiva de arquivos-âncora (moderada, só para projetos que precisam ser gerados/atualizados)

Abra somente, se existirem — **escolha o conjunto conforme o formato detectado no Passo 0**:

Comuns aos dois formatos:
- `Domain/`, `Entities/`, `Models/` (só nomes de classes por listagem — não abra cada arquivo)
- `README.md` do projeto

SDK-style / moderno:
- `Program.cs` / `Startup.cs`
- `*ServiceCollectionExtensions*` / `*DependencyInjection*`
- `*DbContext.cs` (só nomes de `DbSet<T>`)
- `Controllers/`/`Endpoints/` minimal API (só assinaturas públicas)

Legado clássico (.NET Framework):
- `Global.asax.cs` — equivalente ao `Program.cs`, ponto de entrada da aplicação web.
- `Web.config` / `App.config` — configuração, connection strings, `<appSettings>` (não copie segredos/senhas para o `.md`, só cite que existem).
- `App_Start/RouteConfig.cs`, `WebApiConfig.cs`, `BundleConfig.cs` — se for ASP.NET MVC/Web API clássico.
- `*.svc` / `*.svc.cs` — se for WCF, indica serviço SOAP; liste as operações do contrato (`[OperationContract]`), não o corpo.
- `Controllers/` clássico (ASP.NET MVC) ou `*.aspx.cs` (Web Forms, se aplicável) — só assinaturas de actions/handlers.
- `*Context.cs` (EF6 `DbContext` ou até `.edmx` para Entity Framework "Database First") — se houver `.edmx`, apenas registre a existência e não tente abrir o XML gigante do designer.

Limites (valem para os dois formatos):
- Não leia arquivos com mais de ~500 linhas por inteiro.
- Não releia um arquivo já visto.
- Não abra testes, a menos que o projeto seja de testes.
- Projetos claramente análogos (ex: vários `*.Migrations`) → analise um em detalhe e amostre os demais.
- Se um arquivo vier com encoding estranho (comum em código antigo, ex: Windows-1252 em vez de UTF-8) e aparecer cheio de caracteres ilegíveis, não tente decodificar — registre "arquivo com encoding legado, conteúdo não confiável" e siga em frente.

## Fase 4 — Busca dirigida por padrões (em vez de leitura exaustiva)

Use busca/grep para caçar sinais específicos:
- `TODO|FIXME|HACK|Obsolete` → dívida técnica.
- Padrões de auth: `[Authorize]` (MVC/WebApi clássico ou moderno), `JwtBearer` (moderno), `<authentication mode="Forms">` (clássico, em Web.config).
- Sinalizadores de stack legada: `System.Web`, `HttpContext.Current` (clássico, incompatível com .NET moderno), `WCF`, `EF6` vs `EF Core`, `.edmx`, VB.NET misturado no mesmo `.sln`.

Depois de concluir estas 4 fases, siga `output-format.md` para gerar e persistir o resultado.
