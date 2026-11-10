# EditorialSplit

Blocos meio a meio de imagem e texto, com o texto em uma linha só (título serifado + link), alternando lados; e a variação em dupla de imagens com legenda pequena embaixo.

## Por que é assim

- **Split Ossou:** a metade de texto fica quase vazia — título em `heading-3` e um link em `body-sm` na mesma linha, centralizados. O vazio é intencional e é o que dá a calma do preset.
- **Dupla Malene Birger:** duas imagens coladas (`space-gutter`) e legenda em `label` abaixo, alinhada à esquerda. Sem texto sobre a imagem.

## Mapa Shopify

- Seção `Image with text` com setting `Layout`: *Split, text centered* (Moda) / *Image left* / *Image right*.
- Seção `Image gallery` (dupla) com legenda por bloco.
- Focal point da imagem respeitado (requisito).

## Regras

- No mobile o split empilha: imagem primeiro, texto embaixo com `space-8` de respiro.
- Título no máximo 4 palavras; link começa com verbo (requisito de botões e ações).
- Nunca texto embutido na imagem do demo (reprova).
