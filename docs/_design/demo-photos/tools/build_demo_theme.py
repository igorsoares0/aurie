#!/usr/bin/env python3
"""Build a demo-store copy of the theme for one preset.

The theme in the repo must not point at demo resources (Theme Store rule), so
images and collections are filled in only in this copy:

  1. copy the theme folders into <preset>/.theme-build
  2. apply listings/<listing>/ (templates and section groups) over it
  3. make the preset current in config/settings_data.json
  4. set the demo images and collections from catalog.json > theme.settings

Push the result as a separate, unpublished theme, for example:
  shopify theme push --store <store> --path <preset>/.theme-build --unpublished --theme "<name>"

Usage:
  python3 tools/build_demo_theme.py <preset>
"""

import argparse
import json
import re
import shutil
from pathlib import Path

DEMO = Path(__file__).resolve().parent.parent
THEME = DEMO.parents[2]
FOLDERS = ("assets", "blocks", "config", "layout", "locales", "sections", "snippets", "templates")


def read_json(path):
    """Return (header, data); Shopify JSON files may start with a /* */ comment."""
    text = path.read_text(encoding="utf-8")
    start = text.index("{")
    header = text[:start]
    body = re.sub(r"/\*.*?\*/", "", text[start:], flags=re.S)
    return header, json.loads(body)


def write_json(path, header, data):
    path.write_text(header + json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def set_path(data, dotted, value):
    keys = dotted.split(".")
    node = data
    for index, key in enumerate(keys[:-1]):
        if key not in node:
            # Only the final "settings" object may be missing; anything else is a typo.
            if key == "settings" and index == len(keys) - 2:
                node[key] = {}
            else:
                raise KeyError(f"{dotted}: '{key}' not found")
        node = node[key]
    node[keys[-1]] = value


def build(preset):
    catalog = json.loads((DEMO / preset / "catalog.json").read_text(encoding="utf-8"))
    theme = catalog["theme"]
    out = DEMO / preset / ".theme-build"
    # Empty the folder instead of removing it: `shopify theme dev` may be running inside it.
    if out.exists():
        for child in out.iterdir():
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    for folder in FOLDERS:
        shutil.copytree(THEME / folder, out / folder)

    # The default preset (Moda) lives in the theme root and has no listing folder.
    if theme.get("listing"):
        listing = THEME / "listings" / theme["listing"]
        for source in listing.rglob("*"):
            if source.is_file():
                target = out / source.relative_to(listing)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

    settings_path = out / "config" / "settings_data.json"
    header, settings = read_json(settings_path)
    if theme["preset"] not in settings.get("presets", {}):
        raise SystemExit(f"Preset {theme['preset']} not found in settings_data.json")
    settings["current"] = theme["preset"]
    write_json(settings_path, header, settings)

    for relative, values in theme.get("settings", {}).items():
        path = out / relative
        header, data = read_json(path)
        for dotted, value in values.items():
            set_path(data, dotted, value)
        write_json(path, header, data)
        print(f"{relative}: {len(values)} settings")
    print(f"Built {out}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("preset")
    build(parser.parse_args().preset)


if __name__ == "__main__":
    main()
