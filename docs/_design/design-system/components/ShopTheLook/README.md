# ShopTheLook

Imagem de look com pontos clicáveis e, ao lado, a lista das peças com tamanho escolhido, total e um botão que adiciona o look inteiro ao carrinho.

## Por que é assim

- O "set" da Cénée — várias peças, um total, um botão — aplicado a roupa. É o principal diferencial funcional do preset frente a Blum e Prestige, que mostram o look mas mandam comprar peça por peça.
- Ponto ativo invertido (`ink` sobre `surface`) e sincronizado com a linha da lista.

## Mapa Shopify

- Seção `Shoppable image` (compartilhada com o preset Móveis) com blocos `Product hotspot` (product picker + posição horizontal e vertical em %).
- Variante `Layout`: *Image with product list* (Moda) / *Image with floating card* (Móveis).
- "Add the look to bag" usa a Cart API do próprio tema com vários itens numa chamada. É nativo, não é app.
- Cada linha tem seletor de tamanho; produto esgotado sai do total e mostra "Sold out" em `error`.

## Regras

- Máximo de 4 pontos por imagem.
- Pontos são botões com `aria-label` do produto, alvo de 28px.
- Sem desconto automático de "look completo" no tema: desconto é do lojista, via Shopify Discounts.
