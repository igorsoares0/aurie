# Product pages

The product page is built with the **Product information** section. Its blocks can be reordered, removed or added again.

## Product information settings

- **Media aspect ratio**: **Match gallery layout**, **Adapt to first image**, **Portrait**, **Square** or **Landscape**. Images are cropped to fit.
- **Show breadcrumb**: links back to the home page and, when the customer came from a collection, to that collection.
- **Keep product information visible while scrolling**: the column with the title and buttons stays in view on desktop while the gallery scrolls.
- **Number images as figures**: labels each image and thumbnail as Fig. 1, Fig. 2 and so on.
- **Show dimension lines on the first image**: draws the product's width and height along the edges of the first image, from the metafields set in **Theme settings › Spec sheet**.

The gallery layout itself is set in **Theme settings › Product media**. When a customer picks a variant, the gallery moves to that variant's image. In the grid layout, a product with an odd number of images shows the first one at full width, so every row is complete.

## Blocks

| Block | What it does |
| --- | --- |
| **Title** | The product name. **Text above title** can show the **Product type** or **Vendor**, and **Show catalog number** adds "Nº 014" from the metafield set in **Theme settings › Spec sheet**. |
| **Price** | The price, compare-at price and unit price. **Show tax and shipping note** adds a line that says whether taxes and duties are included and that shipping is calculated at checkout, following your store's tax settings. |
| **Installments** | Shows Shop Pay Installments when it's available for the product. Nothing appears when it isn't. |
| **Variant picker** | The product options. See [Variant picker and swatches](#variant-picker-and-swatches). |
| **Fit notes** | A short note about fit, such as "Model is 177 cm and wears S". Connect a product metafield to show notes per product. |
| **Dimensions** | A boxed note with up to four measurements, such as width, depth, height and seat height, a **Unit note** and a **Note**. Connect each value to a product metafield; empty values are hidden. |
| **Specification** | The product's details as rows of a spec sheet, such as Composition, Materials or Seat height: up to eight rows, each a label and a value. Connect values to metafields to fill them per product; rows without a value are hidden. **Use the label font for values** sets the values in the label font. |
| **Engraving field** | A checkbox that reveals a text field for personalization. The text is saved with the cart line and the order under **Order note name**. Set **Maximum characters** and the **Helper text**. |
| **Lead time** | A short line with an icon, such as a delivery estimate or "Gift box included". Connect its text to a metafield to show a different lead time per product. |
| **Buy buttons** | Quantity, add to cart and the dynamic checkout buttons (Shop Pay, Apple Pay and others). **Show sticky add to cart bar on mobile** keeps a bar at the bottom of the screen once the main button scrolls away. |
| **Pickup availability** | Shows where the product can be picked up, for locations with local pickup turned on. |
| **Collapsible tab** | A row that opens and closes. Its content can be text, a page (**Content from page**) or the product description (**Show product description**). **Heading style** is **Label font** or **Heading font**. |
| **Text** | Free text. **Style** is **Body**, **Small** or **Caption**. Connect it to a metafield to show product-specific text, such as the material. |
| **Custom Liquid** | Your own Liquid code. |
| **App blocks** | Blocks from apps you install, such as reviews or subscriptions. |

## Variant picker and swatches

- **Style**: **Buttons**, **Dropdown** or **Rows with codes and prices**. Rows show each value as a line of a table: a radio button, its swatch, its option code (such as F-01), its name and, when prices differ between variants, its price. Sold-out values are struck through. The option's heading shows the chosen value with its code, such as "Fabric — F-01 Linen sand".
- **Show swatches**: shows color or pattern swatches for options linked to Shopify's category metafields. See [Metafields and swatches](metafields-and-swatches.md).
- **Swatch style**: **Circle**, or **Circle and name**.

Sold-out combinations stay selectable and are marked as sold out, so customers can still see the price and image.

### Size guide

1. Create a page with your size table, for example **Size guide**.
2. In the **Variant picker** block, choose it as the **Size guide page**.
3. In **Show next to options**, list the option names the link appears next to, separated by commas, such as `Size, Ring size`.
4. Set the **Link label**.

The guide opens in a drawer without leaving the product page.

## Gift cards

Gift card products use the same product page. In the **Buy buttons** block, turn on **Show recipient form for gift cards** to let customers send the gift card to someone else on a chosen date, with a message.

## Recommendations

Below the product, two **Product recommendations** sections show related products and complementary products. Complementary products only appear after you set them in the Search & Discovery app.
