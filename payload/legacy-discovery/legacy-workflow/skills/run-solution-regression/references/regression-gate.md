# Gate completo de regressão

## Validar os comandos aprovados

Use exclusivamente `solution_path`, `build_configuration`, `build_command`, `regression_command` e `regression_scope` do `DESIGN-FIX-{NNNN}.md` aprovado. Confirme que os comandos ainda existem e que o escopo corresponde à solution ou pipeline oficial.

Não redescubra nem substitua silenciosamente o gate durante a regressão. Ausência, ambiguidade ou incompatibilidade produz `BLOCKED`/`PLAN_INVALID` e volta ao owner do DESIGN.

Não instale SDK, workload, runner ou pacote. Não altere configuração para excluir testes falhos.

## Executar

1. Registre branch, commit HEAD, solution e configuração.
2. Execute o build da **solution inteira**. Se falhar, resultado final `BLOCKED`; não rode testes sobre build inválido.
3. Valide que `regression_scope` cobre todos os projetos/suítes de teste definidos pela solution ou pipeline, incluindo unitários, integração e contrato quando fizerem parte do gate oficial.
4. Execute a regressão completa com o mecanismo oficial. Quando o pipeline separa comandos, execute todos e registre cada um.
5. Compare testes descobertos, executados, aprovados, falhos, ignorados e não executados. Divergência sem explicação impede `PASSED`.
6. Confirme que o teste que originalmente comprovou o bug está presente e passou. Se não foi descoberto, o gate não pode ser aprovado.

## Falhas e instabilidade

- Não corrija código ou teste.
- É permitida uma única repetição diagnóstica somente dos testes falhos, sem qualquer alteração entre execuções.
- Passou apenas na repetição: classifique como `UNSTABLE`, não como aprovado limpo.
- Falha novamente: classifique como `FAILED`.
- Falha por ambiente/serviço/credencial: classifique como `BLOCKED`.
- Pare após essa repetição; não execute ciclos adicionais.

## Resultado

- `PASSED`: build da solution verde, suíte completa executada, teste do bug passou e nenhuma falha/omissão não explicada.
- `FAILED`: ao menos um teste falhou de forma reproduzível.
- `UNSTABLE`: teste falhou e passou na única repetição diagnóstica.
- `BLOCKED`: build, ambiente ou descoberta impediram conclusão confiável.
