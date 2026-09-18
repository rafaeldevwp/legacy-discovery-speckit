---
schema_version: 1
artifact_type: PROJECT
id: PROJECT-{project-slug}
status: CURRENT
owner_skill: analyze-legacy-solution
created_at: {ISO-8601}
updated_at: {ISO-8601}
project_name: {NomeDoProjeto}
depth: STRUCTURAL | COMPLETE
source_modified_at: {ISO-8601 do .csproj}
---

# {NomeDoProjeto}

> Gerado por: skill analyze-legacy-solution
> Última atualização: {DATA_ISO}
> Baseado em: {DATA_MODIFICACAO_DO_CSPROJ} <!-- usado para detectar se está desatualizado -->

## Camada / Responsabilidade
(1 linha: o que este projeto representa na arquitetura — ex: "Domain: entidades e regras de negócio puras") (confiança: Alta/Média/Baixa — ver `confidence-criteria.md`)

## Core funcional
- (bullet 1: caso de uso / entidade principal)
- (bullet 2)
- (bullet 3)

## Estrutura relevante
- `Program.cs` / `Startup.cs`: (o que registra/configura, se aplicável)
- `*DbContext`: (DbSets principais, se aplicável)
- Controllers/Endpoints principais: (rotas de alto nível, se aplicável)
- Entidades/Models principais: (nomes das classes-chave)

## Front-end (omitir esta seção se o projeto não tiver UI)
- **Stack detectado:** (Web Forms puro / AngularJS puro / Híbrido Web Forms + AngularJS / outro) (confiança: Alta/Média/Baixa)
- **Páginas/telas centrais:** (principais `.aspx` ou rotas AngularJS)
- **Integração front↔back:** (lista `service/factory AngularJS → endpoint que consome`, incluindo `.asmx`/`PageMethods` se houver) (confiança: Alta/Média/Baixa por item, se a correspondência não for exata)

## Dependências
- **Projetos internos:** (referenciados via ProjectReference — fato, sem selo de confiança)
- **Pacotes externos relevantes:** (EF Core, MediatR, etc — fato, sem selo de confiança)
- **Chamadas de serviço feitas por este projeto (WS/WCF/ASMX/HTTP):** (lista `este projeto → chama → ProjetoX / serviço externo`; marque `(confiança: Baixa)` em qualquer item onde o destino não bateu exatamente com um projeto conhecido)
- **Chamadas de serviço recebidas por este projeto:** (se souber quem consome — ex: um `.asmx`/WCF exposto aqui, liste quem o chama, se identificável; mesma regra de confiança acima)

## Pontos de atenção / dívida técnica
- (TODO/FIXME relevantes, padrões legados, riscos — omitir seção se não houver nada relevante)

## Perguntas em aberto
- (coisas que não deu pra confirmar só lendo o código — "a confirmar com o time")
