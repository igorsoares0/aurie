# Lighthouse — Caliper redesign

Measured 2026-11-18 with Lighthouse 12.8.2 (headless Chrome 146, default desktop and mobile configs), on the unpublished "Caliper dev" theme of each demo store, preview bar off (`pb=0`), empty cache per run. Theme Store minimum: average performance ≥ 60 and accessibility ≥ 90.

| Preset | Page | Desktop perf | Desktop a11y | Mobile perf | Mobile a11y | Mobile LCP |
| --- | --- | --- | --- | --- | --- | --- |
| Caliper | `/` | 96 | 100 | 85 | 100 | 3.3 s |
| Caliper | `/collections/sofas` | 98 | 100 | 63 | 100 | 3.0 s |
| Caliper | `/products/lune-sofa` | 97 | 100 | 74 | 100 | 3.1 s |
| Seam | `/` | 97 | 100 | 93 | 100 | 2.8 s |
| Seam | `/collections/coats-jackets` | 94 | 100 | 76 | 100 | 3.5 s |
| Seam | `/products/trinelle-wool-coat` | 98 | 100 | 86 | 100 | 3.4 s |
| Facet | `/` | 96 | 100 | 86 | 100 | 3.3 s |
| Facet | `/collections/rings` | 93 | 100 | 91 | 100 | 3.0 s |
| Facet | `/products/pebble-signet` | 96 | 100 | 89 | 100 | 3.1 s |

## Averages

| Preset | Desktop perf | Desktop a11y | Mobile perf | Mobile a11y |
| --- | --- | --- | --- | --- |
| Caliper | 97 | 100 | 74 | 100 |
| Seam | 96 | 100 | 85 | 100 |
| Facet | 95 | 100 | 89 | 100 |

## Notes

- Single runs vary a lot on this machine (the same Caliper home scored 62, 86 and 99 on desktop). Low outliers come from cold Shopify edge caches or from main-thread time in Shopify's own scripts (`<shopify-account>` logger, web pixels, shop-js), not from theme code.
- Changes made for this run: the collection banner is the only image with high fetch priority, gets accurate `sizes` and a 750 px rendition; the first product image, the collection banner, the article image and the home hero (when it is the first section) use `image_tag` `preload: true`. Mobile LCP on Facet rings went from 7.0 s to 3.0 s, on Caliper sofas from 5.5 s to 3.0 s.
