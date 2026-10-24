# Contribuindo

Contribuições devem manter o projeto aberto, didático e rastreável. Antes de uma mudança, confira o estado Git, leia o escopo da fase e sincronize sua cópia sem descartar trabalho local. Não inclua mídia de clientes, material comercial sem autorização, credenciais, arquivos pessoais ou dumps de conversas.

Para cada unidade, registre objetivo, escopo, decisões delegadas, recursos/custo, condição de parada e aceite esperado. Use `python3 scripts/aglaia.py session-start ...` para criar um registro próprio, `event <run-id> ...` para acrescentar evidência e `session-close <run-id> ...` para fechar. Não edite eventos de outra sessão. Eventos são append-only. O mecanismo de claim protege somente escritores cooperantes no mesmo filesystem local; não coordena hosts.

Rode `python3 -m unittest discover -s tests -v` e `python3 scripts/aglaia.py verify --profile fast` antes de propor uma mudança. Mudanças que alteram scripts, governança, proveniência ou fechamento exigem `--profile impact`. `full` é reservado à verificação integral da fase ou release. CI sempre roda os gates de governança e testes portáteis.

Pull requests devem explicar evidência, decisão, ações/pendências e consumidores afetados. Uma configuração documentada não prova adapter ativo; um teste local não prova ensaio em harness, integração real ou aceite humano.
