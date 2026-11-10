# ProductCard

Imagem 3:4 sobre `surface-tile`, nome e preço na mesma linha em `body-sm`, e embaixo os tamanhos disponíveis ou as cores — o card do preset mostra caimento antes do clique.

## Por que é assim

- **Tamanhos no card**, com os esgotados riscados e em `ink-muted`: vem da By Malene Birger. Risco + cor, nunca só cor.
- **Grid quase colado** (`space-gutter`, 4px) e imagem sem borda nem raio.
- **Badge** em `surface` sobre a imagem, só para *New* e *Sale*. Nada de "Only 2 left" — urgência falsa reprova.
- Segunda imagem no hover (desktop).

## Mapa Shopify

- Snippet `product-card`; configuração `Card details`: *Sizes* (Moda) / *Swatches* / *Dimensions* (Móveis).
- Preço: `variant.price`, comparativo, `price_varies` ("From $190"), preço unitário quando existir (requisitos).
- Tamanhos vêm da opção cujo nome o lojista indicar (setting `Size option name`, default "Size").
- Swatches: `swatch.color` e `swatch.image` (requisito).

## Regras

- O nome nunca trunca (requisito). Quebra em duas linhas se precisar.
- Preço de venda em `accent`; preço antigo riscado em `ink-muted`.
- Proporção da imagem é setting do lojista (3:4 padrão, 4:5, 1:1) e o grid não pode quebrar com proporções mistas.
