# BuyBox

Galeria em grade 2×2 colada à esquerda e, à direita, título serifado, preço, cor, tamanhos em botões quadrados, guia de medidas, nota de caimento, add to bag, checkout acelerado e retirada.

## Por que é assim

- **Galeria em grade**, não carrossel: a cliente vê frente, costas, vídeo de caimento e detalhe sem clicar.
- **Nota de caimento** em `surface-tile` logo abaixo dos tamanhos: altura da modelo, tamanho usado e conselho de caimento. É o "fit first" do preset.
- **Tamanho esgotado:** risco + borda tracejada + `ink-muted`, e continua focável com `aria-disabled`.
- **Aviso de dois tamanhos** (Malene Birger): se a cliente adiciona o mesmo item em dois tamanhos, o carrinho sugere o guia de medidas.

## Mapa Shopify

- Seção `main-product` com tudo em blocos (requisito): `Title`, `Price`, `Installments` (Shop Pay Installments), `Variant picker` (style *Buttons*, swatches por `swatch.color`/`swatch.image`), `Size guide` (abre página ou drawer), `Fit notes` (texto ou metafield conectado pelo lojista), `Buy buttons` (checkout acelerado ligado por padrão, cores da marca intocadas), `Pickup availability`, `Collapsible tab`, `@app`, `Custom Liquid`.
- `cart.taxes_included` exibe "Taxes included." (requisito).
- Imagem da variante aparece ao selecionar a variante (requisito).

## Regras

- O título nunca trunca.
- Botões de tamanho com 44px de altura mínima.
- O preço atualiza junto com o preço comparativo e a mensagem de esgotado.
