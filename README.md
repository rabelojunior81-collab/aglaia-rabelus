# Aglaia Rabelus

**Aglaia Studio** é um estúdio desktop local, Mac primeiro, em fase de fundação. A direção inicial é ajudar a compor Reels de joias a partir de coleções de fotos em múltiplos ângulos e vídeos de rotação existentes. O produto ainda não tem editor implementado nem stack escolhida.

Este é um projeto público e full open source, também concebido como material didático para alunos do curso do autor. A fundação não inclui mídia comercial, credenciais, configurações pessoais ou transcrições privadas.

## Estado

Fase 0: proveniência, briefing, governança e verificadores iniciais. A pesquisa de ferramentas está registrada; Remotion, HyperFrames, Higgsfield e outros candidatos continuam sem escolha ou ensaio neste repositório. Nenhuma API paga, assinatura ou crédito de modelo é usado ou presumido gratuito.

## Princípios

- Organização é lindo.
- Antes, durante e depois, sempre.
- Cada um é um, todos são um.
- Evidência antes de claim. Distinguir documento, configuração, teste local, ensaio de harness e aceite humano.
- Toda regra deve apontar um mecanismo verificável ou ser identificada como conduta humana.
- Decisões rotineiras podem ser autônomas dentro do envelope da fase; decisões fora do envelope param para revisão.

## Comece aqui

- [Gênesis e proveniência](docs/origem/GENESIS.md)
- [Briefing do produto](docs/BRIEFING.md)
- [Governança e protocolo Matrix](docs/governanca/METODO-E-GOVERNANCA.md)
- [Estado atual](docs/ESTADO.md)
- [Pesquisa de ferramentas](docs/pesquisa/FERRAMENTAS.md)
- [Roadmap](docs/ROADMAP.md)
- [Plano da Fase 0](docs/fases/fase-0/PLANO.md)
- [Como contribuir](CONTRIBUTING.md)

Para rodar os verificadores portáteis sem dependências externas: `python3 -m unittest discover -s tests -v` e `python3 scripts/aglaia.py verify --profile fast`. Requer Python 3.9+.

## English

Aglaia Studio is a local desktop studio, Mac first, currently in its foundation phase. Its initial direction is helping compose jewelry reels from existing multi-angle photo collections and rotation videos. No editor has been implemented and no technology stack has been selected. The project is public full open source and also intended as educational material. See [the English overview](README.en.md).

## License

The initial foundation is licensed under Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
