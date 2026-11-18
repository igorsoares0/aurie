# Redesenho "Ficha técnica" — plano

Criado em 2026-11-17, depois da recusa na triagem de design da Theme Store (primeira recusa de 3; reenvio permitido 30 dias depois da recusa). Maquete aprovada pelo Igor: https://claude.ai/artifact/VmrHqR35sgeA31yA5rph51 (home, produto desktop e mobile em móveis; teste de expressão em roupa e joia).

## Decisões

- 2026-11-17: nome do tema **Caliper** (paquímetro). Livre na Theme Store, WordPress, ThemeForest, Squarespace e Framer na data. O preset de móveis leva o nome do tema.
- 2026-11-17: presets **Caliper** (móveis, principal), **Seam** (roupa) e **Facet** (joia). Checados na Theme Store, WordPress e buscas em ThemeForest, Squarespace, Framer e Webflow. Descartados: Plinth (Framer, Astro), Notch (Webflow), Colophon e Margin (WordPress), Toile (parecido com o preset Etoile), Ledger (empresa).

- 2026-11-17: fontes confirmadas na biblioteca da Shopify (`font_picker`). O tema terá **três** seletores de fonte: títulos, texto e rótulos (monoespaçada).

| Preset | Títulos | Texto | Rótulos |
| --- | --- | --- | --- |
| Caliper | Archivo (`archivo_n6`) | Inter (`inter_n4`) | IBM Plex Mono (`ibm_plex_mono_n4`) |
| Seam | Space Grotesk (`space_grotesk_n6`) | Inter (`inter_n4`) | Azeret Mono (`azeret_mono_n4`), no lugar da JetBrains Mono da maquete, que não existe na biblioteca |
| Facet | Fraunces (`fraunces_n4`, itálico `fraunces_i4`) | Jost (`jost_n4`) | Roboto Mono (`roboto_mono_n4`), no lugar da DM Mono da maquete, que não existe na biblioteca |

## O conceito em uma frase

A loja como um catálogo técnico de objetos bem feitos: **a informação do produto é o design**.

## A assinatura (o que tem que aparecer em toda tela)

| Elemento | O que é | De onde vem o dado |
| --- | --- | --- |
| Numeração de catálogo | "Nº 014" em produtos, cards e breadcrumb | Metafield opcional `custom.catalog_number`; sem ele, não aparece |
| Cotas | Linhas de medida com traços nas pontas, desenhadas nas bordas do quadro da mídia (nunca sobre o objeto, para funcionar com qualquer foto) | Metafields de medida (largura, profundidade, altura, assento; face e aro em joias; altura da modelo em roupas) |
| Figuras | "Fig. 1 — Front" na galeria; miniaturas com legenda | Ordem da mídia + alt text |
| Códigos de opção | "F-01 Linen sand", "C-02 Espresso", "M-01 18k gold" | Prefixo por nome de opção (setting) + posição do valor; sem prefixo, não aparece |
| Opções como tabela | Variantes em linhas de ficha (código, nome, amostra, preço; tamanhos com medidas de corpo ou diâmetro) | Opções do produto + metaobject/tabela de medidas |
| Ficha técnica | Lista definida (dt/dd) com linhas finas | Metafields e bloco de linhas livres |
| Índice | Coleção como tabela comparável, alternando com "pranchas" | Colunas configuráveis por metafield |
| Grade aparente | Linhas de 1 px, rótulos em monoespaçada, papel quente | Tokens do tema |

O que fica de fora de propósito: banner gigante com texto por cima como abertura padrão, tipografia enorme em preto sobre branco puro (marca do Baseline/Austere, o concorrente mais próximo), slideshow, contador e qualquer efeito decorativo sem função.

## O que se reaproveita do Arvel

Praticamente toda a parte invisível:

- Lógica e JS: carrinho e gaveta, itens do carrinho, quantidade, seletor de variantes, galeria (troca por variante, 3D, vídeo), filtros, busca preditiva, recomendações, localização, cartão-presente, senha, meta tags, utilitários de acessibilidade (`.touch-area`, foco), sistema de animação.
- Estrutura de settings (esquemas de cor, `font_picker`, presets via body classes), locales (en, es), regras de Theme Check.
- Lojas demo, catálogos, fotos, scripts de importação e de admin, documentação (estrutura), materiais e processo de submissão.

## O que se refaz

- `critical.css` e tokens (base visual inteira).
- Cabeçalho (navegação numerada) e rodapé (colofão).
- Card de produto → "prancha" com cotas + linha do índice.
- `main-product` e blocos: variantes como tabela, ficha técnica, cotas, "Will it fit?", figuras numeradas, detalhe com pontos.
- `main-collection`: índice em tabela/pranchas, filtros com a mesma linguagem.
- Carrinho e gaveta como "pedido" (linhas numeradas, códigos de opção).
- Busca, blog, artigo, página, 404, senha, cartão-presente, conta: mesma linguagem, mesmo cuidado (a Shopify cobra consistência em todos os templates).
- Seções da home: revisar uma a uma; manter só as que servem ao conceito, redesenhar as que ficam e cortar as genéricas.

## Fases e estimativa

| Fase | Entrega | Estimativa |
| --- | --- | --- |
| 0. Decisões ✅ | Nome Caliper; presets Caliper, Seam, Facet; fontes confirmadas no `font_picker` | feito em 2026-11-17 |
| 1. Maquetes que faltam ✅ | Coleção em índice e em pranchas, carrinho, busca, home e coleção no celular; aprovadas em 2026-11-17 | feito |
| 2. Fundação ✅ | Feita em 2026-11-17: terceira fonte (rótulos), tipografia maior, botões em texto normal, utilitários da ficha (`.index-no`, `.mono`, `.figure-caption`, `.crop-marks`, `.dim`, `.spec-list`, `.data-table`, `.note-box`), cabeçalho com menu numerado e linha de apoio (dois layouts), rodapé colofão. Testado no tema "Caliper dev" (#159524388982, loja Sotto, não publicado) | feito |
| 3. Produto ✅ | Feita em 2026-11-17: grupo de settings "Spec sheet" (metafield do Nº, códigos de opção, metafields de largura e altura, unidade); snippet `option-code`; galeria com "Fig. N" e cotas na primeira imagem; miniaturas numa linha com legenda; título com Nº; preço em monoespaçada com linha forte; seletor de variantes no estilo "rows" (código, amostra, nome, preço); "Will it fit?" como nota tracejada; bloco novo `specification`; abas com rótulo monoespaçado; botão "Add to cart". Testado no Caliper dev: troca de variante por clique e teclado, axe sem violações | feito |
| 4. Coleção, busca, carrinho 🟡 | Feito em 2026-11-17: card de produto reescrito como prancha (Nº no canto, cotas opcionais com a setting `card_dimension_lines`, nome e preço, linha de detalhes) com modo índice (linha de tabela com colunas de metafields, códigos de opção e preço); seletor Índice/Pranchas na barra de filtros, guardado no navegador; coleção com banner-prancha (marcas de corte e legenda); busca com a consulta em tipografia grande e índice; carrinho como pedido (linhas numeradas, Nº, códigos de opção, medidas, prazo, resumo em linhas). Corrigido o campo de preço máximo dos filtros (mostrava 4.75000 com moeda brasileira). Falta conferir o carrinho na tela: a Cloudflare bloqueou os testes automáticos por excesso de acessos | 3–4 dias |
| 5. Home ✅ | Feita em 2026-11-18 (móveis): seções novas "Catalog hero" (texto, fatos, botões e a foto como prancha com marcas de corte e cotas de um produto) e "Product index" (o índice na home); biblioteca de materiais com códigos e painel em tinta escura; home de móveis enxuta (hero, índice, peças em pranchas, materiais, entrega, depoimento), sem a fileira de ícones, o mosaico de ambientes, a imagem com hotspots e o painel do processo. Axe sem violações. As homes de roupa e joia ficam para a fase 7 | feito |
| 6. Templates secundários ✅ | Feita em 2026-11-18: 404 como entrada do índice (código, ficha com o endereço pedido, busca grande); blog como índice de entradas numeradas, uma por linha (nunca deixa buraco); artigo alinhado à esquerda, com a imagem como "Fig. 1"; página com linha forte no título; lista de coleções em linhas numeradas; cartão-presente com marcas de corte e valores em monoespaçada. A página de senha já herdava a linguagem nova. Axe sem violações | feito |
| 7. Presets e demos 🟡 | 2026-11-18, parte de código pronta: presets Caliper (padrão, móveis), Seam (roupa) e Facet (joia); `listings/caliper`, `listings/seam`, `listings/facet`; Seam em "planta" (papel cinza-azulado, tinta marinho, acento azul) e Facet escuro (papel preto, texto creme, dourado), contrastes ≥ 5:1; nova opção "Italic accent in headings" (Facet); homes de Seam e Facet refeitas com Catalog hero + Product index; produtos com variantes em linhas e bloco de ficha técnica; importador com `--metafields` (Nº de catálogo 001–024 nas três lojas e prazo por produto em Sotto). Lojas (2026-11-18): metafields gravados (Nº de catálogo nas três, prazo na Sotto); tema "Caliper dev" não publicado nas três lojas (moda #156366602318, joias #185864257705, móveis #159524388982); coleção "Home page" tirada da loja virtual da Sotto. Conferido no navegador: sem erros, axe sem violações em home e produto de Seam e Facet. Ajustes: índice sem colunas de medida mostra opções e preço (`show_index`), galeria em grade com número ímpar abre com a primeira foto inteira, coleções de Facet em fileira numerada. Falta: publicar o Caliper dev nas lojas demo (troca o tema ao vivo) e decidir sobre a coleção "Home page" das lojas de roupa e joia | em andamento |
| 8. QA e reenvio 🟡 | 2026-11-18, Lighthouse feito (registro em `docs/submission/lighthouse.md`): médias de desempenho 95–97 no desktop e 74–89 no mobile, acessibilidade 100 em tudo; banner da coleção, 1ª foto do produto, imagem do artigo e hero com `preload`. Teclado conferido nos três presets (Tab com foco visível, link de pular, dropdown, busca, carrinho, menu e filtros no celular, guia de medidas: abrem com Enter, prendem o foco, fecham com Esc e devolvem o foco; variantes por setas; índice/pranchas e abas). Celular de Seam e Facet conferido. Documentação reescrita para o Caliper em `docs/theme-docs/` (página nova `spec-sheet.md`), pacote `docs/submission/caliper-docs.zip`; rótulos do editor corrigidos ("Label font" no lugar de "Small caps", dica da Fabric library). Falta: navegadores reais (usuário), GitBook novo, listagem (nome, screenshots, destaques), novo zip sem AGENTS.md, reenviar a partir de 2026-12-17 | em andamento |

Total: **3 a 4 semanas** de trabalho, o que coincide com a janela de 30 dias antes do reenvio.

## Regras para não repetir erros

- Não reenviar antes de o redesenho estar completo e testado em todos os templates e no celular.
- Cada componente novo é testado com os três presets e com fotos de proporções diferentes.
- A home não pode ser a única tela forte: produto, coleção, carrinho e busca recebem o mesmo cuidado.
- Antes de reenviar, refazer a pesquisa de concorrentes na Theme Store.

## Desenvolvimento

- Tema de testes: **Caliper dev** (#159524388982) na loja Sotto, não publicado. Enviar com `python3 docs/_design/demo-photos/tools/build_demo_theme.py moveis` e `shopify theme push --store arvel-sotto-iivcamps.myshopify.com --theme 159524388982 --path docs/_design/demo-photos/moveis/.theme-build` (sem `--allow-live`). Os temas publicados das três lojas demo continuam com o Arvel até a fase 7.
- A versão enviada à Shopify (Arvel 1.0.0) está no commit feito pelo Igor em 2026-11-17, antes da fase 2.
- Fase 7 (2026-11-18): presets renomeados para Caliper, Seam e Facet em `settings_data.json` (`current` = Caliper). Móveis virou o padrão: os templates da raiz são os de Caliper, com cópia em `listings/caliper`; a moda saiu da raiz para `listings/seam`. `theme_name` = Caliper. As lojas demo mantêm as marcas fictícias Arvel, Oriel e Sotto.
- Pendências de conteúdo para a fase 7 (lojas demo): criar o metafield `custom.catalog_number` (o Nº ainda não aparece porque os produtos não têm o dado) e um metafield de prazo por produto. Hoje a linha "Made to order, ships in 6 to 8 weeks" é fixa no template e aparece até nos produtos em estoque, que saem em 5 dias. Esse erro já existia na loja enviada.
- Conteúdo da loja Sotto para a fase 7: a coleção automática "Home page" (1 produto) aparece na lista de coleções; vale despublicá-la ou renomeá-la.

