# Arvel 1.0.0: pre-submission checklist

Checked on 2026-11-14 and audited against every section of the Theme Store requirements page on 2026-11-15. Items marked ✅ were verified; items marked ⬜ are still to do.

## Theme package

- ✅ `docs/submission/Arvel-1.0.0.zip`, built with `shopify theme package`: 139 files, with `listings/arvel`, `listings/facet` and `listings/sotto`. The submission form requires a listings folder for every preset, including the default one: `listings/arvel` is a copy of the root `templates/` (cart, collection, index, product) and section groups, so keep both in sync when either changes.
- ✅ `AGENTS.md` removed from the zip. `shopify theme package` adds it from the repository root and ignores `.shopifyignore`, so remove it again after every rebuild.
- ✅ Theme Check: 121 files, no offenses.
- ✅ No `shopify://` references or demo metafields in templates, listings or section groups.
- ✅ No `config/markets.json`, Sass or minified CSS/JS.
- ✅ `theme_info`: version 1.0.0, author Aurie Studio, documentation and support links.
- ✅ Presets: Arvel, Facet, Sotto. One preset carries the theme name.
- ✅ Parity: each preset's install has the same structure as its demo store; only demo content differs.

## Quality

- ✅ Lighthouse on the published demo stores, median of 3, average of home, collection and product:
  - mobile: Arvel 79, Facet 91, Sotto 90;
  - desktop: Arvel 98, Facet 99, Sotto 98;
  - accessibility 100 on every page.
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
- ✅ Tally form republished: first and last name, email, store URL with an example, theme, problem description and screenshots. No autoresponder on the free plan; a confirmation page shows instead.

## Fixed in the 2026-11-15 audit

- Footer social media block: icons for each network, with a **Style** setting (names, icons, or icons and names).
- Footer social media menu now defaults to `footer`, as required for `link_list` settings in the header and footer. The repository section groups set it to empty, so installs look the same.
- **Custom Liquid** block added next to app blocks in the cart, collection, collection list, search, blog, article, page, featured product, contact form and footer sections.
- Featured product section shows a video, YouTube or Vimeo video or 3D model when that is the product's main media.
- Headings h1 to h6 are visually distinct, in rich text too.
- Spanish storefront translation (`locales/es.json`), so the demo stores' Spanish language shows the theme text in Spanish.
- Documentation updated for the above (`header-and-footer.md`, `sections.md`). Re-import it in GitBook.

## Still to check in the admin

- ✅ In each demo store, **Settings › Payments**: only the test gateway is active, with every other payment method and manual method turned off (requirement 20). Checked on 2026-11-16.

## Submitted

- ✅ Submitted in the Partner Dashboard on 2026-11-17 (theme 7442). Listing content, features, notes and the other-notes answers are recorded in `listing.md`; `form-fill.md` has the form in field order.
- During review: keep the demo stores and their password unchanged, and answer Shopify emails from themes@shopify.com quickly.

## Submit (how it was done)

1. In the Partner Dashboard, open **Themes** and start a new theme submission.
2. Upload `docs/submission/Arvel-1.0.0.zip`.
3. Fill in the theme listing and each preset listing from `listing.md`, with its demo store and screenshots.
4. Add the documentation and support links.
5. Review and submit.

Don't resubmit after a rejection without fixing every reason given: repeated resubmissions can suspend the account.

## Before submitting

- ⬜ Commit the repository.
- ⬜ Delete the Replicate API token that was pasted in chat.
