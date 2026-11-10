# Pacote para o Claude Code — tema multi-nicho

1. Crie o repositório do tema com `shopify theme init` (Skeleton).
2. Descompacte este pacote **na raiz do repositório**. Fica a pasta `_design/`.
3. **Não apague o `CLAUDE.md` que veio com o Skeleton.** Acrescente esta linha no topo dele:

       @_design/PROJECT.md

   O Claude Code carrega os dois: as convenções da Shopify (do arquivo original) e as regras deste projeto.
4. Abra o Claude Code na raiz e peça: "Comece a Fase 0 do plano."
5. Na hora de submeter, não envie `_design/` (adicione ao `.shopifyignore`).

Conteúdo de `_design/`:

- `docs/implementation-plan.md` — plano de implementação completo
- `design-system/` — tokens, README (com a seção Responsivo) e componentes
- `screens/desktop/` e `screens/mobile/` — as 24 telas do canvas
- `screens/canvas.json` — índice do canvas
