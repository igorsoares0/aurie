#!/usr/bin/env python3
"""Demo store image pipeline.

Builds generation jobs from docs/_design/demo-photos/<preset>/catalog.json,
saves the results, corrects the background tone of packshots and keeps a
manifest (model, prompt, references, prediction id, date) as proof of origin.

Commands:
  plan <preset> [--only a,b] [--editorial] [--ready] [--json]
      List jobs that have no image yet. --ready keeps only jobs whose
      reference images already exist. --json prints model inputs.
  save <preset> <job_id> <url> --model M --prediction P
      Download an output, color-correct packshots and record it.
  run <preset> [--only a,b] [--editorial] [--yes]
      Generate ready jobs directly (needs REPLICATE_API_TOKEN).
  reject <preset> <job_id>
      Move a saved image to images/_rejected so the job is pending again.
  cost <preset>
      Estimated cost of the whole preset.
"""

import argparse
import base64
import io
import json
import os
import re
import unicodedata
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parent.parent

MODELS = {
    "seedream": {
        "id": "bytedance/seedream-5-lite",
        "price": 0.035,
        "input": lambda aspect: {"size": "2K", "aspect_ratio": aspect, "output_format": "jpeg"},
    },
    "pro": {
        "id": "google/nano-banana-pro",
        "price": 0.15,
        "input": lambda aspect: {"resolution": "2K", "aspect_ratio": aspect, "output_format": "jpg"},
    },
}

PACKSHOTS = {"front", "side", "back"}
RETRY_FACTOR = 1.4


def slug(text):
    # Strip accents first so "Bouclé ivory" becomes "boucle-ivory", not "boucl-ivory".
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


def load(preset):
    folder = ROOT / preset
    catalog = json.loads((folder / "catalog.json").read_text(encoding="utf-8"))
    manifest_path = folder / "images" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    return folder, catalog, manifest


def variant_values(product):
    """The option that drives images: metals (Joias) or colors (Moda)."""
    return product.get("metals") or product.get("colors")


def product_jobs(catalog):
    art = catalog["art_direction"]
    style = art["style"]
    packshot_rules = art.get("packshot_rules", "")
    value_prompts = art.get("metal_prompts") or art.get("color_prompts")
    aspect = art.get("aspect", "1:1")
    model_reference = art.get("model_reference")
    jobs = []
    if model_reference:
        jobs.append({
            "id": model_reference,
            "product": None,
            "view": "reference",
            "model": "seedream",
            "aspect": aspect,
            "prompt": f"{art['reference_prompt']} {style} {packshot_rules}",
            "refs": [],
            "alt": "Model reference",
            "file": "model/reference.jpg",
        })
    # Extra models (Moda: petite and tall fits). A product picks one with "model": "<id>".
    for extra in art.get("extra_models", []):
        jobs.append({
            "id": extra["id"],
            "product": None,
            "view": "reference",
            "model": "seedream",
            "aspect": aspect,
            "prompt": f"{extra['prompt']} {style} {packshot_rules}",
            # A reference (usually the main model) keeps background, light and framing identical
            "refs": extra.get("refs", []),
            "alt": extra.get("alt", "Model reference"),
            "file": extra["file"],
        })
    for product in catalog["products"]:
        values = list(variant_values(product))
        base = values[0]
        alt = values[1] if len(values) > 1 else None
        handle = product["handle"]
        for shot in product["shots"]:
            if shot.startswith("metal_swap:"):
                view = shot.split(":", 1)[1]
                value = alt
                prompt = art["shots"]["metal_swap"].format(metal=value_prompts[value])
                refs = [f"{handle}--{slug(base)}--{view}"]
            elif shot.startswith("color_swap:"):
                view = "front"
                value = shot.split(":", 1)[1]
                prompt = art["shots"]["color_swap"].format(garment=product.get("garment", "garment"), color=value_prompts[value])
                refs = [f"{handle}--{slug(base)}--front"]
            else:
                view = shot
                value = base
                prompt = art["shots"][view].format(
                    look=product["look"],
                    metal=value_prompts[value],
                    color=value_prompts[value],
                    styling=product.get("styling", ""),
                    garment=product.get("garment", "garment"),
                    room=product.get("room", ""),
                    detail=product.get("detail_hint", ""),
                    worn=product.get("worn", ""),
                    placement=art.get("placements", {}).get(product["collection"], ""),
                )
                if view == "front":
                    worn_by = product.get("model") or model_reference
                    refs = [worn_by] if worn_by else []
                else:
                    refs = [f"{handle}--{slug(base)}--front"]
            view_label = {"front": "front view", "side": "side view", "back": "back view",
                          "detail": "detail", "worn": "worn", "room": "in a room"}[view]
            jobs.append({
                "id": f"{handle}--{slug(value)}--{view}",
                "product": handle,
                "view": view,
                "model": "seedream",
                "aspect": aspect,
                "prompt": f"{prompt} {style}" + ("" if view in ("worn", "detail", "room") else f" {packshot_rules}"),
                "refs": refs,
                "alt": f"{product['title']} in {value.lower()}, {view_label}",
                "file": f"{handle}/{handle}-{slug(value)}-{view}.jpg",
            })
    gift = catalog.get("gift_card")
    if gift:
        jobs.append({
            "id": "gift-card--front",
            "product": gift["handle"],
            "view": "front",
            "model": "seedream",
            "aspect": "1:1",
            "prompt": f"{gift['image']} {style} {packshot_rules}",
            "refs": [],
            "alt": "Gift card",
            "file": f"{gift['handle']}/{gift['handle']}.jpg",
        })
    return jobs


def editorial_jobs(catalog):
    jobs = []
    for item in catalog["editorial"]:
        refs = []
        for ref in item.get("references", []):
            if ":" not in ref:
                refs.append(ref)  # a plain job id, such as the model reference
                continue
            handle, view = ref.split(":")
            product = next(p for p in catalog["products"] if p["handle"] == handle)
            refs.append(f"{handle}--{slug(next(iter(variant_values(product))))}--{view}")
        jobs.append({
            "id": f"editorial--{item['id']}",
            "product": None,
            "view": "editorial",
            "model": item.get("model", "pro"),
            "aspect": item["aspect"],
            "prompt": f"{item['prompt']} No text, no logo, no watermark.",
            "refs": refs,
            "alt": item.get("alt", ""),
            "file": f"editorial/{item['id']}.jpg",
        })
    return jobs


def all_jobs(catalog):
    return product_jobs(catalog) + editorial_jobs(catalog)


def select(jobs, manifest, folder, only=None, editorial=False, ready=False):
    picked = []
    for job in jobs:
        if job["id"] in manifest:
            continue
        if editorial != (job["view"] == "editorial"):
            continue
        if only and job["product"] not in only and job["id"] not in only:
            continue
        if ready and any(ref not in manifest for ref in job["refs"]):
            continue
        picked.append(job)
    return picked


def model_input(job, ref_values):
    data = {"prompt": job["prompt"], **MODELS[job["model"]]["input"](job["aspect"])}
    if job["refs"]:
        data["image_input"] = ref_values
    return data


def estimate(jobs):
    return sum(MODELS[j["model"]]["price"] for j in jobs)


def correct_background(image, target):
    """Scale RGB channels so the border tone matches the catalog background."""
    rgb = image.convert("RGB")
    width, height = rgb.size
    band = max(8, width // 25)
    strips = [
        rgb.crop((0, 0, width, band)),
        rgb.crop((0, height - band, width, height)),
        rgb.crop((0, 0, band, height)),
        rgb.crop((width - band, 0, width, height)),
    ]
    means = [ImageStat.Stat(strip).mean for strip in strips]
    measured = [sum(mean[c] for mean in means) / len(means) for c in range(3)]
    gains = [min(1.12, max(0.88, target[c] / measured[c])) for c in range(3)]
    channels = [band_img.point(lambda value, g=gains[c]: min(255, round(value * g))) for c, band_img in enumerate(rgb.split())]
    return Image.merge("RGB", channels), measured, gains


def hex_to_rgb(value):
    value = value.lstrip("#")
    return [int(value[i:i + 2], 16) for i in (0, 2, 4)]


def write_manifest(folder, manifest):
    path = folder / "images" / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "demo-images/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def save(preset, job_id, url, model, prediction):
    folder, catalog, manifest = load(preset)
    job = next((j for j in all_jobs(catalog) if j["id"] == job_id), None)
    if job is None:
        sys.exit(f"Unknown job: {job_id}")
    raw_bytes = fetch(url)
    images = folder / "images"
    raw_path = images / "_raw" / job["file"]
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(raw_bytes)
    final_path = images / job["file"]
    final_path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(io.BytesIO(raw_bytes))
    correction = None
    if job["view"] in PACKSHOTS:
        target = hex_to_rgb(catalog["art_direction"]["background"])
        image, measured, gains = correct_background(image, target)
        correction = {"measured_border": [round(v, 1) for v in measured], "gains": [round(g, 3) for g in gains]}
    image.convert("RGB").save(final_path, "JPEG", quality=92, optimize=True)
    manifest[job_id] = {
        "file": job["file"],
        "alt": job["alt"],
        "model": model,
        "prediction": prediction,
        "prompt": job["prompt"],
        "refs": job["refs"],
        "size": list(image.size),
        "color_correction": correction,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    write_manifest(folder, manifest)
    print(f"saved {final_path.relative_to(ROOT)} {image.size[0]}x{image.size[1]}" + (f" gains={correction['gains']}" if correction else ""))


def reject(preset, job_id):
    folder, catalog, manifest = load(preset)
    entry = manifest.pop(job_id, None)
    if entry is None:
        sys.exit(f"No saved image for {job_id}")
    images = folder / "images"
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = images / "_rejected" / f"{Path(entry['file']).stem}-{stamp}.jpg"
    target.parent.mkdir(parents=True, exist_ok=True)
    (images / entry["file"]).rename(target)
    write_manifest(folder, manifest)
    print(f"rejected {job_id} -> {target.relative_to(ROOT)}")


def data_url(path, max_side=1536):
    image = Image.open(path).convert("RGB")
    image.thumbnail((max_side, max_side))
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode()


def replicate_predict(model_id, data, token):
    request = urllib.request.Request(
        f"https://api.replicate.com/v1/models/{model_id}/predictions",
        data=json.dumps({"input": data}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "Prefer": "wait"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        prediction = json.loads(response.read())
    while prediction["status"] in ("starting", "processing"):
        time.sleep(3)
        poll = urllib.request.Request(prediction["urls"]["get"], headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(poll, timeout=60) as response:
            prediction = json.loads(response.read())
    if prediction["status"] != "succeeded":
        raise RuntimeError(f"{prediction['id']}: {prediction['status']} {prediction.get('error')}")
    output = prediction["output"]
    return prediction["id"], output[0] if isinstance(output, list) else output


def run(preset, only, editorial, assume_yes):
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        sys.exit("Set REPLICATE_API_TOKEN first.")
    folder, catalog, manifest = load(preset)
    jobs = select(all_jobs(catalog), manifest, folder, only, editorial, ready=True)
    if not jobs:
        print("Nothing ready to generate.")
        return
    print(f"{len(jobs)} jobs, estimated ${estimate(jobs):.2f}")
    if not assume_yes and input("Generate? [y/N] ").strip().lower() != "y":
        return
    for job in jobs:
        refs = [data_url(folder / "images" / manifest[ref]["file"]) for ref in job["refs"]]
        model_id = MODELS[job["model"]]["id"]
        try:
            prediction, url = replicate_predict(model_id, model_input(job, refs), token)
        except Exception as error:  # keep going; failed jobs stay pending
            print(f"failed {job['id']}: {error}")
            continue
        save(preset, job["id"], url, model_id, prediction)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "run"):
        cmd = sub.add_parser(name)
        cmd.add_argument("preset")
        cmd.add_argument("--only", default="")
        cmd.add_argument("--editorial", action="store_true")
        if name == "plan":
            cmd.add_argument("--ready", action="store_true")
            cmd.add_argument("--json", action="store_true")
        else:
            cmd.add_argument("--yes", action="store_true")
    cmd = sub.add_parser("save")
    cmd.add_argument("preset")
    cmd.add_argument("job_id")
    cmd.add_argument("url")
    cmd.add_argument("--model", required=True)
    cmd.add_argument("--prediction", required=True)
    cmd = sub.add_parser("cost")
    cmd.add_argument("preset")
    cmd = sub.add_parser("reject")
    cmd.add_argument("preset")
    cmd.add_argument("job_id")
    args = parser.parse_args()

    if args.command == "save":
        save(args.preset, args.job_id, args.url, args.model, args.prediction)
        return
    if args.command == "reject":
        reject(args.preset, args.job_id)
        return
    folder, catalog, manifest = load(args.preset)
    if args.command == "cost":
        jobs = all_jobs(catalog)
        done = [j for j in jobs if j["id"] in manifest]
        print(f"{len(jobs)} images ({len(done)} done). Once: ${estimate(jobs):.2f}. With retries: ${estimate(jobs) * RETRY_FACTOR:.2f}")
        return
    only = {item for item in args.only.split(",") if item}
    if args.command == "run":
        run(args.preset, only, args.editorial, args.yes)
        return
    jobs = select(all_jobs(catalog), manifest, folder, only, args.editorial, args.ready)
    if args.json:
        print(json.dumps([{"id": j["id"], "model": MODELS[j["model"]]["id"], "refs": j["refs"], "input": model_input(j, j["refs"])} for j in jobs], indent=2, ensure_ascii=False))
    else:
        for job in jobs:
            print(f"{job['id']:48} {job['model']:9} refs={','.join(job['refs']) or '-'}")
    print(f"# {len(jobs)} jobs, estimated ${estimate(jobs):.2f}", file=sys.stderr)


if __name__ == "__main__":
    main()
