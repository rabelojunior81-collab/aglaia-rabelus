# Plano da Fase 0 — fundação pública

## Envelope YOLO por fase

- **Objetivo:** criar origem pública revisável para Aglaia Rabelus / Aglaia Studio.
- **Escopo:** gênesis/proveniência, briefing, governança, estado, pesquisa inicial, decisão de licença, protocolo Matrix mínimo, scripts/tests e CI portátil.
- **Decisões delegadas:** organização de diretórios, formato Markdown/JSONL, Python stdlib compatível com runtime instalado, nomes de comandos e checks proporcionais.
- **Recursos/custo:** diretório local existente e GitHub já autorizado; sem dependências externas instaladas, APIs pagas ou créditos de modelo.
- **Parada:** qualquer necessidade de expor material privado/comercial, gastar crédito, tocar serviço global/máquina remota, ativar hook pessoal/global, escolher stack completa ou sobrescrever história não autorizada.
- **Aceite:** docs coerentes PT/EN, sanitização, testes executados com resultado registrado, perfil fast, commit autoral, push normal, metadados público e reread de blob/hash pelo consumidor.

## Antes

Inspecionar estado local/remoto, ler fontes selecionadas, registrar fatos e limites no ledger. Confirmar identidade Git antes de commit.

## Durante

Manter o envelope e o ledger; eventos de sessão são append-only, afirmações derivadas carregam fonte, limites e consumidor. Não reivindicar coordenação entre hosts por lock local.

## Depois

Executar testes e perfil de governança, revisar diff e conteúdo público, commit/push sem force, reler GitHub e fechar o ledger com hashes. Um gate indisponível fica `NOT_VERIFIED` com impacto e próximo teste.
