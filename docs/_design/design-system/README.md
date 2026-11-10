# Tema multi-nicho

Um tema Shopify, três presets. Este sistema guarda a **estrutura comum** (os mesmos nomes de token e os mesmos componentes) e os **valores de cada preset** como temas de cor. Os três presets estão preenchidos: **Moda** (`moda-*`), **Joias** (`joias-*`) e **Móveis** (`moveis-*`), todos com os mesmos nomes de token.

> Moda: calma, editorial, caimento em primeiro lugar.

## Preset Moda — personalidade

Marca feminina contemporânea, peças de base bem cortadas, ticket médio, 50 a 150 produtos. A página tem pouca coisa por tela, imagem grande e texto curto. A compra gira em torno de **caimento e tamanho**, mostrados cedo: no card, no menu e na página de produto.

### O que veio de cada referência

| Referência | O que entra | O que fica de fora |
| --- | --- | --- |
| Ossou | Fundo papel quente, tinta café, splits meio a meio com título + link numa linha, utilidades escritas por extenso, wordmark gigante no footer | O ícone flutuante "Aa" de acessibilidade (é app de terceiros) |
| By Malene Birger | Tamanhos no card, grid de imagens quase colado, legendas pequenas em caixa alta sob as imagens, menu com edições curadas, aviso de guia de medidas no carrinho | Wishlist (é funcionalidade de app; proibida no tema) |
| Cénée | Índice numerado de categorias, look/set com total e um botão só | Card flutuante sobre a imagem (fica para o preset Móveis) |
| Jimmy Fairly | Navegação por caimento (Petite, Tall) | — |
| Crafto (print) | Nada visual. Serve de lista do que evitar | Texto gigante vazado, letreiro rolando, logos de marcas famosas, "Black Friday" em imagem |

## Fundamentos visuais

### Cor

Dois esquemas de cor no preset, que viram dois **color schemes** da Shopify:

| Token | Paper | Espresso | Setting Shopify |
| --- | --- | --- | --- |
| `surface` | papel `#f8f5f0` | café `#241a14` | Background |
| `ink` | café `#2a1f18` | creme `#f3ede5` | Text |
| `button` / `button-label` | `ink` / `surface` | `ink` / `surface` | Solid button background / label |
| `control-border` | `#8c7f73` | `#8f8276` | Border |
| `accent` | ferrugem `#8a3f22` | `#e0a07e` | Sale price / Accent |
| `surface-tile` | `#ece7e0` | `#31261e` | Image placeholder background |

São mais de 4 cores e todo fundo tem sua cor de texto (requisito). `accent` aparece no máximo uma vez por altura de tela: preço promocional, sublinhado ativo. `hairline` é só decorativo; bordas de controle usam `control-border`, que passa 3:1.

### Tipografia

- **Títulos:** serifada de alto contraste (`serif`, Cormorant), peso 300–400, nunca bold. Faz o papel das serifadas de Ossou e Malene Birger.
- **Interface e texto:** grotesca discreta (`sans`, Work Sans) em 11–15px. Navegação, botões e legendas em `label`: 11px, caixa alta, espaçamento .08em.
- As duas famílias precisam existir no `font_picker` da Shopify; fonte custom reprova. **A confirmar:** os handles exatos (Work Sans está documentada como `work_sans_n6`; Cormorant precisa ser verificada no seletor do editor). Se Cormorant não estiver na biblioteca, as alternativas a testar são outras serifadas de alto contraste da lista.
- O tema carrega regular, italic, bold e bold italic de cada família via `font_modify` (requisito).

### Layout e espaço

- Margem lateral `space-6` no desktop e `space-4` no mobile; seções separadas por `space-24` (desktop) e `space-16` (mobile).
- Imagens e cards separados por `space-gutter` (4px). O grid quase colado é a marca do preset.
- Tudo quadrado (`radius-none`). Só swatches e hotspots são redondos (`radius-full`).
- Sem sombras. Separação por espaço, e raramente por `hairline`.

### Imagem

- Produto em 3:4 sobre `surface-tile`; editorial em 4:5 ou meio a meio.
- Fotos de estúdio com fundo liso ou locações de arquitetura. Sem texto, preço ou logo dentro da imagem (reprova no demo store).
- Vídeo de caimento na galeria do produto, sem som e em loop.

## Conteúdo e tom

- Inglês americano no tema e no demo (requisito). Títulos curtos: "The fall edit", "Earthy tones". Links começam com verbo: "Shop outerwear", "Explore new washes".
- Nada de urgência: sem "Only 2 left", "12 people viewing", contadores (reprova).
- Nome da loja de demonstração: **Arvel** (provisório, a checar contra marcas existentes).

## Preset Joias — personalidade

> Joias: luminosa, precisa, cada peça com espaço próprio.

Joalheria autoral em ouro e prata, ticket médio-alto, 30 a 80 peças. Fundo quase branco para o metal fazer a cor, muito ar, poucas peças por linha. A compra gira em torno de **material, acabamento e presente**: todo card diz do que a peça é feita, e o site oferece gravação, embalagem e guia de materiais.

### O que veio de cada referência

| Referência | O que entra | O que fica de fora |
| --- | --- | --- |
| Conceito Elsa Peretti | Card com nome serifado e linha de especificação (material e medida), etiqueta de papel sobre a borda da imagem editorial (reta, nunca inclinada), botões em pílula, faixa de serviços com quatro ícones | Nome e marca Tiffany e Elsa Peretti, letras com floreio desenhadas sob medida, filtros dentro da home |
| Conceito "Find the perfect" | Título dividido em duas metades (esquerda e direita), contadores em `joias-label` ("24 pieces"), grid assimétrico | Caixa alta grotesca gigante (fica pesada para joia fina); o losango "Details" no hover |
| Tashola | Fundo claro quente, grade 2×2 de retratos com legenda em serif + itálico ("Rings *Collection*"), bloco de imagem grande com 4 produtos ao lado | Ícones de pagamento soltos na home |

### Como Joias difere de Moda

| Sistema | Moda | Joias |
| --- | --- | --- |
| Header | Utilidades em palavras, menu em linha | Ícones, logo central, segunda linha com as categorias |
| Card | 3:4, nome em sans, tamanhos | 1:1 em tile, nome em serif, linha de especificação, swatches de metal |
| Mídia | Grid colado (4px), splits meio a meio | Muito ar (24px entre peças), retratos 2×2 com legenda sobre a imagem, etiqueta de papel |
| Botões | Quadrados | Pílula (`radius-full`) |
| Footer | Claro com wordmark gigante | Esquema Onyx (escuro), sem wordmark |
| Ritmo | `space-24` entre seções | `space-32` entre seções, margem `space-16` |

### Tipografia de Joias

Playfair Display nos títulos e nos nomes de peça, com itálico só na segunda metade de uma frase; Jost no texto e na interface. **A confirmar** no `font_picker` da Shopify, como as fontes de Moda.

## Preset Móveis — personalidade

> Móveis: sólida, quente, feita para durar — e clara sobre medidas e entrega.

Marca de móveis em madeira maciça e estofados, ticket alto, 80 a 200 produtos. Ambientes grandes com cantos arredondados, títulos condensados em caixa alta e uma madeira (carvalho) usada como painel inteiro. A compra responde a três dúvidas: **cabe no meu espaço, de que é feito, quando chega.** Todo card mostra as medidas; a home explica material, fabricação e entrega.

### O que veio de cada referência

| Referência | O que entra | O que fica de fora |
| --- | --- | --- |
| Prabott | Hero inset com cantos arredondados, card arredondado com nome em cima e preço embaixo, grade de ambientes em mosaico (um grande e três menores) | Números inventados ("800+"), "Join membership", o wordmark gigante no footer (é de Moda) |
| Ditre Italia | Swatches de tecido sob cada produto, chips de categoria (All, Sofas, Armchairs…), produto recortado sobre o fundo | Círculo decorativo sobre o hero, letra inicial em itálico |
| Cira Pro | Título condensado dividido com uma régua no meio ("SIGNATURE —— PIECES"), seção escura de fabricação em quatro etapas | Wordmark gigante, a seção de designers (exige fotos de pessoas reais) |
| Arbora | Imagem de ambiente com pontos e card flutuante do produto, painel "Built from solid oak" em cor de madeira, lista de garantias (madeira maciça, garantia, teste em casa), depoimento | Estrelas de avaliação (dependem de app), botão redondo com seta como padrão |
| Furniseat | Navegação por cômodo (Living room, Dining room, Entryway) | Títulos em serifada condensada, abas "Special price" |

### Como os três presets diferem

| Sistema | Moda | Joias | Móveis |
| --- | --- | --- | --- |
| Header | Logo central, utilidades em palavras | Logo central, ícones, categorias numa 2ª linha | Logo à esquerda, menu por cômodo no centro, ícones |
| Título | Serifada leve | Serifada com itálico | Grotesca condensada em caixa alta, dividida por régua |
| Card | 3:4 com tamanhos | 1:1 com material | Card arredondado com nome, medidas, tecidos e preço |
| Imagem | Quadrada, colada | Quadrada, com ar | Cantos de 16px, hero recuado da borda |
| Botões | Quadrados | Pílula | Cantos de 8px |
| Cor | Rust pontual | Ouro pontual | Carvalho como painel inteiro |
| Footer | Claro, wordmark | Escuro | Linen, com título condensado |

### Tipografia de Móveis

Barlow Condensed (600) nos títulos, sempre em caixa alta; Barlow no texto. Medidas sempre como `W × D × H cm`. **A confirmar** no `font_picker` da Shopify.

## Regra de grid (vale para todos os presets)

Nenhuma linha termina com um item sozinho e um vão em branco ao lado. Listas de produtos, posts e categorias ficam numa linha só e rolam na horizontal quando não cabem; blocos de quatro (retratos, serviços) quebram em pares: 4, depois 2+2, depois 1.

## Responsivo

Três faixas, as mesmas da Shopify: **celular abaixo de 750 px**, **tablet de 750 a 989 px**, **desktop a partir de 990 px**. As telas mobile do canvas foram desenhadas em 390 px.

O que vale para os três presets no celular:

- **Menu:** gaveta em tela cheia. Moda lista as categorias em serifa grande; Joias soma o guia de materiais; Móveis mostra os ambientes como cards com foto.
- **Listas:** produtos, posts e categorias rolam de lado (cards de 150 a 300 px, com snap). Grades em 2 colunas só com quantidade par: 4 ou 8 itens. Quantidade ímpar vira rolagem horizontal.
- **Página de produto:** a galeria muda por preset (Moda rola de lado em 3:4; Joias tem quadrado grande com miniaturas embaixo; Móveis tem foto arredondada com 4 miniaturas). Uma barra fixa de "Add to bag" com a variante e o preço aparece quando o botão principal sai da tela.
- **Coleção:** barra de filtro e ordenação fixa no topo. O filtro abre em tela cheia (Moda e Móveis) ou de baixo para cima (Joias). Moda e Joias usam grade de 2 colunas; Móveis usa um card por linha, com medidas.
- **Carrinho:** o resumo vem abaixo dos itens e o total com "Check out" fica fixo no rodapé da tela.
- **Rodapé:** os menus viram sanfonas.
- **Toque:** todo alvo tem pelo menos 44 × 44 px; campos usam fonte de 15 px ou mais, para o iOS não dar zoom.

## Componentes

Os componentes de assinatura do preset Moda: **Header**, **ProductCard**, **BuyBox**, **ShopTheLook**, **EditorialSplit**, **CategoryIndex**, **Footer** e **Button**. Cada um traz no seu README o mapa para seções, snippets e settings da Shopify.

## Próximos passos

1. Levar tokens, componentes e as telas do canvas (desktop e mobile) para o Claude Code.
2. Montar o tema sobre o Skeleton seguindo o plano de implementação.
