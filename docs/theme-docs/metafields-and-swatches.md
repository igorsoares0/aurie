# Metafields and swatches

Metafields let each product carry its own details, such as its material, its dimensions or a fit note. Arvel reads them in product cards, the cart and several product blocks.

## Create a metafield definition

1. In your admin, go to **Settings › Custom data › Products**.
2. Select **Add definition**.
3. Enter a **Name**, such as "Material". Shopify suggests the namespace and key, such as `custom.material`.
4. Choose the type **Single line text** (or **Multi-line text** for longer notes) and save.
5. Open a product and fill in the new field under **Metafields**.

## Where Arvel uses metafields

| Where | How to connect it | Suggested metafield |
| --- | --- | --- |
| Product card, material line | **Theme settings › Product cards › Card details: Material**, then **Material metafield** | `custom.material` |
| Product card, dimensions line | **Card details: Dimensions**, then **Dimensions metafield** | `custom.dimensions`, such as "W 220 × D 95 × H 78 cm" |
| Cart line, lead time | **Theme settings › Cart › Lead time metafield** | `custom.lead_time` |
| Product page, Fit notes block | Select the database icon next to **Text** and pick the metafield | `custom.fit` |
| Product page, Dimensions block | Connect each **value** field to a metafield | `custom.width`, `custom.depth`, `custom.height`, `custom.seat_height` |
| Product page, Text or Collapsible tab blocks | Select the database icon next to the text field | Any text metafield, such as materials and care |
| Product comparison section | Enter the metafield in each **Row metafield** | Any text metafield, such as `custom.width` |

Products without a value simply don't show that line.

## Color and pattern swatches

Swatches come from Shopify's product categories, not from the theme. To show them:

1. Open a product and choose its **Category**, such as "Dresses" or "Rings".
2. Under **Category metafields**, find **Color** (or **Pattern**) and add the colors the product comes in. Each color can have a hex value or an image.
3. In **Variants**, open the option, such as "Color", and select **Connect metafield** to link it to that category metafield.

Then, in the theme editor:

- On the product page, the **Variant picker** block shows swatches when **Show swatches** is on. **Swatch style** is **Circle**, or **Circle and name**.
- Product cards show the swatches automatically and switch the card image when a color is picked. For this, give each variant its own image in the product.

Some categories don't support color swatches, such as tables and desks. For those, options appear as buttons or a dropdown with the value names.
