# Footer

Newsletter com campo sublinhado, três colunas de links, seletores de país e idioma e o nome da loja em `wordmark` ocupando a largura toda.

## Por que é assim

- O wordmark gigante é comum à Ossou e à By Malene Birger e é a assinatura visual do preset. Nos outros presets ele é desligado.
- Newsletter sem caixa: só uma linha de `control-border` e o botão escrito.

## Mapa Shopify

- Seção `footer` em section group; blocos `Newsletter`, `Menu` (default `footer`, requisito), `Text`.
- Setting `Show store name as wordmark` (ligado no Moda).
- Seletores de país e idioma seguindo as UX guidelines da Shopify (requisito).
- `powered_by_link` sem alteração (requisito); ícones de pagamento, se exibidos, coloridos via `payment_type_svg_tag`.
- Botão Follow on Shop pode entrar como bloco (requisito do tema).

## Regras

- O wordmark é decorativo (`aria-hidden`); o nome real da loja já está no header.
- Nomes longos: o tamanho do wordmark escala para caber em uma linha, mínimo 64px.
