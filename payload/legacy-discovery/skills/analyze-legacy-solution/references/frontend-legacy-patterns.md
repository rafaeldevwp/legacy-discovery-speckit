# Front-end legado: AngularJS + ASP.NET Web Forms (ASPX)

Use esta referência durante a Fase 3 (`discovery-process.md`) quando o projeto detectado for de UI/Web. Front-end legado geralmente não aparece bem em `.csproj` — os sinais estão nos arquivos e no HTML.

## Passo 0.5 — Detectar o(s) stack(s) de front-end do projeto

Um mesmo projeto de UI legado pode ter **mais de um** stack coexistindo. Não assuma um só — verifique todos:

- **AngularJS (1.x)** — procure por: `angular.module(`, `angular.controller(`, `$scope`, `ng-app`, `ng-controller`, `$routeProvider`/`$stateProvider` (roteamento), arquivo `bower.json` (gerenciador de pacotes típico dessa era), pasta tipo `Scripts/app/` com subpastas `controllers/`, `services/`, `directives/`, `views/` (templates `.html` parciais).
- **ASP.NET Web Forms (ASPX)** — pares `.aspx` + `.aspx.cs` (code-behind; trate como uma unidade só), `.master` (master pages/layout compartilhado), `.ascx` + `.ascx.cs` (user controls reutilizáveis). **Ignore `*.designer.cs`** — é gerado automaticamente, não tem informação de negócio.
- **ASMX / PageMethods (backend de AJAX antigo, comum nessa combinação)** — arquivos `.asmx` com atributo `[WebMethod]`/`[ScriptService]`, ou métodos estáticos com `[WebMethod]` dentro de um `.aspx.cs` chamados via `PageMethods.NomeDoMetodo()` no JS. Isso é frequentemente o backend real que o AngularJS consome, mesmo num app com Web API "moderna" em paralelo — **procure por ambos, não assuma que é só um ou outro.**

Registre no `projects/PROJECT-{project-slug}.md` qual combinação foi encontrada.

## Detectar o padrão híbrido (o mais comum nesse tipo de legado)

Procure por `ng-app` **dentro de arquivos `.aspx` ou `.master`** — isso indica que uma página Web Forms está servindo de "casca" e o AngularJS é bootstrapado dentro dela (ilha de SPA dentro de um app multi-page tradicional). Isso é uma decisão arquitetural relevante — considere gerar um ADR (ver `adr-format.md`) se o padrão for consistente em várias páginas.

## Mapear a fronteira front-end ↔ back-end (o valor real da análise aqui)

Isso é o que mais importa entender num híbrido — qual JS chama qual endpoint:
- Nos arquivos de `services/`/`factories/` do AngularJS, procure chamadas `$http.get(`, `$http.post(`, `$resource(` — extraia só as **URLs/rotas** chamadas, não o corpo da função.
- Cruze essas rotas com os Controllers já mapeados na análise backend (`Controllers/`, `.asmx`, `PageMethods`) para saber quem serve quem.
- Registre esse mapeamento na seção "Estrutura relevante" do `projects/PROJECT-{project-slug}.md`.

## Limites (não vale a pena ir mais fundo que isso)

- Não abra cada controller/service AngularJS individualmente — liste os arquivos por nome e leia só os 2-3 mais centrais (geralmente o(s) que mais outros arquivos referenciam, ou o que está no módulo principal `app.js`).
- Não tente resolver a árvore de dependency injection do AngularJS em detalhe.
- Não abra `.html` de views parciais a menos que o nome sugira ser uma tela central do fluxo principal.
- `ViewState` e detalhes de ciclo de vida de Web Forms (`Page_Load`, `Page_Init` etc) — só mencione que existem se forem incomuns; não é preciso narrar o ciclo de vida padrão do ASP.NET.
