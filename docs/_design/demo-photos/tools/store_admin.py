#!/usr/bin/env python3
"""Set up a demo store's policies, second market and second language.

Reads docs/_design/demo-photos/<preset>/policies.md and, through
`shopify store execute`, sets:

  1. the refund, shipping and terms of service policies (the privacy policy
     is left to Shopify's automatic one, which is more complete)
  2. a second market for the United States
  3. Spanish as a second, published language

Steps that are already done are skipped. Without --yes it only prints the plan.

Usage:
  python3 tools/store_admin.py <preset> --store <name>.myshopify.com [--yes]

Authenticate first with the importer's scopes plus:
  read_legal_policies,write_legal_policies,read_markets,write_markets,read_locales,write_locales
"""

import argparse
import html
import re
import sys
from pathlib import Path

from shopify_import import ROOT, Store

POLICIES = {"Refund policy": "REFUND_POLICY", "Shipping policy": "SHIPPING_POLICY", "Terms of service": "TERMS_OF_SERVICE"}
MARKET = {"name": "United States", "handle": "united-states", "country": "US"}
LANGUAGE = "es"


def inline(text):
    text = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def markdown_to_html(markdown):
    """The small subset the policy files use: paragraphs, **bold** lead-ins and - lists."""
    out, items = [], []
    def flush():
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()
    for block in re.split(r"\n\s*\n", markdown.strip()):
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        paragraph = []
        for line in lines:
            if line.startswith("- "):
                if paragraph:
                    out.append("<p>" + "<br>".join(inline(p) for p in paragraph) + "</p>"); paragraph = []
                items.append(line[2:])
            else:
                flush(); paragraph.append(line)
        flush()
        if paragraph:
            out.append("<p>" + "<br>".join(inline(p) for p in paragraph) + "</p>")
    return "\n".join(out)


def read_policies(preset):
    text = (ROOT / preset / "policies.md").read_text(encoding="utf-8")
    sections = re.split(r"^## (.+)$", text, flags=re.M)
    found = {}
    for title, body in zip(sections[1::2], sections[2::2]):
        if title.strip() in POLICIES:
            found[POLICIES[title.strip()]] = markdown_to_html(body.split("\n---")[0])
    missing = set(POLICIES.values()) - set(found)
    if missing:
        sys.exit(f"{preset}/policies.md is missing: {', '.join(sorted(missing))}")
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("preset")
    parser.add_argument("--store", required=True)
    parser.add_argument("--yes", action="store_true", help="apply the changes (otherwise only print the plan)")
    args = parser.parse_args()
    store = Store(args.store)
    policies = read_policies(args.preset)
    state = store.run("admin_state")
    current = {p["type"]: p["body"] for p in state["shop"]["shopPolicies"]}
    markets = {m["handle"] for m in state["markets"]["nodes"]}
    locales = {l["locale"]: l for l in state["shopLocales"]}

    todo_policies = [t for t, body in policies.items() if current.get(t) != body]
    needs_market = MARKET["handle"] not in markets
    needs_enable = LANGUAGE not in locales
    # The language must be on the same web presences as the primary one, or the
    # storefront has no /es URL and the language selector stays empty.
    primary = next(l for l in locales.values() if l["primary"])
    presences = sorted(w["id"] for w in primary["marketWebPresences"])
    current_presences = sorted(w["id"] for w in locales.get(LANGUAGE, {}).get("marketWebPresences", []))
    needs_publish = not locales.get(LANGUAGE, {}).get("published") or current_presences != presences
    print(f"Store: {args.store} ({state['shop']['name']})")
    print(f"Policies to set: {', '.join(todo_policies) or 'none'}")
    print(f"Market {MARKET['name']}: {'create' if needs_market else 'exists'}")
    print(f"Language {LANGUAGE}: {'enable and publish' if needs_enable else 'publish' if needs_publish else 'published'}")
    if not args.yes:
        return

    for policy_type in todo_policies:
        data = store.run("policy_update", {"shopPolicy": {"type": policy_type, "body": policies[policy_type]}}, mutation=True)["shopPolicyUpdate"]
        if data["userErrors"]:
            sys.exit(f"{policy_type}: {data['userErrors']}")
        print(f"policy {data['shopPolicy']['title']}")
    if needs_market:
        data = store.run("market_create", {"input": {
            "name": MARKET["name"], "handle": MARKET["handle"], "enabled": True,
            "conditions": {"regionsCondition": {"regions": [{"countryCode": MARKET["country"]}]}},
        }}, mutation=True)["marketCreate"]
        if data["userErrors"]:
            sys.exit(f"market: {data['userErrors']}")
        print(f"market {data['market']['name']} {data['market']['status']}")
    if needs_enable:
        data = store.run("locale_enable", {"locale": LANGUAGE}, mutation=True)["shopLocaleEnable"]
        if data["userErrors"]:
            sys.exit(f"language: {data['userErrors']}")
    if needs_enable or needs_publish:
        data = store.run("locale_publish", {"locale": LANGUAGE, "presences": presences}, mutation=True)["shopLocaleUpdate"]
        if data["userErrors"]:
            sys.exit(f"language publish: {data['userErrors']}")
        print(f"language {LANGUAGE} published")


if __name__ == "__main__":
    main()
