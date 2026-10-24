# Aglaia Studio — instruções do repositório

## Entrada e limites

1. Leia `docs/ESTADO.md`, o plano da fase ativa e o ledger correspondente em `ops/session-governance/`.
2. Confira branch, alterações, owner e origem antes de escrever. Preserve trabalho existente; nunca force push.
3. Não coloque originais de mídia, material comercial sem autorização, transcrições privadas, caminhos de host, credenciais ou configurações pessoais no repositório.
4. Não instale hooks globais/pessoais nem ative adapters sem ensaio documentado. Não escolha stack/editor fora do envelope da fase.

## Registro

Cada unidade tem run-id próprio e eventos append-only. Registre `fato → evidência → decisão → ação/pendência → consumidor`; lacunas ficam `NOT_VERIFIED`, com impacto e próximo teste. Uma correção posterior é evento novo ou novo run, nunca reescrita de evento publicado.

## Claims e concorrência

`python3 scripts/aglaia.py claim <recurso> --owner <run-id>` cria claim local cooperativo; liberação exige mesmo owner. Claims só cobrem o filesystem local, não protegem contra processos que ignorem o protocolo e não coordenam máquinas remotas. Claim vencido não é removido automaticamente: inspecione estado e reconcilie explicitamente.

## Verificação e fechamento

- Mudanças documentais comuns: `python3 scripts/aglaia.py verify --profile fast`.
- Scripts, governança, proveniência ou claims: `impact` e `python3 -m unittest discover -s tests -v`.
- Release/fase: `full`, incluindo reler o consumidor publicado.

Distinguir documentação/configuração, teste local, ensaio de harness, integração real e aceite humano. Não declarar uma camada como validada por outra.
