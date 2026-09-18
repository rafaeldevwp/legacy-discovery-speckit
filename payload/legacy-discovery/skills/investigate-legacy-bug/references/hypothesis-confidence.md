# Critério de confiança para hipóteses de investigação

Diferente do critério de "padrão arquitetural" da skill `analyze-legacy-solution` (que mede repetição/consistência), aqui a pergunta é outra: **o quanto a evidência encontrada explica o sintoma relatado.**

- **Alta** — existe um caminho de código traçável e específico que, seguido com o exemplo concreto relatado (Fase 0), produziria exatamente o comportamento errado descrito. Você consegue apontar a linha/condição exata.
- **Média** — o candidato está claramente envolvido no fluxo relacionado ao sintoma (mesma classe, mesmo dado, mesma operação), mas não foi possível confirmar que aquele caminho específico é o que gera o erro — falta o exemplo concreto, ou a lógica é complexa demais pra confirmar só lendo.
- **Baixa** — indício indireto (nome parecido, área geral do sistema), incluído só por completude — não deveria ser o foco da investigação, mas vale registrar caso as hipóteses de confiança maior não se confirmem.

## Regra: nunca apresentar Alta sem caminho traçável

Não marque uma hipótese como "Alta" só porque parece plausível ou porque é a explicação mais simples. "Alta" exige ter seguido o código passo a passo e chegado num ponto que bate com o sintoma — se isso não foi feito (por falta de exemplo concreto, por exemplo), a hipótese é no máximo "Média", mesmo que pareça óbvia.

## Isso não é uma garantia de correção

Confiança Alta aqui significa "a evidência estática aponta fortemente pra cá" — não significa "é isso, pode corrigir". Leitura de código não substitui reprodução real do bug. O relatório final sempre inclui um próximo passo de confirmação, mesmo quando a confiança é Alta.
