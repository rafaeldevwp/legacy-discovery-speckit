# Legacy .NET Skills para GitHub Copilot

Conjunto de skills para compreender, investigar e planejar mudanças com mais segurança em solutions C#/.NET legadas.

O pacote foi desenhado para solutions grandes, monorepos e ambientes híbridos que podem combinar .NET moderno, .NET Framework clássico, WCF, ASMX, Web Forms, AngularJS, Entity Framework, `packages.config` e projetos de teste com diferentes frameworks.

O objetivo não é fazer o Copilot ler todo o repositório a cada pergunta. As skills trabalham em etapas, reaproveitam conhecimento salvo localmente e aprofundam apenas a área necessária.

## Fluxo proposto

```text
Entender a solution
        ↓
Investigar o bug
        ↓
Gerar e executar um teste que comprove o ofensor
        ↓
Analisar o impacto da mudança
        ↓
Gerar SPEC → DESIGN → TASKS
        ↓
O time implementa e aprova a mudança
        ↓
Verificar a correção e a regressão
        ↓
Atualizar a base de conhecimento
```

## Skills incluídas

### 1. `analyze-legacy-solution`

Responde à pergunta: **“O que é esta solution e qual é a responsabilidade de cada projeto?”**

Principais capacidades:

- Descoberta estrutural de `.sln`, `.csproj` e dependências internas.
- Compatibilidade com projetos SDK-style e `.csproj` clássico.
- Identificação de .NET Framework, .NET moderno e solutions híbridas.
- Reconhecimento de `PackageReference` e `packages.config`.
- Mapeamento de chamadas entre projetos por WCF, ASMX, HTTP e outros serviços.
- Suporte a Web Forms, AngularJS e aplicações híbridas.
- Visão arquitetural inspirada no C4.
- ADRs inferidos a partir do código, sempre identificados como inferências.
- Deep dives opcionais para classes, métodos e regras específicas.
- RFCs de modernização somente quando solicitadas.

### 2. `investigate-legacy-bug`

Responde à pergunta: **“Algo está errado; onde provavelmente está o problema?”**

Principais capacidades:

- Estruturação do sintoma, comportamento esperado e resultado observado.
- Busca progressiva por candidatos, evitando leituras desnecessárias.
- Hipóteses classificadas por evidência e confiança.
- Registro dos candidatos descartados.
- Geração opcional de teste de regressão que nasce falhando para comprovar o bug.
- Reutilização do framework de teste e da biblioteca de mock já usados pelo projeto.
- Detecção de MSTest, xUnit, NUnit, Moq, NSubstitute e FakeItEasy.
- Proteção contra uso de CPF, CNPJ ou outros dados pessoais reais em testes.
- Registro da evidência de execução que confirma, refuta ou deixa a hipótese inconclusiva.
- Separação entre falha funcional, falha de build e problema de ambiente.

Esta skill não corrige automaticamente o código de produção.

### 3. `analyze-change-impact`

Responde à pergunta: **“Se eu alterar isto, o que pode ser afetado?”**

Principais capacidades:

- Mapeamento de dependentes por `ProjectReference`.
- Confirmação de uso real de classes e métodos.
- Identificação de dependências indiretas por serviços.
- Detecção de consumidores externos ao repositório.
- Consulta a ADRs, deep dives e testes existentes.
- Identificação da documentação que ficará desatualizada.
- Classificação objetiva do risco como Alto, Médio ou Baixo.

O critério de risco considera quantidade e tipo de dependentes, contratos externos e cobertura de testes. A skill informa o raio de impacto, mas não decide se a mudança deve ser realizada.

### 4. `coordinate-fix`

Responde a duas perguntas:

- **Antes da implementação:** “Como podemos organizar uma correção que mitigue os impactos encontrados?”
- **Depois da implementação:** “A correção resolveu o problema sem causar regressões no raio afetado?”

Principais capacidades:

- Criação de um pacote rastreável separado em `SPEC.md`, `DESIGN.md` e `TASKS.md`.
- Ligação entre investigação, teste do bug e análise de impacto.
- Requisitos funcionais (`REQ-*`) e não funcionais (`NFR-*`) com critérios de aceite.
- Design técnico com componentes, contratos, alternativas, trade-offs e decisões (`DEC-*`).
- Tarefas pequenas e verificáveis (`TASK-*`) ligadas aos requisitos e ao design.
- Matriz de rastreabilidade entre requisito, decisão, tarefa e evidência.
- Mitigação específica para cada dependente afetado.
- Plano de tarefas pequenas e verificáveis.
- Critérios de aceite técnicos e de negócio.
- Estratégia de verificação e rollback.
- Verificação do teste que originalmente comprovou o bug.
- Regressão orientada pelo raio de impacto, sem executar testes indiscriminadamente.
- Registro em `VERIFICATION.md` como `VERIFICADO`, `FALHOU` ou `PARCIAL/BLOQUEADO`.
- Atualização da documentação que descrevia o comportamento anterior.

A skill gera e verifica o plano, mas não implementa a correção, não faz deploy e não executa rollback.

## Memória local e progressive disclosure

O conhecimento descoberto pelas skills é persistido em:

```text
.github/copilot-knowledge/
├── INDEX.md
├── solution-overview.md
├── projects/
├── decisions/
├── deep-dives/
├── proposals/
├── investigations/
├── impact-analyses/
└── fix-plans/
    └── FIX-0001-exemplo/
        ├── SPEC.md
        ├── DESIGN.md
        ├── TASKS.md
        └── VERIFICATION.md
```

O `INDEX.md` é o ponto de entrada. Ele permite ao Copilot descobrir o que já foi documentado antes de abrir arquivos maiores ou analisar o código novamente.

Essa arquitetura reduz o consumo de tokens por meio de três princípios:

1. Ler primeiro a estrutura e o índice.
2. Reutilizar o conhecimento já persistido.
3. Abrir código detalhado somente quando a pergunta exigir.

## Instalação

Extraia o conteúdo do pacote na raiz do repositório. A estrutura final deve ser semelhante a:

```text
seu-repositorio/
└── .github/
    └── skills/
        ├── analyze-legacy-solution/
        ├── investigate-legacy-bug/
        ├── analyze-change-impact/
        └── coordinate-fix/
```

Se o repositório já tiver uma pasta `.github`, mescle as pastas sem apagar os arquivos existentes.

## Exemplos de uso

As skills são descobertas pelo GitHub Copilot a partir do contexto do pedido. Em linguagem natural, você pode solicitar:

```text
Analise esta solution e explique a responsabilidade principal de cada projeto.
```

```text
O cálculo de frete do produto 123 está retornando R$ 150, mas deveria retornar R$ 100. Investigue onde pode estar o problema.
```

```text
Gere um teste de regressão para comprovar essa hipótese, reutilizando o projeto de testes e a biblioteca de mock já existentes.
```

```text
Preciso alterar o método CalcularFrete. Analise o que pode ser afetado antes de qualquer mudança.
```

```text
Com base na investigação confirmada e na análise de impacto, gere a SPEC, o DESIGN e as TASKS para coordenar a correção.
```

```text
A implementação da FIX-0001 foi concluída. Verifique a correção e execute a regressão orientada pelo impacto.
```

## Regras de segurança e qualidade

- Código de produção não é alterado automaticamente pelas skills deste pacote.
- Hipóteses não são apresentadas como fatos confirmados.
- Uma falha de infraestrutura não é considerada prova do bug.
- Build verde isolado não comprova que a correção funcionou.
- Dados pessoais reais não devem ser gravados em testes ou documentação.
- Frameworks e bibliotecas existentes têm prioridade sobre novas dependências.
- Mudanças estruturais, como criar um projeto de testes, exigem confirmação.
- Aprovação da SPEC, implementação, deploy e rollback permanecem decisões humanas.

## Evolução do pacote

### Etapa 1 — Análise da solution

O trabalho começou como um prompt único para leitura de solutions legadas. Ele foi convertido em uma skill com referências carregadas sob demanda e memória persistida no repositório.

### Etapa 2 — Compatibilidade com legado real

Foram adicionados suporte a `.csproj` clássico, `packages.config`, `Web.config`, `App.config`, `Global.asax`, WCF, ASMX, EDMX, Web Forms, AngularJS e solutions híbridas.

### Etapa 3 — Documentação arquitetural

A análise passou a produzir visão C4 simplificada, ADRs inferidos, deep dives seletivos e RFCs opcionais para modernização.

### Etapa 4 — Investigação de bugs

Foi criada uma skill dedicada à triagem de sintomas, geração de hipóteses com evidência, criação de testes de regressão e reaproveitamento da base de conhecimento.

### Etapa 5 — Adaptação aos testes existentes

A geração de testes passou a detectar automaticamente o framework de testes, a biblioteca de mock e as convenções já usadas no projeto, evitando impor Moq, NSubstitute ou qualquer pacote novo.

### Etapa 6 — Análise de impacto

Foi adicionada uma skill para mapear dependentes de compilação, chamadas de serviço, consumidores externos, cobertura de testes e risco antes de qualquer alteração.

### Etapa 7 — Evidência do ofensor

O relatório de investigação passou a registrar o teste executado, resultado, ambiente, evidência mínima e conclusão. O resultado pode confirmar, refutar ou manter a hipótese inconclusiva.

### Etapa 8 — Coordenação da correção

Foi criada a skill `coordinate-fix`, responsável pelo fluxo SPEC → DESIGN → TASKS, mitigação dos impactos, critérios de aceite, verificação pós-correção, regressão orientada e atualização da documentação. Cada iniciativa recebe uma pasta própria e usa IDs rastreáveis (`REQ`, `NFR`, `DEC` e `TASK`).

### Etapa 9 — Consistência dos critérios de risco

O critério de classificação foi revisado para remover uma ambiguidade em que a ausência de teste poderia classificar o mesmo cenário simultaneamente como risco Alto e Médio.

## Limitações conhecidas

- A qualidade da investigação depende de um cenário concreto e de um comportamento esperado conhecido.
- Dependentes externos podem ser identificados sem que seja possível validá-los dentro do repositório.
- Projetos muito antigos podem exigir runners ou ferramentas que não estejam disponíveis no ambiente atual.
- A data de modificação do `.csproj` detecta bem mudanças estruturais, mas não garante que todo conteúdo `.cs` permaneça atualizado na documentação.
- Regras de negócio inferidas do código devem ser confirmadas pelo time responsável.

## Licença e contribuição

Defina a licença do repositório antes da distribuição pública. Melhorias são bem-vindas, especialmente novos padrões de legado, frameworks de teste e cenários reais de monorepos .NET.
