# Arvel 1.0.0: pre-submission checklist

Checked on 2026-11-14. Items marked ✅ were verified; items marked ⬜ are still to do.

## Theme package

- ✅ `docs/submission/Arvel-1.0.0.zip`, built with `shopify theme package`: 128 files, 590 KB, with `listings/facet` and `listings/sotto`.
- ✅ Theme Check: 119 files, no offenses.
- ✅ No `shopify://` references or demo metafields in templates, listings or section groups.
- ✅ No `config/markets.json`, Sass or minified CSS/JS.
- ✅ `theme_info`: version 1.0.0, author Aurie Studio, documentation and support links.
- ✅ Presets: Arvel, Facet, Sotto. One preset carries the theme name.
- ✅ Parity: each preset's install has the same structure as its demo store; only demo content differs.

## Quality

- ✅ Lighthouse on the published demo stores (mobile, median of 3): Arvel 79, Facet 91, Sotto 90; accessibility 100.
- ✅ Keyboard: skip link, tab order, visible focus, drawers trap focus and close with Escape.
- ✅ Automated sweep: no horizontal scroll, broken images, Liquid or JavaScript errors; touch targets at least 44 × 44 px on mobile; no axe violations.
- ✅ HTML validation: the remaining messages come from Shopify's injected scripts.
- ⬜ Real-device and browser check: Safari (Mac and iPhone), Firefox, Chrome on Android, and the Instagram and Facebook in-app browsers. Only headless Chrome was tested.

## Demo stores

| Preset | Store | Theme |
| --- | --- | --- |
| Arvel | arvel-theme-9h3bmm3m.myshopify.com | Arvel demo (published) |
| Facet | arvel-facet-7rk7w1ea.myshopify.com | Facet demo (published) |
| Sotto | arvel-sotto-iivcamps.myshopify.com | Sotto demo (published) |

- ✅ Client transfer stores, created in the Dev Dashboard.
- ✅ 24 products each, with collections, pages, blog posts, menus and AI-generated photos (rights under Replicate's terms; generation records in each `images/manifest.json`).
- ✅ Store names, refund, shipping and terms policies, privacy policy, a second market (United States), a second language (Spanish), test payment gateway, filters, homepage title and meta description.
- ✅ Gift card product in the Facet store.

## Listing and support

- ✅ Listing copy: `docs/submission/listing.md`.
- ✅ Screenshots: `docs/submission/screenshots/` (18 images).
- ✅ Documentation: https://arvel-theme-documentation.gitbook.io/arvel-theme-documentation-docs (public).
- ✅ Support form: https://tally.so/r/Ge9EpZ (public).
- ⬜ Optional: in GitBook, delete the SUMMARY page and rename the pages in the sidebar (Introduction, Getting started, …).
- ⬜ Republish the Tally form so the "Store URL (for example, …)" label goes live.

## Submit

1. In the Partner Dashboard, open **Themes** and start a new theme submission.
2. Upload `docs/submission/Arvel-1.0.0.zip`.
3. Fill in the theme listing and each preset listing from `listing.md`, with its demo store and screenshots.
4. Add the documentation and support links.
5. Review and submit.

Don't resubmit after a rejection without fixing every reason given: repeated resubmissions can suspend the account.

## Before submitting

- ⬜ Commit the repository.
- ⬜ Delete the Replicate API token that was pasted in chat.
