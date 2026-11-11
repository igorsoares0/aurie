#!/usr/bin/env python3
"""Load a preset's demo catalog into a Shopify store.

Reads docs/_design/demo-photos/<preset>/catalog.json and images/manifest.json,
then uses `shopify store execute` (Admin GraphQL 2026-07) to:

  1. create the custom.material and custom.dimensions metafield definitions
  2. upload every approved image as a file (staged upload + fileCreate)
  3. create or update each product with productSet (options, variants,
     prices, inventory, media, variant images) and publish it
  4. write the material/dimensions metafields
  5. create the gift card product and the collections, and publish them

Editorial images are uploaded as files only; pick them in the theme editor.
Progress is kept in <preset>/.shopify-<store>.json so a rerun skips finished
work. Without --yes it only prints the plan.

Usage:
  python3 tools/shopify_import.py <preset> --store <name>.myshopify.com [--yes]

Authenticate first:
  shopify store auth --store <name>.myshopify.com --scopes <SCOPES>
"""

import argparse
import json
import mimetypes
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid
from pathlib import Path

from demo_images import slug, variant_values

ROOT = Path(__file__).resolve().parent.parent
GRAPHQL = Path(__file__).resolve().parent / "graphql"
SCOPES = ("read_products,write_products,read_files,write_files,read_inventory,write_inventory,"
          "read_locations,read_publications,write_publications,read_metaobjects,write_metaobjects,"
          "read_metaobject_definitions,write_metaobject_definitions,read_online_store_pages,"
          "write_online_store_pages,read_content,write_content,read_online_store_navigation,"
          "write_online_store_navigation")
STOCK = 8
SOLID_PATTERN = "gid://shopify/TaxonomyValue/2874"  # taxonomy pattern "Solid", required by color metaobjects


class Store:
    def __init__(self, domain):
        self.domain = domain

    def run(self, operation, variables=None, mutation=False):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump(variables or {}, handle)
            variable_file = handle.name
        command = [
            "shopify", "store", "execute",
            "--store", self.domain,
            "--query-file", str(GRAPHQL / f"{operation}.graphql"),
            "--variable-file", variable_file,
            "--json", "--no-color",
        ]
        if mutation:
            command.append("--allow-mutations")
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        Path(variable_file).unlink(missing_ok=True)
        # Output can mix one-line progress events with the (pretty-printed) result;
        # keep the last JSON object that is not a progress event.
        payload = None
        text = result.stdout
        decoder = json.JSONDecoder()
        position = 0
        while True:
            start = text.find("{", position)
            if start == -1:
                break
            try:
                value, position = decoder.raw_decode(text, start)
            except json.JSONDecodeError:
                position = start + 1
                continue
            if isinstance(value, dict) and value.get("type") != "progress":
                payload = value
        if result.returncode != 0 or payload is None or "error" in payload:
            raise RuntimeError(f"{operation} failed:\n{result.stderr or result.stdout}")
        return payload.get("data", payload)


def user_errors(data, key):
    errors = data[key].get("userErrors") or []
    return [e for e in errors if e.get("code") != "TAKEN"]


def upload(target, path):
    """POST a file to a staged upload target (multipart form)."""
    boundary = uuid.uuid4().hex
    body = bytearray()
    for parameter in target["parameters"]:
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{parameter['name']}\"\r\n\r\n{parameter['value']}\r\n".encode()
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{path.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode()
    body += path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    request = urllib.request.Request(target["url"], data=bytes(body), method="POST",
                                     headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(request, timeout=180) as response:
        if response.status >= 300:
            raise RuntimeError(f"upload of {path.name} returned {response.status}")


class Importer:
    def __init__(self, preset, domain):
        self.folder = ROOT / preset
        self.catalog = json.loads((self.folder / "catalog.json").read_text(encoding="utf-8"))
        self.manifest = json.loads((self.folder / "images" / "manifest.json").read_text(encoding="utf-8"))
        self.state_path = self.folder / f".shopify-{domain.split('.')[0]}.json"
        self.state = json.loads(self.state_path.read_text(encoding="utf-8")) if self.state_path.exists() else {}
        for key in ("files", "products", "collections"):
            self.state.setdefault(key, {})
        self.store = Store(domain)

    def save(self):
        self.state_path.write_text(json.dumps(self.state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # --- plan -----------------------------------------------------------

    def plan(self):
        pending_files = [k for k in self.manifest if k not in self.state["files"] and not k.startswith("model--")]
        products = self.catalog["products"]
        print(f"Store: {self.store.domain}")
        print(f"Images to upload: {len(pending_files)} of {len(self.manifest)}")
        print(f"Products: {len(products)} (+ gift card), collections: {len(self.catalog['collections'])}")
        print("Each product is created with productSet (identifier: handle), so reruns update in place.")

    # --- steps ----------------------------------------------------------

    def setup(self):
        data = self.store.run("setup")
        self.location = data["locations"]["nodes"][0]["id"]
        online = [p for p in data["publications"]["nodes"] if (p.get("catalog") or {}).get("title", "").endswith("Online Store")]
        if not online:
            sys.exit("Online Store publication not found.")
        self.publication = online[0]["id"]
        print(f"location {self.location}, publication {self.publication}")

    def metafield_specs(self):
        """Product metafields to write: catalog["metafields"], or the Joias defaults."""
        return self.catalog.get("metafields") or [
            {"key": "material", "name": "Material", "template": "{value} · {spec}"},
            {"key": "dimensions", "name": "Dimensions", "field": "dimensions"},
            {"key": "style", "name": "Style", "field": "style"},
        ]

    def definitions(self):
        for spec in self.metafield_specs():
            key, name = spec["key"], spec["name"]
            data = self.store.run("metafield_definition", {"definition": {
                "name": name, "namespace": "custom", "key": key,
                "type": "single_line_text_field", "ownerType": "PRODUCT",
                "access": {"storefront": "PUBLIC_READ"},
            }}, mutation=True)
            errors = user_errors(data, "metafieldDefinitionCreate")
            if errors:
                print(f"definition custom.{key}: {errors}")

    def swatch_values(self):
        return self.catalog.get("metals") or self.catalog.get("colors")

    def swatches(self):
        """Option values (metals or colors) as Shopify color metaobjects, so options render as swatches."""
        for operation, key in (("enable_color_metaobject", "standardMetaobjectDefinitionEnable"),
                               ("enable_color_metafield", "standardMetafieldDefinitionEnable")):
            errors = user_errors(self.store.run(operation, mutation=True), key)
            if errors:
                print(f"{operation}: {errors}")
        for name, metal in self.swatch_values().items():
            data = self.store.run("metaobject_upsert", {
                "handle": {"type": "shopify--color-pattern", "handle": metal["handle"]},
                "metaobject": {"fields": [
                    {"key": "label", "value": name},
                    {"key": "color", "value": metal["swatch"]},
                    {"key": "color_taxonomy_reference", "value": json.dumps([metal["taxonomy"]])},
                    {"key": "pattern_taxonomy_reference", "value": SOLID_PATTERN},
                ]},
            }, mutation=True)["metaobjectUpsert"]
            if data["userErrors"]:
                sys.exit(f"metaobjectUpsert {name}: {data['userErrors']}")
            self.state.setdefault("metals", {})[name] = data["metaobject"]["id"]
        self.save()
        print(f"swatches {len(self.swatch_values())}")

    def upload_files(self):
        # Model references are generation inputs, not store content (the first one predates this rule).
        pending = [k for k in self.manifest if k not in self.state["files"] and not k.startswith("model--")]
        images = self.folder / "images"
        for start in range(0, len(pending), 10):
            batch = pending[start:start + 10]
            paths = [images / self.manifest[k]["file"] for k in batch]
            staged = self.store.run("staged_uploads", {"input": [{
                "filename": p.name, "mimeType": "image/jpeg", "resource": "IMAGE",
                "httpMethod": "POST", "fileSize": str(p.stat().st_size),
            } for p in paths]}, mutation=True)["stagedUploadsCreate"]
            if staged["userErrors"]:
                sys.exit(f"stagedUploadsCreate: {staged['userErrors']}")
            for target, path in zip(staged["stagedTargets"], paths):
                upload(target, path)
            created = self.store.run("file_create", {"files": [{
                "originalSource": target["resourceUrl"], "alt": self.manifest[k]["alt"] or path.stem,
                "filename": path.name, "contentType": "IMAGE",
            } for target, path, k in zip(staged["stagedTargets"], paths, batch)]}, mutation=True)["fileCreate"]
            if created["userErrors"]:
                sys.exit(f"fileCreate: {created['userErrors']}")
            for job_id, file in zip(batch, created["files"]):
                self.state["files"][job_id] = {"id": file["id"]}
            self.save()
            print(f"uploaded {start + len(batch)}/{len(pending)}")
        self.wait_for_files()

    def wait_for_files(self):
        for _ in range(40):
            waiting = [k for k, v in self.state["files"].items() if not v.get("url")]
            if not waiting:
                return
            ids = [self.state["files"][k]["id"] for k in waiting]
            nodes = []
            for start in range(0, len(ids), 50):
                nodes += self.store.run("file_status", {"ids": ids[start:start + 50]})["nodes"]
            by_id = {n["id"]: n for n in nodes if n}
            for key in waiting:
                node = by_id.get(self.state["files"][key]["id"]) or {}
                if node.get("fileStatus") == "FAILED":
                    sys.exit(f"file processing failed for {key}")
                if node.get("fileStatus") == "READY" and node.get("image"):
                    self.state["files"][key]["url"] = node["image"]["url"]
            self.save()
            time.sleep(3)
        sys.exit("files did not finish processing; rerun later")

    def media(self, job_id):
        # Reference the already uploaded file by id, so it is reused, not copied.
        return {"id": self.state["files"][job_id]["id"]}

    def product_input(self, product, linked=True):
        handle = product["handle"]
        prices = variant_values(product)
        metals = list(prices)
        # Móveis mixes "Fabric" and "Finish", so a product can name its own option.
        option = product.get("option") or self.catalog.get("option", "Metal")
        collection = next(c for c in self.catalog["collections"] if c["handle"] == product["collection"])
        jobs = [k for k in self.manifest if k.startswith(f"{handle}--")]
        order = {"front": 0, "side": 1, "back": 1, "worn": 2, "detail": 2}
        jobs.sort(key=lambda k: (0 if f"--{slug(metals[0])}--" in k else 1, order.get(k.rsplit("--", 1)[1], 3)))
        swatch_ids = self.state.get("metals", {})
        if linked:
            options = [{"name": option, "position": 1, "linkedMetafield": {
                "namespace": "shopify", "key": "color-pattern", "values": [swatch_ids[m] for m in metals],
            }}]
        else:
            options = [{"name": option, "position": 1, "values": [{"name": m} for m in metals]}]
        sizes = product.get("sizes") or []
        if sizes:
            options.append({"name": "Size", "position": 2, "values": [{"name": s} for s in sizes]})
        sold_out = {(s.get("metal") or s.get("color"), s["size"]) for s in product.get("sold_out", [])}
        variants = []
        for metal in metals:
            front = f"{handle}--{slug(metal)}--front"
            for size in sizes or [None]:
                if linked:
                    values = [{"optionName": option, "linkedMetafieldValue": swatch_ids[metal]}]
                else:
                    values = [{"optionName": option, "name": metal}]
                if size:
                    values.append({"optionName": "Size", "name": size})
                variant = {
                    "optionValues": values,
                    "price": prices[metal],
                    "sku": "-".join(filter(None, [handle, slug(metal), size])).upper(),
                    "inventoryPolicy": "DENY",
                    "inventoryItem": {"tracked": True},
                    "inventoryQuantities": [{
                        "locationId": self.location, "name": "available",
                        "quantity": 0 if (metal, size) in sold_out else STOCK,
                    }],
                }
                compare_at = (product.get("compare_at") or {}).get(metal)
                if compare_at:
                    variant["compareAtPrice"] = compare_at
                if front in self.state["files"]:
                    variant["file"] = self.media(front)
                variants.append(variant)
        return {
            "title": product["title"],
            "handle": handle,
            "descriptionHtml": f"<p>{product['description']}</p>",
            "vendor": self.catalog.get("vendor", ""),
            "productType": collection["title"],
            **({"category": product.get("category") or collection["category"]}
               if product.get("category") or collection.get("category") else {}),
            "status": "ACTIVE",
            "tags": product.get("tags", []),
            "productOptions": options,
            "files": [self.media(k) for k in jobs if k in self.state["files"]],
            "variants": variants,
        }

    def publish(self, resource_id):
        data = self.store.run("publish", {"id": resource_id, "input": [{"publicationId": self.publication}]}, mutation=True)
        if data["publishablePublish"]["userErrors"]:
            print(f"publish {resource_id}: {data['publishablePublish']['userErrors']}")

    def products(self, update=False, only=None):
        for product in self.catalog["products"]:
            handle = product["handle"]
            if only is not None and handle not in only:
                continue
            if handle in self.state["products"] and not update:
                continue
            data = self.store.run("product_set", {
                "identifier": {"handle": handle},
                "input": self.product_input(product),
            }, mutation=True)["productSet"]
            # Tables and desks are outside the categories of the standard color definition,
            # so their option falls back to plain values (no swatch).
            if any(e.get("code") == "INVALID_METAFIELD_VALUE_FOR_LINKED_OPTION" for e in data["userErrors"]):
                print(f"{handle}: category has no color swatches, using plain option values")
                data = self.store.run("product_set", {
                    "identifier": {"handle": handle},
                    "input": self.product_input(product, linked=False),
                }, mutation=True)["productSet"]
            if data["userErrors"]:
                sys.exit(f"productSet {handle}: {data['userErrors']}")
            product_id = data["product"]["id"]
            if handle not in self.state["products"]:
                self.publish(product_id)
            self.state["products"][handle] = product_id
            self.save()
            print(f"product {handle}")

    def metafields(self):
        entries = []
        for product in self.catalog["products"]:
            owner = self.state["products"][product["handle"]]
            first_value = next(iter(variant_values(product)))
            for spec in self.metafield_specs():
                if "template" in spec:
                    value = spec["template"].format(value=first_value, **product)
                else:
                    value = product.get(spec["field"])
                if value:
                    entries.append({"ownerId": owner, "namespace": "custom", "key": spec["key"],
                                    "type": "single_line_text_field", "value": value})
        for start in range(0, len(entries), 25):
            data = self.store.run("metafields_set", {"metafields": entries[start:start + 25]}, mutation=True)
            if data["metafieldsSet"]["userErrors"]:
                sys.exit(f"metafieldsSet: {data['metafieldsSet']['userErrors']}")
        print(f"metafields {len(entries)}")

    def gift_card(self):
        gift = self.catalog.get("gift_card")
        if not gift or gift["handle"] in self.state["products"]:
            return
        values = [f"${amount}" for amount in gift["denominations"]]
        data = self.store.run("gift_card_product_set", {
            "identifier": {"handle": gift["handle"]},
            "input": {
                "title": gift["title"],
                "handle": gift["handle"],
                "descriptionHtml": "<p>Let them choose. Delivered by email with a personal note.</p>",
                "status": "ACTIVE",
                "productOptions": [{"name": "Denomination", "position": 1, "values": [{"name": v} for v in values]}],
                "files": [self.media("gift-card--front")] if "gift-card--front" in self.state["files"] else [],
                "variants": [{"optionValues": [{"optionName": "Denomination", "name": v}], "price": a}
                             for v, a in zip(values, gift["denominations"])],
            },
        }, mutation=True)["giftCardProductSet"]
        if data["userErrors"]:
            # Usually gift cards are not activated yet (Settings > Gift cards); rerun later.
            print(f"gift card skipped: {data['userErrors']}")
            return
        self.publish(data["product"]["id"])
        self.state["products"][gift["handle"]] = data["product"]["id"]
        self.save()
        print("gift card")

    def collections(self):
        for collection in self.catalog["collections"]:
            handle = collection["handle"]
            if handle in self.state["collections"]:
                continue
            existing = self.store.run("collection_lookup", {"handle": handle})["collectionByIdentifier"]
            if existing:
                self.state["collections"][handle] = existing["id"]
                self.save()
                continue
            image = self.state["files"].get(collection.get("image") or f"editorial--collection-{handle}")
            if collection.get("tag"):
                source = {"title": f"Tagged {collection['tag']}", "targetType": "PRODUCTS", "inclusion": {
                    "matchType": "ALL",
                    "conditions": [{"productTag": {"relation": "TAGGED_WITH", "values": [collection["tag"]], "matchType": "ANY"}}],
                }}
            else:
                handles = collection.get("products") or [p["handle"] for p in self.catalog["products"] if p["collection"] == handle]
                source = {"title": "Hand-picked", "targetType": "PRODUCTS",
                          "inclusion": {"selections": [{"productId": self.state["products"][h]} for h in handles]}}
            data = self.store.run("collection_create", {"collection": {
                "title": collection["title"],
                "handle": handle,
                **({} if collection.get("tag") else {"sortOrder": "MANUAL"}),
                **({"image": {"src": image["url"], "altText": collection["title"]}} if image else {}),
                "sources": [{"source": source}],
            }}, mutation=True)["collectionCreate"]
            if data["userErrors"]:
                sys.exit(f"collectionCreate {handle}: {data['userErrors']}")
            self.publish(data["collection"]["id"])
            self.state["collections"][handle] = data["collection"]["id"]
            self.save()
            print(f"collection {handle}")

    def fill_files(self, html):
        """Replace {file:<job id>} with the uploaded image's CDN URL."""
        return re.sub(r"\{file:([^}]+)\}", lambda m: self.state["files"][m.group(1)]["url"], html)

    def blog(self):
        blog = self.catalog.get("blog")
        if not blog:
            return
        blogs = self.state.setdefault("blogs", {})
        if blog["handle"] not in blogs:
            found = self.store.run("blog_lookup", {"query": f"handle:{blog['handle']}"})["blogs"]["nodes"]
            if found:
                blogs[blog["handle"]] = found[0]["id"]
            else:
                data = self.store.run("blog_create", {"blog": {"title": blog["title"], "handle": blog["handle"]}},
                                      mutation=True)["blogCreate"]
                if data["userErrors"]:
                    sys.exit(f"blogCreate: {data['userErrors']}")
                blogs[blog["handle"]] = data["blog"]["id"]
            self.save()
        articles = self.state.setdefault("articles", {})
        for article in blog["articles"]:
            handle = article["handle"]
            if handle in articles:
                continue
            found = self.store.run("article_lookup", {"query": f"handle:{handle}"})["articles"]["nodes"]
            if found:
                articles[handle] = found[0]["id"]
            else:
                image = self.state["files"][article["image"]]
                data = self.store.run("article_create", {"article": {
                    "blogId": blogs[blog["handle"]],
                    "title": article["title"],
                    "handle": handle,
                    "body": self.fill_files(article["body"]),
                    "summary": article["summary"],
                    "author": {"name": blog["author"]},
                    "tags": article.get("tags", []),
                    "image": {"url": image["url"], "altText": self.manifest[article["image"]]["alt"] or article["title"]},
                    "isPublished": True,
                }}, mutation=True)["articleCreate"]
                if data["userErrors"]:
                    sys.exit(f"articleCreate {handle}: {data['userErrors']}")
                articles[handle] = data["article"]["id"]
            self.save()
            print(f"article {handle}")

    def pages(self):
        pages = self.state.setdefault("pages", {})
        for page in self.catalog.get("pages", []):
            handle = page["handle"]
            if handle in pages:
                continue
            found = self.store.run("page_lookup", {"query": f"handle:{handle}"})["pages"]["nodes"]
            if found:
                pages[handle] = found[0]["id"]
            else:
                data = self.store.run("page_create", {"page": {
                    "title": page["title"], "handle": handle, "body": self.fill_files(page["body"]), "isPublished": True,
                    **({"templateSuffix": page["template_suffix"]} if page.get("template_suffix") else {}),
                }}, mutation=True)["pageCreate"]
                if data["userErrors"]:
                    sys.exit(f"pageCreate {handle}: {data['userErrors']}")
                pages[handle] = data["page"]["id"]
            self.save()
            print(f"page {handle}")

    def update_pages(self, handles=None):
        """Re-send the body of pages that already exist (after editing them in the catalog)."""
        pages = self.state.get("pages", {})
        for page in self.catalog.get("pages", []):
            handle = page["handle"]
            if handle not in pages or (handles and handle not in handles):
                continue
            data = self.store.run("page_update", {"id": pages[handle], "page": {
                "body": self.fill_files(page["body"]),
            }}, mutation=True)["pageUpdate"]
            if data["userErrors"]:
                sys.exit(f"pageUpdate {handle}: {data['userErrors']}")
            print(f"page {handle} updated")

    def menu_items(self, items):
        resolved = []
        for item in items:
            entry = {"title": item["title"]}
            if "collection" in item:
                entry.update(type="COLLECTION", resourceId=self.state["collections"][item["collection"]])
            elif "page" in item:
                entry.update(type="PAGE", resourceId=self.state["pages"][item["page"]])
            elif "product" in item:
                entry.update(type="PRODUCT", resourceId=self.state["products"][item["product"]])
            elif "blog" in item:
                entry.update(type="BLOG", resourceId=self.state["blogs"][item["blog"]])
            else:
                entry.update(type="HTTP", url=item["url"])
            if item.get("items"):
                entry["items"] = self.menu_items(item["items"])
            resolved.append(entry)
        return resolved

    def menus(self):
        """Demo-only menus; existing store menus are left untouched."""
        existing = {m["handle"]: m["id"] for m in self.store.run("menu_lookup")["menus"]["nodes"]}
        for menu in self.catalog.get("menus", []):
            items = self.menu_items(menu["items"])
            if menu["handle"] in existing:
                data = self.store.run("menu_update", {"id": existing[menu["handle"]], "title": menu["title"],
                                                      "handle": menu["handle"], "items": items}, mutation=True)["menuUpdate"]
            else:
                data = self.store.run("menu_create", {"title": menu["title"], "handle": menu["handle"],
                                                      "items": items}, mutation=True)["menuCreate"]
            if data["userErrors"]:
                sys.exit(f"menu {menu['handle']}: {data['userErrors']}")
            print(f"menu {menu['handle']}")

    def replace(self, job_ids):
        """Swap regenerated images: delete the old store files, upload the new ones
        under the same names and re-send the products that use them."""
        unknown = [k for k in job_ids if k not in self.manifest]
        if unknown:
            sys.exit(f"not in the manifest: {', '.join(unknown)}")
        self.setup()  # location and publication, needed by productSet
        old = [self.state["files"][k]["id"] for k in job_ids if k in self.state["files"]]
        if old:
            data = self.store.run("file_delete", {"fileIds": old}, mutation=True)["fileDelete"]
            if data["userErrors"]:
                sys.exit(f"fileDelete: {data['userErrors']}")
            print(f"deleted {len(data['deletedFileIds'])} old files")
        for k in job_ids:
            self.state["files"].pop(k, None)
        self.save()
        # Shopify releases a deleted file's name after a moment; a new file may otherwise get a suffix.
        time.sleep(10)
        self.upload_files()
        handles = {k.split("--")[0] for k in job_ids if not k.startswith(("editorial--", "model--"))}
        self.products(update=True, only=handles)
        self.metafields()
        for k in job_ids:
            if k.startswith("editorial--"):
                print(f"{k}: {self.state['files'][k]['url'].split('/')[-1].split('?')[0]}")

    def run(self, update=False):
        self.setup()
        self.definitions()
        self.swatches()
        self.upload_files()
        self.products(update)
        self.metafields()
        self.gift_card()
        self.collections()
        self.pages()
        self.blog()
        self.menus()
        editorial = [self.manifest[k]["file"] for k in self.manifest if k.startswith("editorial--")]
        print(f"Done. Editorial images are in Files: {', '.join(Path(f).name for f in editorial)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("preset")
    parser.add_argument("--store", required=True)
    parser.add_argument("--yes", action="store_true", help="run the import (otherwise only print the plan)")
    parser.add_argument("--update", action="store_true", help="also re-send products that were already created")
    parser.add_argument("--replace", help="comma-separated image job ids that were regenerated: "
                        "deletes the old store files, uploads the new ones and re-sends their products")
    parser.add_argument("--update-pages", nargs="?", const="all", help="re-send the body of existing pages: "
                        "all of them, or a comma-separated list of handles")
    args = parser.parse_args()
    importer = Importer(args.preset, args.store)
    if args.update_pages:
        handles = None if args.update_pages == "all" else [h.strip() for h in args.update_pages.split(",")]
        print(f"Update page bodies on {args.store}: {', '.join(handles) if handles else 'all pages in the catalog'}")
        if args.yes:
            importer.update_pages(handles)
        return
    if args.replace:
        job_ids = [k.strip() for k in args.replace.split(",") if k.strip()]
        print(f"Replace {len(job_ids)} images on {args.store}: {', '.join(job_ids)}")
        if args.yes:
            importer.replace(job_ids)
        return
    importer.plan()
    if not args.yes:
        print(f"\nAuthenticate with:\n  shopify store auth --store {args.store} --scopes {SCOPES}\nThen rerun with --yes.")
        return
    importer.run(args.update)


if __name__ == "__main__":
    main()
