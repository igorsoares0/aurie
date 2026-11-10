# Tema multi-nicho — instruções do projeto (importado pelo CLAUDE.md da raiz)

Tema Shopify para a **Theme Store**, com **um código e três presets**: moda feminina (demo "Arvel"), joias (demo "Oriel") e móveis (demo "Sotto"). O objetivo é passar na revisão da Shopify na primeira submissão. O design está fechado; o trabalho aqui é implementar.

## Fontes da verdade (leia antes de escrever código)

| Arquivo | O que é | Quando consultar |
| --- | --- | --- |
| `_design/docs/implementation-plan.md` | Plano em fases (0–6), mapa de seções, blocos, snippets, settings e presets | Sempre. Siga as fases em ordem e só avance quando o "Pronto quando" passar |
| `_design/design-system/tokens.json` | Cores dos 6 esquemas, famílias e escalas de fonte, espaçamento e raios | Ao montar `settings_schema.json`, `settings_data.json` e `critical.css` |
| `_design/design-system/README.md` | Personalidade de cada preset, diferenças estruturais, regra de grid e regras **Responsivo** | Ao decidir layout e comportamento mobile |
| `_design/design-system/components/*` | Header, ProductCard, BuyBox, ShopTheLook, EditorialSplit, CategoryIndex, Footer, Button: preview HTML + README com o mapa para seções, snippets e settings | Ao construir cada componente |
| `_design/screens/desktop/*.dc.html` | 12 telas desktop (1440 px): home, produto, coleção, carrinho × 3 presets | Referência visual e de conteúdo de cada template |
| `_design/screens/mobile/*.dc.html` | 12 telas mobile (390 px), as mesmas páginas | Referência para abaixo de 750 px |

Se o plano e as telas divergirem, **as telas mandam no visual** e **o plano manda na arquitetura**. Na dúvida, pergunte ao Igor antes de inventar.

## Como ler os arquivos `.dc.html`

São mockups de um canvas de design, não código para copiar.

- A marcação fica dentro de `<x-dc>`. `{{nome}}` é um valor calculado no `<script data-dc-script>` do fim do arquivo (`renderVals()`): é lá que estão os dados de exemplo (produtos, preços, tamanhos, textos).
- `<sc-for list="{{x}}" as="i">` é um loop; `<sc-if value="{{x}}">` é condicional. Em Liquid, vire `{% for %}` e `{% if %}` sobre objetos reais da Shopify.
- Os estilos estão **inline só por causa do formato do mockup**. No tema, traduza para classes em CSS com custom properties vindas dos tokens. Nunca leve `style=""` inline para o Liquid.
- `support.js`, `<helmet>` e os links do Google Fonts são do canvas. No tema, as fontes vêm do `font_picker`.
- Textos entre colchetes, como `[SHOWROOM ADDRESS]`, são placeholders.

## Como os presets diferem (resumo — detalhes no plano)

O código é um só. A diferença está em settings globais que aplicam classes no `<body>`:

| Setting | Moda | Joias | Móveis |
| --- | --- | --- | --- |
| `header_layout` | `logo_center_words` | `logo_center_icons` | `logo_left` |
| `card_style` | `portrait` (3:4) | `square` (1:1) | `framed` (card arredondado) |
| `card_details` | `sizes` | `material` | `dimensions` |
| `media_layout` | `grid` (2×2) | `thumbnails_beside` | `thumbnails_below` |
| `corner_style` | `square` | `pill_buttons` | `rounded` (8 px botões, 16 px imagens) |
| `heading_case` | normal | normal + itálico na 2ª metade | `uppercase` |
| Esquemas de cor | Paper, Espresso | Light, Onyx | Linen, Walnut |
| Fontes | Cormorant / Work Sans | Playfair Display / Jost | Barlow Condensed / Barlow |

No mobile, a galeria de produto também muda por preset: Moda rola de lado em 3:4, Joias tem um quadrado grande com miniaturas embaixo e Móveis tem uma foto arredondada com 4 miniaturas. Veja `_design/design-system/README.md` › Responsivo.

## Regras que reprovam na revisão (não negociáveis)

- Base **Skeleton theme** (`shopify theme init`). Nada copiado de Dawn ou Horizon.
- Todas as features obrigatórias da Shopify: variantes com imagem, swatches, preço unitário, impostos, Shop Pay Installments, pickup availability, checkout acelerado, selling plans, descontos automáticos, notas do carrinho, filtros facetados, busca preditiva, gift card, seletores de país e idioma, `<shopify-account>`, blocos `@app` em todas as seções onde fizer sentido, Custom Liquid.
- Lighthouse com média **≥ 60 em performance e ≥ 90 em acessibilidade** (meta interna 75 / 95), em home, coleção e produto de cada preset.
- Nada que pareça app: sem wishlist, sem reviews próprios, sem contadores de urgência falsos ("only 2 left", timers).
- Fontes **só** via `font_picker` (`font_face` + `font_modify` para bold e itálico).
- Mínimo de 4 cores por esquema; todo fundo tem a cor de texto correspondente.
- Textos do editor em **inglês americano, sentence case**, sem "&", sem rótulos numerados ("Layout 1").
- Nomes de preset com 1–2 palavras, sem palavra de indústria; um preset leva o nome do tema. **"Moda", "Joias" e "Móveis" são provisórios** — use-os só nos nomes de pasta de trabalho até o Igor definir os nomes finais.
- `/listings/<preset>/templates` para cada preset, com paridade total entre o preset instalado e o demo.
- Nenhum JSON de template pode apontar para recursos do demo (`shopify://…`, metafields do demo).
- Não enviar `config/markets.json`, Sass, nem CSS/JS minificado.

## Regras de design que o Igor cobra

- **Grid sem buraco:** nenhuma linha termina com um item sozinho ao lado de espaço vazio. Listas de produtos, posts e categorias com quantidade variável rolam de lado. Blocos de 4 quebram em 2+2. No mobile, grades de 2 colunas só com quantidade par.
- **Sem faixas em branco no fim da página:** o rodapé encosta no conteúdo.
- Em Joias, nada inclinado (a etiqueta do editorial é reta).
- Alvos de toque com pelo menos 44 × 44 px; campos com fonte de 15 px ou mais.
- Faixas de largura: **< 750 px** mobile, **750–989 px** tablet, **≥ 990 px** desktop.

## Mapa tela → arquivo do tema

| Tela | Template / seções principais |
| --- | --- |
| `*-Home` | `templates/index.json` (Moda) e `listings/<preset>/templates/index.json`, montados com as 30 seções do plano |
| `*-Produto` | `sections/main-product.liquid` + blocos em `blocks/`; snippets `product-media`, `price`, `swatch`; drawer de guia de medidas |
| `*-Colecao` | `sections/main-collection.liquid` + snippets `product-card`, `facets`, `pagination`; drawer de filtro no mobile |
| `*-Carrinho` | `sections/main-cart.liquid` (página) e o cart drawer em `snippets/drawer` + `assets/theme.js` |

## Como trabalhar

1. Comece pela **Fase 0** do plano e rode `shopify theme check` a cada commit.
2. Construa primeiro com o preset Moda, mas sempre com as settings de assinatura já ligadas. Troque o preset no editor ao fim de cada componente para provar que os três funcionam.
3. JavaScript em ES6 sem build e sem minificar; use Web Components quando houver estado (drawer, variant picker, filtros).
4. Imagens com `image_url` + `srcset` + `loading="lazy"` (exceto o LCP); nada de jQuery ou bibliotecas pesadas.
5. Ao terminar cada fase, atualize os checkboxes em `_design/docs/implementation-plan.md` e resuma o que falta.

## Em aberto (pergunte antes de decidir)

- Nomes finais do tema e dos presets.
- Se todas as seis fontes existem no `font_picker` da Shopify; se faltar alguma, propor a substituta mais próxima.
- Origem das fotos dos demos.
