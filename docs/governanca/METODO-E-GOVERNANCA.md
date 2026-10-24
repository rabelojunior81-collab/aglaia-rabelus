# Método e governança — Rabelus Matrix Protocol (inicial)

## Regras e mecanismo

| Regra | Mecanismo nesta fundação | Alcance / limite |
|---|---|---|
| Antes, durante e depois | Plano de fase e ledger append-only | Ledger registra a sessão deste workspace; não garante comportamento de todo harness |
| Evidência antes de claim | `session start/event/close`, registro hash e perfis `verify` | Evidência local/Git; não prova aceitação humana nem efeito externo |
| Cada sessão é autora do próprio evento | Diretório `ops/session-governance/<run>/`; caminho exclusivo por run | Convenção e CLI cooperativa; usuário local pode editar arquivo arbitrariamente |
| Claims de recurso | Lock por criação atômica de diretório em `.aglaia/claims/` com PID/metadados e expiração | Só checkout/filesystem local, escritores cooperantes; não coordena hosts nem resiste a processos maliciosos |
| Continuidade | Evento JSONL, estado derivável e hashes | Estado pode ser reconstruído dos eventos; ainda não há merge automático |
| YOLO por fase | Envelope de objetivo/escopo/decisões/recursos/parada/aceite | Autonomia rotineira dentro do envelope; fronteiras externas seguem humanas |
| Verificação proporcional | `fast`, `impact`, `full`; CI sempre roda governança + testes | CI deste repositório; nenhum adapter de harness está ativado |

## Fluxo

**Antes:** conferir owner, branch, alterações e fontes; sincronizar de forma fast-forward conforme o checkout; criar sessão com envelope e run-id.

**Durante:** registrar `fato → evidência → decisão → ação/pendência → consumidor`; usar `NOT_VERIFIED` quando fonte/ensaio faltar. Claims locais cercam escrita cooperativa e expiram; incerteza não autoriza repetir efeito externo.

**Depois:** conferir testes apropriados, alterações e artefatos afetados, fechar sessão com resultado e evidência, publicar e reler consumidores quando o escopo incluir publicação.

## Perfis

- **fast:** lint de whitespace/conteúdo sensível básico e consistência de metadados; cada commit local.
- **impact:** fast + testes unitários + integridade de eventos, ledger e links internos; mudanças de scripts/governança/proveniência.
- **full:** impact + inventário total de docs/licença/links/artefatos e validação pública de release; fase ou release. CI não roda matriz completa nem ensaios caros.

Gatilho desconhecido ou mudança com efeito externo sobe para `impact` e avaliação humana. Um teste não substitui outro tipo de prova.

## Adapters por harness

A pasta `matrix/adapters/` registra configuração/capacidade desejada. Adapters permanecem `NOT_VERIFIED` e inativos até ensaio específico documentado; nenhum hook pessoal/global é instalado. A existência de instrução ou arquivo de configuração não prova execução. Compatibilidade Codex é descrita como alvo futuro, não validada nesta fundação.
