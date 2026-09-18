# Spec Kit oficial usado por este bundle

Este bundle fixa o **GitHub Spec Kit / specify-cli 1.0.1**.

- Projeto: `github/spec-kit`
- Tag GitHub: `v1.0.1`
- Pacote oficial PyPI: `specify-cli==1.0.1`
- Python: `>= 3.11`
- Licença: MIT (veja `LICENSE.txt`)

O CLI não é uma cópia modificada. O instalador usa a distribuição oficial do
Spec Kit na primeira instalação e depois executa `specify init` no repositório alvo.

Isso mantém o Spec Kit atualizável e separa claramente:

- **Spec Kit oficial**: SDD / TO-BE
- **Legacy Discovery V2**: Discovery / AS-IS / Persistent Knowledge / HANDOFF
