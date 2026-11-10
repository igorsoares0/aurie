# Header

Barra de anúncio em `bar`, menu à esquerda, wordmark serifado no centro e utilidades escritas por extenso à direita, com o menu aberto organizado por categoria, edição curada e caimento.

## Por que é assim

- **Utilidades em palavras** ("Search", "Account", "Bag (2)") em vez de ícones: vem da Ossou e é uma das marcas visuais do preset. Os outros presets usarão ícones.
- **Menu em três eixos:** categorias, edições curadas (Malene Birger) e caimento (Petite, Tall — a ideia "for small faces" da Jimmy Fairly). O guia de caimento aparece no nível de cima do menu.
- **Painel aberto com duas imagens** de edição, legendas em `label`.

## Mapa Shopify

- Seção `header` dentro do section group do header; `announcement-bar` separada no mesmo grupo.
- Configuração `Utility style`: *Words* (Moda) / *Icons* (outros presets).
- `link_list` com default `main-menu` (requisito).
- "Account" é o componente `<shopify-account>`, visível no desktop e no mobile (requisito).
- Seletores de país e idioma ficam no footer e no drawer mobile.

## Regras

- O wordmark usa a fonte de `heading` em caixa alta, espaçamento .12em. Logo enviado pelo lojista substitui o texto.
- Item ativo: sublinhado, nunca cor.
- Alvo de toque mínimo de 24px (requisito); os links têm 4px de padding vertical.
