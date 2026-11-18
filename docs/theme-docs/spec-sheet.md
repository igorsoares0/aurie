# Spec sheet

Caliper's signature is product information shown as design. Five features work together, and each one reads data you already keep in Shopify: product metafields and product options. When the data is missing, the feature simply doesn't appear, so a product without measurements still looks complete.

| Feature | What shoppers see | Where it reads from |
| --- | --- | --- |
| Catalog number | "Nº 014" next to the product name on cards, the product page, the breadcrumb and cart lines | A product metafield, such as `custom.catalog_number` |
| Dimension lines | Measurement lines with end ticks drawn along the edges of the first product image, such as W 220 cm and H 78 | Width and height product metafields, such as `custom.width` and `custom.height` |
| Option codes | "F-01 Linen sand", "C-02 Espresso", "M-01 18k gold" in the variant picker, the index and the cart | A code letter per option name, plus the position of each value |
| Figures | "Fig. 1", "Fig. 2" on gallery images and thumbnails | The order of the product media |
| Index view | A collection read as a table: number, image, name, chosen measurements, option codes and price | Product metafields chosen per section |

## Set it up

1. **Create the metafields.** In **Settings › Custom data › Products**, add the definitions you need. Single line text works for all of them. See [Metafields and swatches](metafields-and-swatches.md).
2. **Fill them in** on each product, under **Metafields**.
3. **Point the theme at them.** In the theme editor, open **Theme settings › Spec sheet**:
   - **Catalog number metafield**: such as `custom.catalog_number`. Enter numbers the way you want them shown, such as `014`.
   - **Option codes**: the option name and its code letter, separated by commas, such as `Fabric: F, Finish: W, Color: C, Metal: M`. Values then show as F-01, F-02 in the order they have in the product.
   - **Width metafield**, **Height metafield** and **Unit**: the measurements drawn as dimension lines, such as `custom.width`, `custom.height` and `cm`.
4. **Choose where they appear.** Each place has its own switch:
   - Product page: **Product information › Number images as figures** and **Show dimension lines on the first image**; **Title › Show catalog number**.
   - Product cards: **Theme settings › Product cards › Show dimension lines on cards**.
   - Collection and search pages: **Show index and plates switch**, **First view** and **Index columns** in the **Product grid** and **Search results** sections.
   - Home page: the **Catalog hero** and **Product index** sections.

Leave any field in **Spec sheet** empty to turn that feature off everywhere.

## Tips

- Dimension lines are drawn on the frame of the image, never over the object, so they work with any photo. Products shot on a plain background read best.
- If a width value contains Ø, such as `Ø 45`, the line is labeled with the value alone, which suits round tables and rings.
- Option codes follow the order of the values in the product. Reordering the values in your admin changes their codes.
- The **Fabric library** section has a **Code** field on each fabric, so a swatch can carry the same code shoppers see on the product page.
- The **Specification** block on the product page lists up to eight rows of details. Connect each value to a metafield to fill it per product.
