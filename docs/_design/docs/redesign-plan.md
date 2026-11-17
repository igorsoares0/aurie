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
| 1. Maquetes que faltam 🟡 | Feitas em 2026-11-17 (coleção em índice e em pranchas, carrinho, busca, home e coleção no celular); falta a revisão do Igor | 2–3 dias |
| 2. Fundação | Tokens, `critical.css`, tipografia, settings, cabeçalho, rodapé | 2–3 dias |
| 3. Produto | `main-product`, blocos, cotas, variantes em tabela, ficha | 3–4 dias |
| 4. Coleção, busca, carrinho | Índice, filtros, busca, gaveta e página do carrinho | 3–4 dias |
| 5. Home | Seções revistas e cortadas | 3–4 dias |
| 6. Templates secundários | Blog, artigo, página, 404, senha, cartão-presente | 2 dias |
| 7. Presets e demos | Três presets, metafields nas lojas (números, medidas, códigos), conteúdo, screenshots | 2–3 dias |
| 8. QA e envio | Lighthouse, acessibilidade, teclado, navegadores reais, Theme Check, docs, listing | 3 dias |

Total: **3 a 4 semanas** de trabalho, o que coincide com a janela de 30 dias antes do reenvio.

## Regras para não repetir erros

- Não reenviar antes de o redesenho estar completo e testado em todos os templates e no celular.
- Cada componente novo é testado com os três presets e com fotos de proporções diferentes.
- A home não pode ser a única tela forte: produto, coleção, carrinho e busca recebem o mesmo cuidado.
- Antes de reenviar, refazer a pesquisa de concorrentes na Theme Store.
