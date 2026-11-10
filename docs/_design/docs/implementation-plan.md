# Plano de implementação — tema multi-nicho

Oct 19, 2026 · @igor

## Resumo

Um código só, partindo do [Skeleton theme](https://github.com/Shopify/skeleton-theme), com três presets que mudam em três camadas: **valores** (cores e fontes), **variantes** (os quatro sistemas de assinatura escolhidos por setting) e **templates** (cada preset traz os seus em `/listings`). Nada de CSS ou seção duplicada por preset.

- **Base:** Skeleton + Shopify CLI (`shopify theme init`, `shopify theme dev`). Theme blocks na pasta `blocks/`, CSS por `{% stylesheet %}` e um `critical.css`.
- **Tokens:** o design system Tema multi-nicho vira CSS custom properties alimentadas por settings: color schemes, `font_picker` e alguns `select`.
- **Assinatura por variante:** header, card, galeria e forma (raio dos botões e imagens) são `select` globais que aplicam classes modificadoras. Cada preset grava sua combinação em `settings_data.json`.
- **Ordem:** fundação → templates obrigatórios → seções → presets → qualidade → demo stores → submissão. As features obrigatórias vêm antes das seções bonitas, porque são o que reprova.
- **Estimativa:** 7 fases; o esforço maior está nas fases 2 e 3.

## Como um tema vira três presets

O código é o mesmo para os três; o que muda é o que cada preset grava nas settings e nos templates.

| Camada | Onde vive | Moda | Joias | Móveis |
| --- | --- | --- | --- | --- |
| Cores | `color_scheme_group` em `settings_schema.json` | Paper, Espresso | Light, Onyx | Linen, Walnut |
| Fontes | `font_picker` (títulos, texto) | Cormorant / Work Sans | Playfair Display / Jost | Barlow Condensed / Barlow |
| Header | `select` `header_layout` | Logo central, utilidades em palavras | Logo central, ícones, categorias na 2ª linha | Logo à esquerda, menu central |
| Card de produto | `select` `card_style` | Retrato 3:4 com tamanhos | Quadrado 1:1 com material | Card arredondado com medidas |
| Galeria do produto | `select` `media_layout` | Grade 2×2 | Imagem grande + miniaturas na lateral | 16:10 + miniaturas embaixo |
| Forma | `select` `shape` | Quadrado | Pílula nos botões | Arredondado (8px botões, 16px imagens) |
| Título | `select` `heading_case` + `checkbox` `heading_split_rule` | Normal | Normal, itálico na 2ª metade | Caixa alta, régua no meio |
| Footer | settings da seção `footer` | Wordmark gigante | Esquema Onyx | Card linen |
| Templates | `/listings/<preset>/templates/*.json` | Home de 12 blocos | Home de 11 blocos | Home de 12 blocos |

As classes modificadoras ficam no `<body>` (por exemplo `card--portrait`, `shape--pill`), e cada componente lê a classe. Assim um lojista pode trocar o card de joias para o de móveis sem quebrar nada, e o revisor vê que a diferença entre presets é estrutural.

## Estrutura de arquivos

Parte do Skeleton e acrescenta só o que os requisitos e o design pedem. Nomes de arquivo em inglês, porque viram rótulos no editor.

```
.
├── assets/
│   ├── critical.css            tokens → CSS custom properties, reset, tipografia
│   ├── theme.js                cart drawer, variant picker, filtros (ES6, sem minificar)
│   └── icons/…                 SVG de ícones em linha
├── blocks/                     theme blocks reutilizáveis (price, title, swatches, fit-notes…)
├── config/
│   ├── settings_schema.json    cores, fontes, assinatura, carrinho, redes sociais, theme_info
│   └── settings_data.json      "presets": Moda (atual), Joias, Móveis
├── layout/
│   ├── theme.liquid            lang, page_image, SEO, Open Graph, classes de assinatura no <body>
│   └── password.liquid
├── locales/
│   ├── en.default.json
│   └── en.default.schema.json  todos os rótulos do editor (inglês americano, sentence case)
├── sections/
│   ├── header-group.json · footer-group.json
│   ├── main-*.liquid           uma por template (product, collection, cart, search, blog…)
│   └── *.liquid                as 30 seções de conteúdo
├── snippets/                   product-card, price, swatch, media, pagination, facets…
├── templates/                  JSON do preset principal (Moda) + gift_card.liquid
└── listings/
    ├── moda/templates/*.json
    ├── joias/templates/*.json  + sections/header-group.json, footer-group.json
    └── moveis/templates/*.json + sections/header-group.json, footer-group.json
```

- O nome real de cada pasta em `/listings` segue o nome final do preset (ver a pergunta em aberto no fim).
- Não enviar `config/markets.json`, Sass, nem CSS/JS minificado (requisitos).

## Configurações globais (`settings_schema.json`)

Cada grupo abaixo vira uma aba de Theme settings, com rótulos em inglês na terminologia da Shopify.

| Grupo no editor | Settings | De onde vem no design system |
| --- | --- | --- |
| Colors | `color_scheme_group` com Background, Text, Muted text, Tile background, Border, Accent, Solid button background, Solid button label; 2 esquemas por preset | `surface`, `ink`, `ink-muted`, `surface-tile`, `control-border`, `accent`, `button`, `button-label` |
| Typography | `font_picker` Heading font, Body font; `range` Heading scale; `select` Heading style (Normal, Uppercase) | famílias e estilos de cada preset |
| Layout | `range` Page margin, Section spacing; `select` Grid gap (Tight, Airy) | `space-6`/`space-16`, `space-24`/`space-32`, `space-gutter`/`space-6` |
| Shape | `select` Corner style (Square, Rounded, Pill buttons) | `radius-none`, `radius-sm` + `radius-md`, `radius-full` |
| Product cards | `select` Card style (Portrait, Square, Framed); `select` Card details (Sizes, Material, Dimensions); `checkbox` Show second image on hover | os três cards |
| Product media | `select` Gallery layout (Grid, Thumbnails beside, Thumbnails below) | as três galerias |
| Cart | `select` Cart type (Drawer, Page); `checkbox` Show cart note; `checkbox` Show two-size reminder | carrinhos |
| Social media | `text` por rede (vazios por padrão, requisito) | — |
| Favicon | `image_picker` | requisito |

Regras do editor que a revisão cobra: todo fundo com cor de texto correspondente, mínimo de 4 cores, fontes só via `font_picker` carregando bold e italic com `font_modify`, nada de "&", nada de rótulos numerados ("Layout 1").

## Mapa de seções, blocos e snippets

11 seções de template, 18 seções base e 12 de nicho — as mesmas do plano de seções, agora com nome de arquivo.

### Seções de template (uma por página obrigatória)

| Arquivo | Template | O que precisa cumprir |
| --- | --- | --- |
| `main-product.liquid` | product | Tudo em blocos, `@app` e Custom Liquid; variantes, swatches, imagem por variante, preço unitário, impostos, Shop Pay Installments, retirada, checkout acelerado |
| `main-collection.liquid` | collection | Título, descrição e imagem; filtros facetados, ordenação, paginação, estado vazio, "From" e Sale |
| `main-list-collections.liquid` | list-collections | `featured_image`, paginação |
| `main-cart.liquid` | cart | Linhas completas, quantidade, notas, selling plans, descontos automáticos, checkout acelerado, estado vazio |
| `main-search.liquid` + `predictive-search` snippet | search | Produtos, páginas e artigos (`object_type`), estado vazio, paginação |
| `main-blog.liquid` · `main-article.liquid` | blog · article | `excerpt_or_content`, `published_at`, comentários paginados |
| `main-page.liquid` · `contact-form.liquid` | page · page.contact | Template alternativo de contato |
| `main-404.liquid` · `main-password.liquid` | 404 · password | Mensagem e saída; logo e campo de senha |
| `gift_card.liquid` | gift card | Código, QR ≥ 120px, Apple Wallet, logo |

### Seções de conteúdo

- **Base (18):** `announcement-bar`, `header`, `footer`, `slideshow`, `image-banner`, `image-with-text`, `rich-text`, `featured-collection`, `collection-list`, `featured-product`, `multicolumn`, `testimonials`, `video`, `blog-posts`, `collapsible-content`, `newsletter`, `logo-list`, `custom-liquid`.
- **Nicho (12):** `shoppable-image`, `lookbook`, `collection-tabs`, `size-guide`, `material-guide`, `detail-gallery`, `craft-process`, `gift-guide`, `shop-by-room`, `product-comparison`, `fabric-library`, `delivery-and-assembly`.

### Blocos de tema (`blocks/`)

`title`, `price`, `installments`, `variant-picker`, `quantity`, `buy-buttons`, `pickup-availability`, `collapsible-tab`, `fit-notes`, `size-guide-link`, `engraving-field`, `dimensions`, `lead-time`, `complementary-products`, `custom-liquid`, `text`, `button`.

### Snippets

`product-card` (lê `card_style`), `price`, `swatch`, `product-media` (lê `media_layout`), `facets`, `pagination`, `image` (srcset + lazy + focal point), `icon`, `drawer`.

## Presets

Cada preset é um bloco em `settings_data.json` mais uma pasta em `/listings`. Instalar um preset tem que reproduzir o demo dele (layout, cores e tipografia).

```json
{
  "current": "Moda",
  "presets": {
    "Moda":   { "header_layout": "logo_center_words", "card_style": "portrait", "card_details": "sizes",
                "media_layout": "grid", "corner_style": "square", "heading_font": "cormorant_n3", "…": "…" },
    "Joias":  { "header_layout": "logo_center_icons", "card_style": "square", "card_details": "material",
                "media_layout": "thumbnails_beside", "corner_style": "pill_buttons", "…": "…" },
    "Móveis": { "header_layout": "logo_left", "card_style": "framed", "card_details": "dimensions",
                "media_layout": "thumbnails_below", "corner_style": "rounded", "heading_case": "uppercase", "…": "…" }
  }
}
```

Os nomes "Moda", "Joias" e "Móveis" acima são provisórios: a Shopify proíbe nome de indústria, e o preset principal leva o nome do tema.

### Templates de cada preset

| Template | Moda | Joias | Móveis |
| --- | --- | --- | --- |
| `index.json` | 12 blocos (lookbook, shop the look, journal) | 11 blocos (ícones, metais, presentes) | 12 blocos (cômodos, card flutuante, carvalho) |
| `product.json` | Fit notes, size guide, complete the look | Metal, gravação, ring size guide | Tamanho, tecido, pés, "Will it fit?", prazo |
| `collection.json` | Filtro em barra, grade de 4 | Filtro lateral, grade de 3, load more | Chips + gaveta, grade de 3 |
| `cart.json` | Aviso de dois tamanhos | Embrulho, mensagem do cartão | Notas de entrega, prazo por item |
| `page.contact.json`, `search.json`, `blog.json`, `article.json`, `404.json`, `list-collections.json`, `password.json` | Mesmas seções, valores do preset | idem | idem |

Nenhum JSON pode citar recursos do demo (`shopify://…`, metafields próprios do demo store) — o lojista instala numa loja vazia.

## Plano em fases

Cada fase termina com um critério de pronto verificável. Só se avança quando ele passa.

### Fase 0 — Ambiente

- [ ] `shopify theme init` com o Skeleton; repositório Git novo (não reaproveitar o Aurelia)
- [ ] Loja de desenvolvimento + uma client transfer store por preset para os demos — dev stores prontas: `testetemply` (Joias) e `aurie-moda` (Moda); faltam Móveis e as client transfer stores da submissão
- [x] Theme Check e GitHub Actions do Skeleton ligados (`.github/workflows/ci.yml`; Theme Check sem ofensas em 2026-10-26)

**Pronto quando:** `shopify theme dev` roda e o Theme Check passa sem erros.

### Fase 1 — Fundação

- [x] `settings_schema.json` completo (seção anterior) e `critical.css` com os tokens como variáveis
- [x] Classes de assinatura no `<body>` a partir das settings
- [x] `theme.liquid`: `lang`, SEO, Open Graph, `page_image`, `content_for_header` intacto
- [x] Header e footer em section groups, com as três variantes de layout, `<shopify-account>`, seletores de país e idioma, menu multinível

**Pronto quando:** trocar o preset no editor muda cores, fontes, header, forma e footer, sem recarregar código.

### Fase 2 — Templates obrigatórios

- [x] Produto completo com todos os blocos e as três galerias
- [x] Coleção com facetas, ordenação, paginação e estado vazio; busca com busca preditiva
- [x] Carrinho (página e drawer) com notas, selling plans, descontos e checkout acelerado
- [x] Blog, artigo, página, contato, 404, senha, lista de coleções, gift card

**Pronto quando:** cada item do checklist de features da Shopify funciona na loja de desenvolvimento com produtos reais de teste.

### Fase 3 — Seções

- [x] 18 seções base com presets de seção e placeholders da Shopify
- [x] 12 seções de nicho
- [x] Rótulos revisados contra a terminologia e o guia de texto

**Pronto quando:** as três homes do canvas podem ser montadas só com o editor, sem código.

### Fase 4 — Presets

- [x] Os três blocos em `settings_data.json`
- [x] `/listings/<preset>/templates` e section groups de cada um, espelhando o canvas

**Pronto quando:** instalar cada preset numa loja vazia dá a mesma cara do demo.

### Fase 5 — Qualidade

- [ ] Lighthouse ≥ 60 performance e ≥ 90 acessibilidade (meta interna 75 / 95) em home, coleção e produto dos três presets
- [ ] Teclado, foco visível, contraste, alvos ≥ 24px, HTML válido
- [ ] Navegadores e webviews (Instagram, Facebook, Pinterest)

**Pronto quando:** as medições estão anotadas por preset e todas passam.

**Referência (2026-10-28, mobile, mediana de 3 rodadas, tema demo em modo de pré-visualização):**

| Preset | Página | Performance | Acessibilidade |
| --- | --- | --- | --- |
| Joias | Home / Coleção / Produto | 91 / 94 / 90 | 97 / 92 → 97 / 93 → 97 |
| Moda | Home / Coleção / Produto | 74 / 77 / 57 → 91 | 97 / 92 → 97 / 93 → 97 |

- Corrigido após a medição: rótulo de ordenação escondido com `display: none` (`select-name`) e contraste do botão "Buy it now" (`color-contrast`).
- O `frame-title` restante é o iframe da barra de pré-visualização da Shopify, não do tema. A barra também pesa na performance: refazer a medição final com o tema publicado na loja demo.
- Produto de Moda investigado: a nota 57 foi oscilação da máquina (WSL) e não do tema. Sem throttling a página tem uma única tarefa longa (59 ms); os scripts embutidos são todos da plataforma (iguais aos de Joias); a galeria carrega só a 1ª imagem em `eager`/`fetchpriority=high` e as demais em `lazy`, com `sizes` corretos. Nova mediana de 3 rodadas com a máquina estável: 91. Na medição final, conferir o `benchmarkIndex` de cada rodada e descartar as que ficarem muito abaixo de ~1000.

### Fase 6 — Demos e submissão

- [ ] Três demo stores com catálogo realista, fotos licenciadas e Bogus Gateway
  - Joias (`testetemply`, tema "Oriel demo"): 24 produtos + gift card, 76 imagens, swatches de metal, 8 coleções, páginas, blog, menus. Falta no admin: nome da loja, políticas (`docs/_design/demo-photos/joias/policies.md`), 2º mercado/idioma, Bogus Gateway, filtros no Search & Discovery
  - Moda (`aurie-moda`, tema "Arvel demo"): 24 produtos, 72 imagens, swatches de cor, 11 coleções, páginas, blog, menus. Falta no admin: os mesmos itens de Joias (políticas em `moda/policies.md`) e ativar cartões-presente
  - Móveis: demo completo em 2026-10-28 na loja `aurie-moveis` (tema "Sotto demo" 189565075609, não publicado): 24 produtos, 93 imagens, 6 swatches, 9 coleções, 7 páginas, blog com 3 artigos, 3 menus. Mesas e escrivaninhas ficaram sem swatch (a Shopify não aceita swatch de cor nessas categorias)
  - Fluxo e ferramentas: `docs/_design/demo-photos/tools/` (`demo_images.py`, `shopify_import.py`, `build_demo_theme.py`). Os templates do repositório ficam sem referências ao demo; só a cópia em `<preset>/.theme-build` tem
- [ ] Documentação pública com FAQ, formulário de suporte com autoresposta
- [ ] Nomes finais, listing por preset com screenshots, versão 1.0.0 e release notes

**Pronto quando:** o checklist de pré-submissão do documento de requisitos está todo marcado.

## Testes, demo stores e submissão

| O quê | Como | Quando |
| --- | --- | --- |
| Erros de código e terminologia | Theme Check (já vem no Skeleton) | A cada commit |
| Performance e acessibilidade | Lighthouse em home, coleção e produto, desktop e mobile, com a [loja de benchmark](https://shopify.dev/docs/storefronts/themes/best-practices/performance/testing-for-performance) da Shopify | Fim das fases 2, 3 e 5 |
| Acessibilidade fina | Navegação só com teclado, leitor de tela, contraste das seis cores de esquema | Fase 5 |
| Features obrigatórias | Produtos de teste cobrindo cada caso: variante com imagem, esgotado, promoção, preço unitário, assinatura, gift card | Fase 2 |
| Paridade preset × demo | Instalar cada preset numa loja limpa e comparar com o demo | Fase 4 |
| Navegadores | Safari, Chrome, Firefox, Edge, Safari iOS, Chrome Android, Samsung Internet e webviews sociais | Fase 5 |

**Demo stores:** uma client transfer store por preset, com catálogo do tamanho que a tag de catálogo promete, fotos licenciadas sem texto embutido, nenhum app e Bogus Gateway ligado.

**Submissão:** pelo Partner Dashboard, com listing por preset, documentação, contato de suporte, versão 1.0.0 e release notes. Reenviar sem corrigir o motivo de uma rejeição pode suspender a conta.

### Perguntas em aberto

- [ ] Nome do tema e dos três presets (verificar contra a Theme Store e outras plataformas)
- [x] Confirmar no `font_picker` que Cormorant, Work Sans, Playfair Display, Jost, Barlow e Barlow Condensed existem; trocar o que faltar
- [x] Origem das fotos dos três demos (produção própria ou banco com licença) — geradas por IA na Replicate (Seedream 5 Lite para catálogo, Nano Banana Pro para banners), com modelo, prompt e ID de cada imagem registrados em `<preset>/images/manifest.json`. Confirmar com a equipe de revisão da Theme Store que imagens de IA são aceitas
- [ ] Rótulos exatos de indústria e tamanho de catálogo no formulário atual
