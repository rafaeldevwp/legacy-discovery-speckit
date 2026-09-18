# Critério de confiança (usado em toda a skill, não só em ADRs)

Sempre que um campo desta skill for **interpretação/inferência** (não leitura direta e inequívoca do código), marque com um destes três níveis. Critério objetivo, baseado em quantidade e consistência de evidência — não em impressão subjetiva do modelo:

- **Alta** — o padrão se repete de forma consistente em 3+ lugares (arquivos, projetos, ocorrências), sem exceção contraditória encontrada.
- **Média** — aparece, mas com poucas ocorrências (1-2) ou com alguma inconsistência (parte do código segue o padrão, parte não).
- **Baixa** — inferência feita a partir de um único indício indireto, sem repetição que confirme.

Isso mede **"o quão bem sustentado esse padrão está no código"**, nunca **"o quão certo estou do motivo por trás dele"** — motivação/intenção nunca ganha confiança alta só a partir de código; vai sempre para uma seção de perguntas em aberto, à parte.

## Quando NÃO marcar confiança

Campos que são **leitura direta e verificável** não precisam de selo de confiança — são fato, não interpretação. Exemplos: lista de `DbSet<T>` encontrados, lista de `ProjectReference`, nome de pacotes NuGet, existência de um arquivo. Reservar o selo para os campos que realmente exigem julgamento evita poluir o documento com confiança-alta óbvia demais pra ser útil.

## Onde isso se aplica nesta skill

- **ADRs** (`adr-format.md`) — campo `Confiança` no cabeçalho, sempre presente (é a natureza do ADR: sempre é inferência).
- **`projects/PROJECT-{project-slug}.md`** (`project-template.md`) — nos campos interpretativos.
- **`SOLUTION-OVERVIEW.md`** — no padrão arquitetural da solution.
